"""Streamlit rendering helpers for uploaded media and generation results."""

from __future__ import annotations

import os

import streamlit as st

from .schemas import GenerationResult, UploadedMedia


# ---------------------------------------------------------------------------
# Uploaded-media preview
# ---------------------------------------------------------------------------

def render_uploaded_media(media: UploadedMedia) -> None:
    """Display a preview of the uploaded file in Streamlit."""
    st.caption(f"📎 {media.file_name} ({media.modality})")

    if media.modality == "image":
        st.image(media.file_bytes, use_container_width=True)
    elif media.modality == "audio":
        st.audio(media.file_bytes)
    elif media.modality == "video":
        st.video(media.file_bytes)
    elif media.modality == "text":
        try:
            text = media.file_bytes.decode("utf-8", errors="replace")
            st.markdown(f"```\n{text[:2000]}\n```")
        except Exception:
            st.info("Unable to decode text file.")


# ---------------------------------------------------------------------------
# Generation-result rendering
# ---------------------------------------------------------------------------

def render_generation_result(result: GenerationResult) -> None:
    """Render a GenerationResult in the output panel."""
    if result.output_modality == "text" or result.mime_type == "text/markdown":
        content = result.content if isinstance(result.content, str) else result.content.decode()
        st.markdown(content)

    elif result.output_modality == "image" and isinstance(result.content, bytes):
        st.image(result.content, use_container_width=True)
        st.download_button(
            "⬇️ Download image",
            data=result.content,
            file_name="mock_output.png",
            mime="image/png",
        )

    elif result.output_modality == "audio" and isinstance(result.content, bytes):
        st.audio(result.content)
        st.download_button(
            "⬇️ Download audio",
            data=result.content,
            file_name="mock_output.wav",
            mime="audio/wav",
        )

    elif result.output_modality == "video":
        if isinstance(result.content, bytes) and result.mime_type.startswith("video/"):
            st.video(result.content)
            st.download_button(
                "⬇️ Download MP4",
                data=result.content,
                file_name="generated_video.mp4",
                mime="video/mp4",
            )
        elif isinstance(result.content, str) and os.path.isfile(result.content):
            # Content is a local file path (e.g. from Sora generation)
            st.video(result.content)
            with open(result.content, "rb") as f:
                st.download_button(
                    "⬇️ Download MP4",
                    data=f,
                    file_name="generated_video.mp4",
                    mime="video/mp4",
                )
        elif isinstance(result.content, str):
            # Markdown placeholder (mock)
            st.markdown(result.content)
        else:
            st.error("Video file not found or unsupported format.")

    else:
        st.info("Unsupported output type.")

    # Metadata
    with st.expander("📋 Metadata"):
        st.markdown(
            f"- **Provider:** {result.provider}\n"
            f"- **Model:** {result.model}\n"
            f"- **Input modality:** {result.input_modality}\n"
            f"- **Output modality:** {result.output_modality}\n"
            f"- **Timestamp:** {result.created_at}"
        )
        if result.metadata:
            st.json(result.metadata)


# ---------------------------------------------------------------------------
# Route badge
# ---------------------------------------------------------------------------

def render_route_badge(input_modality: str, output_modality: str) -> None:
    """Show a small route-preview badge."""
    direct_routes = {
        ("text", "text"),
        ("text", "image"),
        ("text", "audio"),
        ("text", "video"),
        ("image", "text"),
        ("audio", "text"),
    }
    is_direct = (input_modality, output_modality) in direct_routes
    route_type = "✅ direct" if is_direct else "🔀 text-bridge mock"
    st.markdown(
        f"**{input_modality}** → **{output_modality}**  \n"
        f"Route: {route_type}"
    )
