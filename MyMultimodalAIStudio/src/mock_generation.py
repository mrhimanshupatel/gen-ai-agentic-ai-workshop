"""Generation functions — real providers where available, mock fallbacks elsewhere."""

from __future__ import annotations

import io
import math
import os
import struct
import wave
from datetime import datetime

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from .schemas import GenerationRequest, GenerationResult


# ---------------------------------------------------------------------------
# Text mock
# ---------------------------------------------------------------------------

def _mock_text(req: GenerationRequest) -> GenerationResult:
    prompt_snippet = (req.prompt[:80] + "…") if len(req.prompt) > 80 else req.prompt
    input_desc = req.input_modality
    if req.uploaded_media:
        input_desc += f" ({req.uploaded_media.file_name})"

    md = (
        f"### Mock Text Response\n\n"
        f"**Provider:** {req.provider}  \n"
        f"**Model:** {req.model}  \n"
        f"**Input modality:** {input_desc}  \n"
        f"**Prompt:** {prompt_snippet}  \n"
        f"**Temperature:** {req.temperature}  \n"
        f"**Max tokens:** {req.max_tokens}  \n\n"
        f"---\n\n"
        f"This is a **mock response**. In production, the `{req.provider}` "
        f"API would be called with model `{req.model}` to generate a real "
        f"text completion.\n\n"
        f"Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
        f"Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. "
        f"Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.\n\n"
        f"*Generated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"
    )
    return GenerationResult(
        content=md,
        mime_type="text/markdown",
        output_modality="text",
        provider=req.provider,
        model=req.model,
        input_modality=req.input_modality,
    )


# ---------------------------------------------------------------------------
# Image mock — generates a placeholder PNG with PIL
# ---------------------------------------------------------------------------

def _mock_image(req: GenerationRequest) -> GenerationResult:
    w, h = (int(x) for x in req.image_size.split("x"))
    img = Image.new("RGB", (w, h), color=(30, 33, 48))
    draw = ImageDraw.Draw(img)

    # gradient background
    for y in range(h):
        r = int(30 + 60 * (y / h))
        g = int(33 + 40 * (y / h))
        b = int(48 + 80 * (y / h))
        draw.line([(0, y), (w, y)], fill=(r, g, b))

    # centre text
    try:
        font = ImageFont.truetype("arial.ttf", 32)
        font_sm = ImageFont.truetype("arial.ttf", 20)
    except OSError:
        font = ImageFont.load_default()
        font_sm = font

    title = "Mock Image Output"
    draw.text((w // 2, h // 3), title, fill="white", font=font, anchor="mm")
    draw.text((w // 2, h // 2), f"{req.provider} / {req.model}", fill="#aaa", font=font_sm, anchor="mm")
    prompt_short = (req.prompt[:60] + "…") if len(req.prompt) > 60 else req.prompt
    draw.text((w // 2, h // 2 + 40), f'"{prompt_short}"', fill="#888", font=font_sm, anchor="mm")
    draw.text((w // 2, h * 2 // 3), f"{w}×{h}", fill="#666", font=font_sm, anchor="mm")

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return GenerationResult(
        content=buf.getvalue(),
        mime_type="image/png",
        output_modality="image",
        provider=req.provider,
        model=req.model,
        input_modality=req.input_modality,
    )


# ---------------------------------------------------------------------------
# Audio mock — generates a short sine-wave WAV
# ---------------------------------------------------------------------------

def _mock_audio(req: GenerationRequest) -> GenerationResult:
    sample_rate = 22050
    duration = 2.0  # seconds
    freq = 440.0  # A4 note
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    # fade-in / fade-out envelope
    envelope = np.ones_like(t)
    fade = int(sample_rate * 0.1)
    envelope[:fade] = np.linspace(0, 1, fade)
    envelope[-fade:] = np.linspace(1, 0, fade)
    samples = (0.5 * np.sin(2 * math.pi * freq * t) * envelope * 32767).astype(np.int16)

    buf = io.BytesIO()
    with wave.open(buf, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(samples.tobytes())
    return GenerationResult(
        content=buf.getvalue(),
        mime_type="audio/wav",
        output_modality="audio",
        provider=req.provider,
        model=req.model,
        input_modality=req.input_modality,
    )


# ---------------------------------------------------------------------------
# Video mock — placeholder message (no heavy deps)
# ---------------------------------------------------------------------------

def _mock_video(req: GenerationRequest) -> GenerationResult:
    md = (
        f"### Mock Video Placeholder\n\n"
        f"**Provider:** {req.provider}  \n"
        f"**Model:** {req.model}  \n"
        f"**Requested duration:** {req.video_duration}s  \n\n"
        f"Real video generation requires heavy dependencies (e.g. OpenCV, ffmpeg). "
        f"This placeholder will be replaced once `{req.provider}` video API "
        f"integration is implemented.\n\n"
        f"*Generated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"
    )
    return GenerationResult(
        content=md,
        mime_type="text/markdown",
        output_modality="video",
        provider=req.provider,
        model=req.model,
        input_modality=req.input_modality,
        metadata={"note": "video mock — text placeholder only"},
    )


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

_GENERATORS = {
    "text": _mock_text,
    "image": _mock_image,
    "audio": _mock_audio,
    "video": _mock_video,
}


def should_stream(request: GenerationRequest) -> bool:
    """Return True if this request should use streaming."""
    return (
        request.provider == "OpenAI"
        and request.output_modality == "text"
        and request.input_modality in ("text", "image")
        and bool(os.getenv("OPENAI_API_KEY"))
    )


def generate_mock_result(request: GenerationRequest) -> GenerationResult:
    """Route to real provider if available, otherwise use mock."""
    # Real OpenAI text generation (non-streaming fallback)
    if should_stream(request):
        from .openai_provider import generate_openai_text
        return generate_openai_text(request)

    # Real OpenAI image generation
    if (
        request.provider == "OpenAI"
        and request.output_modality == "image"
        and os.getenv("OPENAI_API_KEY")
    ):
        from .openai_provider import generate_openai_image
        return generate_openai_image(request)

    # Real OpenAI TTS audio generation
    if (
        request.provider == "OpenAI"
        and request.output_modality == "audio"
        and os.getenv("OPENAI_API_KEY")
    ):
        from .openai_provider import generate_openai_audio
        return generate_openai_audio(request)

    # Real OpenAI video generation (image + Ken Burns animation)
    if (
        request.provider == "OpenAI"
        and request.output_modality == "video"
        and os.getenv("OPENAI_API_KEY")
    ):
        from .openai_provider import generate_openai_video
        return generate_openai_video(request)

    # Fallback to mock
    gen_fn = _GENERATORS.get(request.output_modality, _mock_text)
    return gen_fn(request)
