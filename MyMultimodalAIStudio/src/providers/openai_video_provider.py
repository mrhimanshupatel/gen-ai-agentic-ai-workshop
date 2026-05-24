"""OpenAI Sora text-to-video provider adapter.

Uses the OpenAI Videos API (Sora 2) to generate MP4 video from a text prompt.
This module is intentionally isolated so it can be replaced if the API changes.
"""

from __future__ import annotations

import os
import time
import uuid
from pathlib import Path
from typing import Callable

from openai import OpenAI

# Valid parameter values accepted by the API
_VALID_MODELS = {"sora-2", "sora-2-pro"}
_VALID_SECONDS = {4, 8, 12}
_VALID_SIZES = {"1280x720", "720x1280", "1024x1792", "1792x1024"}


def generate_openai_video_from_text(
    prompt: str,
    *,
    api_key: str,
    model: str = "sora-2",
    size: str = "1280x720",
    seconds: int = 4,
    output_dir: str = "outputs/videos",
    poll_interval_seconds: int = 10,
    max_wait_seconds: int = 600,
    progress_callback: Callable[[float, str, str], None] | None = None,
) -> str:
    """Generate a video via OpenAI Sora and return the local MP4 path.

    Args:
        prompt: Text description of the video to generate.
        api_key: OpenAI API key.
        model: One of sora-2, sora-2-pro.
        size: Video resolution.
        seconds: Video duration (4, 8, or 12).
        output_dir: Directory to save the downloaded MP4.
        poll_interval_seconds: How often to check job status.
        max_wait_seconds: Maximum time to wait before raising.
        progress_callback: Optional fn(progress_pct, status, video_id).

    Returns:
        Local file path to the saved MP4 video.

    Raises:
        ValueError: For invalid parameters.
        RuntimeError: If the job fails or times out.
    """
    # ── Validate inputs ──────────────────────────────────────────────────
    if not prompt or not prompt.strip():
        raise ValueError("Prompt must not be empty.")
    if model not in _VALID_MODELS:
        raise ValueError(f"Invalid model '{model}'. Must be one of: {_VALID_MODELS}")
    if seconds not in _VALID_SECONDS:
        raise ValueError(f"Invalid seconds '{seconds}'. Must be one of: {_VALID_SECONDS}")
    if size not in _VALID_SIZES:
        raise ValueError(f"Invalid size '{size}'. Must be one of: {_VALID_SIZES}")

    # ── Setup ────────────────────────────────────────────────────────────
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    client = OpenAI(api_key=api_key)

    # ── Start video generation job ───────────────────────────────────────
    video = client.videos.create(
        model=model,
        prompt=prompt,
        size=size,
        seconds=str(seconds),
    )

    video_id = video.id
    if progress_callback:
        progress_callback(0.0, "queued", video_id)

    # ── Poll until completion ────────────────────────────────────────────
    elapsed = 0
    while elapsed < max_wait_seconds:
        job = client.videos.retrieve(video_id)
        status = getattr(job, "status", "unknown")
        progress = getattr(job, "progress", None)
        progress_pct = float(progress) if progress is not None else 0.0

        if progress_callback:
            progress_callback(progress_pct, status, video_id)

        if status == "completed":
            break
        elif status in ("failed", "cancelled", "expired"):
            error_msg = getattr(job, "error", None) or "No error details provided."
            raise RuntimeError(
                f"OpenAI video generation {status}. "
                f"Video ID: {video_id}. Error: {error_msg}"
            )
        elif status not in ("queued", "in_progress"):
            raise RuntimeError(
                f"Unexpected video job status: '{status}'. Video ID: {video_id}"
            )

        time.sleep(poll_interval_seconds)
        elapsed += poll_interval_seconds
    else:
        raise RuntimeError(
            f"Video generation timed out after {max_wait_seconds}s. "
            f"Video ID: {video_id}. Last status: {status}"
        )

    # ── Download the video ───────────────────────────────────────────────
    file_name = f"openai_video_{uuid.uuid4().hex[:12]}.mp4"
    local_path = out_path / file_name

    # Use the SDK's download helper (GET /videos/{id}/content)
    response = client.videos.download_content(video_id)
    with open(local_path, "wb") as f:
        for chunk in response.iter_bytes():
            f.write(chunk)

    if progress_callback:
        progress_callback(1.0, "downloaded", video_id)

    return str(local_path)
