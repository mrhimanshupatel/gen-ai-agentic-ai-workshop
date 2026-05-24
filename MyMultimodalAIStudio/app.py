"""Multimodal AI Studio — Streamlit UI prototype with mock model outputs."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

# Load the global .env from the workspace root (one level up)
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

import streamlit as st

from src.model_registry import PROVIDERS, get_models_for_provider
from src.mock_generation import generate_mock_result, should_stream
from src.renderers import render_uploaded_media, render_generation_result, render_route_badge
from src.schemas import GenerationRequest, UploadedMedia
from src.ui_helpers import ALL_EXTENSIONS, detect_modality, init_session_state, inject_custom_css

BOUNCING_DOTS_HTML = '<div class="bouncing-dots"><div class="dot"></div><div class="dot"></div><div class="dot"></div></div>'

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Multimodal AI Studio",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_session_state()
inject_custom_css()

# ── Title ────────────────────────────────────────────────────────────────────
st.title("🎨 Multimodal AI Studio")
st.caption(
    "UI prototype with **mock model outputs**. "
    "Real API integrations (OpenAI, Claude, Gemini, Groq, OpenRouter, Hugging Face) "
    "will be plugged in later."
)

# ── Top action buttons (moved to header via JS) ───────────────────────────
st.markdown('<div id="header-action-buttons">', unsafe_allow_html=True)
btn_col1, btn_col2, btn_col3 = st.columns(3)
with btn_col1:
    if st.button("🗑️ Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.last_result = None
        st.rerun()
with btn_col2:
    if st.button("🗑️ Clear uploaded media", use_container_width=True):
        st.session_state.uploaded_media = None
        st.rerun()
with btn_col3:
    if st.button("💾 Save last result to history", use_container_width=True):
        if st.session_state.last_result:
            st.session_state.generation_history.append(st.session_state.last_result)
            st.toast("Result saved to history ✅")
        else:
            st.warning("Nothing to save yet.")
st.markdown('</div>', unsafe_allow_html=True)

# JS to move the buttons into the Streamlit header toolbar
st.markdown(
    """
    <script>
    function moveButtonsToHeader() {
        const marker = document.getElementById('header-action-buttons');
        const header = document.querySelector('header[data-testid="stHeader"]');
        if (marker && header) {
            // Find the horizontal block (the columns) right after the marker
            const wrapper = marker.closest('.stMarkdown');
            if (wrapper) {
                const hBlock = wrapper.nextElementSibling;
                if (hBlock && !header.contains(hBlock)) {
                    // Position in header
                    hBlock.style.position = 'fixed';
                    hBlock.style.top = '6px';
                    hBlock.style.left = '50%';
                    hBlock.style.transform = 'translateX(-50%)';
                    hBlock.style.zIndex = '999999';
                    hBlock.style.width = 'auto';
                    hBlock.style.minWidth = '500px';
                    // Hide the marker div
                    wrapper.style.display = 'none';
                }
            }
        }
    }
    // Run after DOM settles
    setTimeout(moveButtonsToHeader, 200);
    setTimeout(moveButtonsToHeader, 800);
    </script>
    """,
    unsafe_allow_html=True,
)

st.divider()

# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR — Model Settings
# ═══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.header("⚙️ Model Settings")

    provider = st.selectbox("Provider", PROVIDERS)
    input_modality = st.selectbox("Input modality", ["text", "image", "audio", "video"])
    output_modality = st.selectbox("Output modality", ["text", "image", "audio", "video"])

    models = get_models_for_provider(provider)
    # Auto-select the best model based on modality
    if provider == "OpenAI":
        if output_modality == "image":
            default_idx = models.index("gpt-image-1") if "gpt-image-1" in models else 0
        elif output_modality == "audio":
            default_idx = models.index("gpt-4o-mini-tts") if "gpt-4o-mini-tts" in models else 0
        elif output_modality == "text":
            default_idx = models.index("gpt-5.2") if "gpt-5.2" in models else 0
        elif output_modality == "video":
            default_idx = models.index("sora-2") if "sora-2" in models else 0
        elif input_modality == "audio" and output_modality == "text":
            default_idx = models.index("gpt-4o-transcribe") if "gpt-4o-transcribe" in models else 0
        else:
            default_idx = 0
    else:
        default_idx = 0
    model = st.selectbox("Model", models, index=default_idx) if models else "default"

    temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.05)
    max_tokens = st.number_input("Max tokens", min_value=64, max_value=16384, value=1024, step=64)

    st.divider()
    st.subheader("Image settings")
    image_size = st.selectbox("Image size", ["1024x1024", "1024x1792", "1792x1024"])

    st.subheader("Audio settings")
    voice = st.selectbox("Voice", ["alloy", "verse", "aria", "custom"])

    st.subheader("Video settings")
    _is_sora = provider == "OpenAI" and output_modality == "video"
    if _is_sora:
        video_size = st.selectbox("Video size", ["1280x720", "720x1280", "1024x1792", "1792x1024"])
        video_duration = st.selectbox("Video duration (s)", [4, 8, 12], index=0)
    else:
        video_size = "1280x720"
        video_duration = st.slider("Video duration (s)", 2, 10, 5)

    # Route preview
    st.divider()
    st.subheader("🗺️ Route Preview")
    render_route_badge(input_modality, output_modality)
    st.markdown(f"`{provider}` / `{model}`")

# ═══════════════════════════════════════════════════════════════════════════════
# FILE UPLOADER (fallback above chat input)
# ═══════════════════════════════════════════════════════════════════════════════
uploaded_file = st.file_uploader("📁 Upload media", type=ALL_EXTENSIONS)
if uploaded_file is not None:
    modality = detect_modality(uploaded_file.name, uploaded_file.type)
    st.session_state.uploaded_media = UploadedMedia(
        file_name=uploaded_file.name,
        file_type=uploaded_file.type or "",
        file_bytes=uploaded_file.getvalue(),
        modality=modality,
    )

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN LAYOUT — two columns
# ═══════════════════════════════════════════════════════════════════════════════
col_left, col_right = st.columns([2, 1], gap="large")

# ── Left column: conversation + input preview ────────────────────────────────
with col_left:
    st.subheader("💬 Conversation")

    # Conversation history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Uploaded-media preview
    if st.session_state.uploaded_media:
        with st.expander("📎 Uploaded input preview", expanded=True):
            render_uploaded_media(st.session_state.uploaded_media)

# ── Right column: output preview ─────────────────────────────────────────────
with col_right:
    st.subheader("🖼️ Output Preview")

    if st.session_state.last_result:
        res = st.session_state.last_result
        # Only show full output preview for non-text modalities;
        # text responses are already displayed in the conversation column.
        if res.output_modality != "text":
            st.markdown('<div class="output-card">', unsafe_allow_html=True)
            render_generation_result(res)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            with st.expander("📋 Last Response Metadata", expanded=True):
                st.markdown(
                    f"- **Provider:** {res.provider}\n"
                    f"- **Model:** {res.model}\n"
                    f"- **Input modality:** {res.input_modality}\n"
                    f"- **Output modality:** {res.output_modality}\n"
                    f"- **Timestamp:** {res.created_at}"
                )
                if res.metadata:
                    st.json(res.metadata)
    else:
        st.info("Run a generation to see output here.")

    # History
    if st.session_state.generation_history:
        with st.expander(f"📜 History ({len(st.session_state.generation_history)} items)"):
            for i, res in enumerate(st.session_state.generation_history):
                st.markdown(f"**#{i+1}** — {res.provider}/{res.model} "
                            f"({res.input_modality}→{res.output_modality}) "
                            f"@ {res.created_at}")

# ═══════════════════════════════════════════════════════════════════════════════
# CHAT INPUT
# ═══════════════════════════════════════════════════════════════════════════════
prompt = st.chat_input("Type your prompt…")

if prompt:
    # Validate
    if input_modality != "text" and st.session_state.uploaded_media is None:
        st.warning(
            f"Input modality is **{input_modality}** but no file was uploaded. "
            "Please upload a file or switch input modality to text."
        )
    else:
        # Record user message
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Last 2 conversation exchanges (4 messages: user+assistant pairs)
        history = st.session_state.messages[-4:] if len(st.session_state.messages) > 1 else []

        # Build request
        request = GenerationRequest(
            prompt=prompt,
            input_modality=input_modality,
            output_modality=output_modality,
            provider=provider,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            image_size=image_size,
            voice=voice,
            video_duration=video_duration,
            uploaded_media=st.session_state.uploaded_media,
            conversation_history=history,
        )

        # Generate
        # ── Real OpenAI Sora text-to-video ────────────────────────────────
        if (
            provider == "OpenAI"
            and input_modality == "text"
            and output_modality == "video"
            and model in ("sora-2", "sora-2-pro")
            and os.getenv("OPENAI_API_KEY")
        ):
            from src.providers.openai_video_provider import generate_openai_video_from_text
            from src.schemas import GenerationResult

            with col_left:
                with st.chat_message("user"):
                    st.markdown(prompt)
                with st.chat_message("assistant"):
                    dots_sora = st.empty()
                    dots_sora.markdown(BOUNCING_DOTS_HTML, unsafe_allow_html=True)

            try:
                dots_sora.empty()
                progress_bar = st.progress(0, text="Starting video generation…")
                status_text = st.empty()

                def _progress_cb(pct: float, status: str, vid_id: str) -> None:
                    progress_bar.progress(
                        min(pct, 1.0),
                        text=f"Status: {status} | Video ID: {vid_id}",
                    )
                    status_text.caption(
                        f"⏳ {status} — {pct*100:.0f}% | ID: {vid_id}"
                    )

                video_path = generate_openai_video_from_text(
                    prompt=prompt,
                    api_key=os.getenv("OPENAI_API_KEY"),
                    model=model,
                    size=video_size,
                    seconds=video_duration,
                    progress_callback=_progress_cb,
                )

                progress_bar.progress(1.0, text="✅ Video ready!")
                status_text.empty()

                result = GenerationResult(
                    content=video_path,
                    mime_type="video/mp4",
                    output_modality="video",
                    provider="OpenAI",
                    model=model,
                    input_modality="text",
                    metadata={
                        "route": "text_to_video",
                        "video_size": video_size,
                        "video_duration": video_duration,
                        "is_real_generation": True,
                    },
                )
                st.session_state.last_result = result
                st.session_state.messages.append(
                    {"role": "assistant", "content": f"✅ Generated video using OpenAI/{model}."}
                )
                st.rerun()

            except Exception as e:
                st.error(f"Video generation failed: {e}")
                st.session_state.messages.append(
                    {"role": "assistant", "content": f"❌ Video generation failed: {e}"}
                )
                st.rerun()

        # ── Streaming text (Chat Completions / Responses API) ─────────────
        elif should_stream(request):
            from src.openai_provider import stream_openai_text
            from src.schemas import GenerationResult

            # Show user message immediately
            with col_left:
                with st.chat_message("user"):
                    st.markdown(prompt)
                with st.chat_message("assistant"):
                    # Show bouncing dots until first chunk arrives
                    dots_placeholder = st.empty()
                    dots_placeholder.markdown(BOUNCING_DOTS_HTML, unsafe_allow_html=True)

                    def _stream_clear_dots(gen, ph):
                        first = True
                        for chunk in gen:
                            if first:
                                ph.empty()
                                first = False
                            yield chunk

                    streamed_content = st.write_stream(
                        _stream_clear_dots(stream_openai_text(request), dots_placeholder)
                    )

            result = GenerationResult(
                content=streamed_content,
                mime_type="text/markdown",
                output_modality="text",
                provider=provider,
                model=model,
                input_modality=input_modality,
            )
            st.session_state.last_result = result
            st.session_state.messages.append({"role": "assistant", "content": streamed_content})
            st.rerun()
        else:
            with col_left:
                with st.chat_message("user"):
                    st.markdown(prompt)
                with st.chat_message("assistant"):
                    dots = st.empty()
                    dots.markdown(BOUNCING_DOTS_HTML, unsafe_allow_html=True)
                    result = generate_mock_result(request)
                    dots.empty()
            st.session_state.last_result = result

            # Add assistant response to conversation
            if result.output_modality == "text" or result.mime_type == "text/markdown":
                content = result.content if isinstance(result.content, str) else result.content.decode()
                st.session_state.messages.append({"role": "assistant", "content": content})
            else:
                st.session_state.messages.append(
                    {"role": "assistant", "content": f"✅ Generated {result.output_modality} output — see the Output Preview panel."}
                )

            st.rerun()
