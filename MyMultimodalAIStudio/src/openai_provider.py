"""Real OpenAI provider integration."""

from __future__ import annotations

import base64
import os
from collections.abc import Generator
from datetime import datetime

from openai import OpenAI

from .schemas import GenerationRequest, GenerationResult

# Models that require the Responses API instead of Chat Completions
_RESPONSES_API_MODELS: set[str] = set()


def _uses_responses_api(model: str) -> bool:
    return model in _RESPONSES_API_MODELS


def _build_user_content(req: GenerationRequest) -> list[dict] | str:
    """Build user message content, adding the uploaded image for vision requests."""
    if (
        req.input_modality == "image"
        and req.uploaded_media
        and req.uploaded_media.modality == "image"
    ):
        # Multipart content: image + text prompt
        img_b64 = base64.b64encode(req.uploaded_media.file_bytes).decode()
        mime = req.uploaded_media.file_type or "image/png"
        return [
            {
                "type": "image_url",
                "image_url": {"url": f"data:{mime};base64,{img_b64}"},
            },
            {"type": "text", "text": req.prompt},
        ]
    return req.prompt


def stream_openai_text(req: GenerationRequest) -> Generator[str, None, None]:
    """Stream tokens from OpenAI (auto-selects Responses or Chat Completions API)."""
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    user_content = _build_user_content(req)

    if _uses_responses_api(req.model):
        # Build input for Responses API
        input_items = []
        for msg in req.conversation_history:
            input_items.append({"role": msg["role"], "content": msg["content"]})
        input_items.append({"role": "user", "content": user_content})

        stream = client.responses.create(
            model=req.model,
            input=input_items,
            temperature=req.temperature,
            max_output_tokens=req.max_tokens,
            stream=True,
        )
        for event in stream:
            if event.type == "response.output_text.delta":
                yield event.delta
    else:
        # Chat Completions API
        messages = []
        for msg in req.conversation_history:
            messages.append({"role": msg["role"], "content": msg["content"]})
        messages.append({"role": "user", "content": user_content})

        stream = client.chat.completions.create(
            model=req.model,
            messages=messages,
            temperature=req.temperature,
            max_completion_tokens=req.max_tokens,
            stream=True,
        )
        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content


def generate_openai_text(req: GenerationRequest) -> GenerationResult:
    """Call OpenAI (auto-selects Responses or Chat Completions API)."""
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    if _uses_responses_api(req.model):
        input_items = []
        for msg in req.conversation_history:
            input_items.append({"role": msg["role"], "content": msg["content"]})
        input_items.append({"role": "user", "content": req.prompt})

        response = client.responses.create(
            model=req.model,
            input=input_items,
            temperature=req.temperature,
            max_output_tokens=req.max_tokens,
        )
        content = response.output_text or ""

        return GenerationResult(
            content=content,
            mime_type="text/markdown",
            output_modality="text",
            provider=req.provider,
            model=req.model,
            input_modality=req.input_modality,
            metadata={
                "usage": {
                    "input_tokens": response.usage.input_tokens if response.usage else None,
                    "output_tokens": response.usage.output_tokens if response.usage else None,
                    "total_tokens": response.usage.total_tokens if response.usage else None,
                },
            },
        )
    else:
        messages = []
        for msg in req.conversation_history:
            messages.append({"role": msg["role"], "content": msg["content"]})
        messages.append({"role": "user", "content": req.prompt})

        response = client.chat.completions.create(
            model=req.model,
            messages=messages,
            temperature=req.temperature,
            max_completion_tokens=req.max_tokens,
        )
        content = response.choices[0].message.content or ""

        return GenerationResult(
            content=content,
            mime_type="text/markdown",
            output_modality="text",
            provider=req.provider,
            model=req.model,
            input_modality=req.input_modality,
            metadata={
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens if response.usage else None,
                    "completion_tokens": response.usage.completion_tokens if response.usage else None,
                    "total_tokens": response.usage.total_tokens if response.usage else None,
                },
                "finish_reason": response.choices[0].finish_reason,
            },
        )


