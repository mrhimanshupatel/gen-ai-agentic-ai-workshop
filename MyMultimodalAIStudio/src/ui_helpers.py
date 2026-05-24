"""Small UI helper utilities for the Streamlit app."""

from __future__ import annotations

import streamlit as st

# ---------------------------------------------------------------------------
# Accepted file extensions
# ---------------------------------------------------------------------------

IMAGE_EXTENSIONS = ["png", "jpg", "jpeg", "webp"]
AUDIO_EXTENSIONS = ["mp3", "wav", "m4a", "webm"]
VIDEO_EXTENSIONS = ["mp4", "mov", "webm", "mkv"]
TEXT_EXTENSIONS = ["txt", "md", "py", "json", "csv"]
ALL_EXTENSIONS = IMAGE_EXTENSIONS + AUDIO_EXTENSIONS + VIDEO_EXTENSIONS + TEXT_EXTENSIONS


def detect_modality(file_name: str, mime: str | None = None) -> str:
    """Infer modality from file name or MIME type."""
    ext = file_name.rsplit(".", 1)[-1].lower() if "." in file_name else ""
    if ext in IMAGE_EXTENSIONS:
        return "image"
    if ext in AUDIO_EXTENSIONS:
        return "audio"
    if ext in VIDEO_EXTENSIONS:
        return "video"
    if ext in TEXT_EXTENSIONS:
        return "text"
    if mime:
        if mime.startswith("image"):
            return "image"
        if mime.startswith("audio"):
            return "audio"
        if mime.startswith("video"):
            return "video"
    return "text"


# ---------------------------------------------------------------------------
# Session-state initialiser
# ---------------------------------------------------------------------------

def init_session_state() -> None:
    """Ensure all required session-state keys exist."""
    defaults = {
        "messages": [],
        "uploaded_media": None,
        "last_result": None,
        "generation_history": [],
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


# ---------------------------------------------------------------------------
# Inject lightweight custom CSS
# ---------------------------------------------------------------------------

def inject_custom_css() -> None:
    st.markdown(
        """
        <style>
        /* output card */
        .output-card {
            background: #1E2130;
            border-radius: 12px;
            padding: 1.2rem;
            border: 1px solid #2d3250;
            margin-bottom: 1rem;
        }
        /* route badge */
        .route-badge {
            display: inline-block;
            padding: 0.25rem 0.7rem;
            border-radius: 20px;
            background: #2d3250;
            color: #ccc;
            font-size: 0.85rem;
            margin-bottom: 0.5rem;
        }
        /* metadata block */
        .meta-block {
            font-size: 0.8rem;
            color: #888;
            margin-top: 0.5rem;
        }
        /* compact sidebar sections */
        section[data-testid="stSidebar"] .block-container {
            padding-top: 1rem;
        }
        /* Style header buttons when moved into toolbar */
        #header-action-buttons {
            display: flex;
            gap: 6px;
            align-items: center;
        }
        #header-action-buttons button {
            padding: 0.15rem 0.7rem !important;
            font-size: 0.78rem !important;
            min-height: 0 !important;
            height: auto !important;
        }
        /* Bouncing dots animation */
        .bouncing-dots {
            display: flex;
            gap: 6px;
            padding: 12px 0;
        }
        .bouncing-dots .dot {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: #888;
            animation: bounce 1.4s infinite ease-in-out both;
        }
        .bouncing-dots .dot:nth-child(1) { animation-delay: -0.32s; }
        .bouncing-dots .dot:nth-child(2) { animation-delay: -0.16s; }
        .bouncing-dots .dot:nth-child(3) { animation-delay: 0s; }
        @keyframes bounce {
            0%, 80%, 100% { transform: scale(0); }
            40% { transform: scale(1.0); }
        }
        /* Sticky Output Preview — right column stays visible while scrolling */
        [data-testid="stColumns"] > div:last-child {
            position: sticky;
            top: 3.5rem;
            align-self: flex-start;
            max-height: calc(100vh - 4rem);
            overflow-y: auto;
        }
        /* Separate scrollable chat panel for left column */
        [data-testid="stColumns"] > div:first-child {
            max-height: calc(100vh - 4rem);
            overflow-y: auto;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
