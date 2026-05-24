"""Model registry mapping providers to their available models."""

from __future__ import annotations

MODEL_REGISTRY: dict[str, list[str]] = {
    "OpenAI": [
        "gpt-5.2",
        "gpt-4.1",
        "gpt-4o",
        "gpt-image-1",
        "gpt-4o-mini-tts",
        "gpt-4o-transcribe",
        "sora-2",
        "sora-2-pro",
    ],
    "Claude": [
        "claude-opus-4",
        "claude-sonnet-4",
        "claude-haiku-3.5",
    ],
    "Gemini": [
        "gemini-2.5-pro",
        "gemini-2.5-flash",
        "imagen",
        "veo",
    ],
    "Groq": [
        "llama-3.3-70b-versatile",
        "whisper-large-v3-turbo",
    ],
    "OpenRouter": [
        "auto",
        "multimodal-router",
    ],
    "Hugging Face": [
        "text-generation-model",
        "image-generation-model",
        "speech-recognition-model",
        "text-to-speech-model",
        "video-generation-model",
    ],
}

PROVIDERS = list(MODEL_REGISTRY.keys())


def get_models_for_provider(provider: str) -> list[str]:
    """Return the list of models available for a given provider."""
    return MODEL_REGISTRY.get(provider, [])
