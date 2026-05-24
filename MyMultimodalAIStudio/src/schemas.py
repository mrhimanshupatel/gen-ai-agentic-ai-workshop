"""Data classes for the Multimodal AI Studio."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class UploadedMedia:
    """Represents a file uploaded by the user."""

    file_name: str
    file_type: str  # e.g. "image/png", "audio/wav"
    file_bytes: bytes
    modality: str  # "image", "audio", "video", "text"


@dataclass
class GenerationRequest:
    """Captures everything needed to (mock-)generate output."""

    prompt: str
    input_modality: str
    output_modality: str
    provider: str
    model: str
    temperature: float = 0.7
    max_tokens: int = 1024
    image_size: str = "1024x1024"
    voice: str = "alloy"
    video_duration: int = 5
    uploaded_media: Optional[UploadedMedia] = None
    conversation_history: list[dict] = field(default_factory=list)


@dataclass
class GenerationResult:
    """The output returned by a generation function."""

    content: bytes | str
    mime_type: str  # e.g. "text/markdown", "image/png", "audio/wav"
    output_modality: str
    provider: str
    model: str
    input_modality: str
    created_at: str = field(default_factory=lambda: datetime.now().isoformat(timespec="seconds"))
    metadata: dict = field(default_factory=dict)