def generate_openai_image(req: GenerationRequest) -> GenerationResult:
    """Call the OpenAI Images API to generate an image."""
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.images.generate(
        model="gpt-image-1",
        prompt=req.prompt,
        size=req.image_size,
        n=1,
    )

    # Get base64 image data
    image_data = response.data[0]
    if image_data.b64_json:
        image_bytes = base64.b64decode(image_data.b64_json)
    elif image_data.url:
        import urllib.request
        with urllib.request.urlopen(image_data.url) as resp:
            image_bytes = resp.read()
    else:
        raise ValueError("No image data returned from OpenAI API")

    return GenerationResult(
        content=image_bytes,
        mime_type="image/png",
        output_modality="image",
        provider=req.provider,
        model="gpt-image-1",
        input_modality=req.input_modality,
        metadata={
            "size": req.image_size,
            "revised_prompt": getattr(image_data, "revised_prompt", None),
        },
    )


def generate_openai_audio(req: GenerationRequest) -> GenerationResult:
    """Call the OpenAI TTS API to generate speech from text."""
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice=req.voice if req.voice != "custom" else "alloy",
        input=req.prompt,
    )

    audio_bytes = response.content

    return GenerationResult(
        content=audio_bytes,
        mime_type="audio/mp3",
        output_modality="audio",
        provider=req.provider,
        model="gpt-4o-mini-tts",
        input_modality=req.input_modality,
        metadata={
            "voice": req.voice,
            "prompt_length": len(req.prompt),
        },
    )


def generate_openai_video(req: GenerationRequest) -> GenerationResult:
    """Generate a video by creating an AI image and animating it with a Ken Burns effect."""
    import io
    import imageio.v3 as iio
    import numpy as np
    from PIL import Image

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # Step 1: Generate an image from the prompt
    img_response = client.images.generate(
        model="gpt-image-1",
        prompt=req.prompt,
        size="1024x1024",
        n=1,
    )

    image_data = img_response.data[0]
    if image_data.b64_json:
        img_bytes = base64.b64decode(image_data.b64_json)
    elif image_data.url:
        import urllib.request
        with urllib.request.urlopen(image_data.url) as resp:
            img_bytes = resp.read()
    else:
        raise ValueError("No image data returned from OpenAI API")

    source_img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    src_w, src_h = source_img.size

    # Step 2: Create Ken Burns (slow zoom + pan) animation frames
    fps = 24
    duration = req.video_duration
    total_frames = fps * duration
    out_w, out_h = 512, 512  # output video resolution

    frames = []
    for i in range(total_frames):
        t = i / total_frames  # 0.0 → 1.0

        # Zoom from 100% to 130% over the duration
        zoom = 1.0 + 0.3 * t
        crop_w = int(src_w / zoom)
        crop_h = int(src_h / zoom)

        # Pan: slowly drift from center-left to center-right
        max_offset_x = src_w - crop_w
        max_offset_y = src_h - crop_h
        offset_x = int(max_offset_x * t)
        offset_y = int(max_offset_y * 0.5)

        cropped = source_img.crop((offset_x, offset_y, offset_x + crop_w, offset_y + crop_h))
        resized = cropped.resize((out_w, out_h), Image.LANCZOS)
        frames.append(np.array(resized))

    # Step 3: Write frames to MP4 in memory
    buf = io.BytesIO()
    iio.imwrite(buf, frames, extension=".mp4", fps=fps)
    video_bytes = buf.getvalue()

    return GenerationResult(
        content=video_bytes,
        mime_type="video/mp4",
        output_modality="video",
        provider=req.provider,
        model="gpt-image-1",
        input_modality=req.input_modality,
        metadata={
            "duration_seconds": duration,
            "fps": fps,
            "resolution": f"{out_w}x{out_h}",
            "effect": "Ken Burns (zoom + pan)",
        },
    )
