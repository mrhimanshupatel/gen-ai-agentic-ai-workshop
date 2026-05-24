# Multimodal AI Studio

A **UI-only** Streamlit prototype for a multimodal AI application. All model outputs are **mocked** — no real API calls are made.

## Purpose

Provide a clean, functional UI where users can:

- Enter text prompts or upload images / audio / video / text files
- Select a provider (OpenAI, Claude, Gemini, Groq, OpenRouter, Hugging Face) and model
- Choose input and output modalities (text, image, audio, video)
- See realistic placeholder outputs rendered in the correct format

## Setup

```bash
# Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate    # Windows
# source .venv/bin/activate  # macOS / Linux

# Install dependencies
pip install -r requirements.txt
```

## Run

```bash
streamlit run app.py
```

The app will open at [http://localhost:8501](http://localhost:8501).

## Project Structure

```
app.py                   # Main Streamlit application
src/
  __init__.py
  schemas.py             # Data classes (GenerationRequest, GenerationResult, UploadedMedia)
  model_registry.py      # MODEL_REGISTRY dict + get_models_for_provider()
  mock_generation.py     # Mock generation functions (text, image, audio, video)
  renderers.py           # Streamlit rendering helpers for media & results
  ui_helpers.py          # Session-state init, CSS injection, file-type helpers
.streamlit/
  config.toml            # Streamlit theme and server config
.env                     # API keys (not committed to version control)
requirements.txt
```

## Adding Real Provider Integrations

Replace or extend the mock functions in `src/mock_generation.py`:

1. Create a new module per provider, e.g. `src/providers/openai_provider.py`.
2. Implement a function matching the signature:
   ```python
   def generate(request: GenerationRequest) -> GenerationResult:
       ...
   ```
3. Load the provider's API key from the `.env` file using `os.getenv()`.
4. Update `generate_mock_result()` in `mock_generation.py` to dispatch to the real provider when the key is available.

## Real OpenAI Text-to-Video Route

The **OpenAI text → video** route uses the Sora 2 Videos API for real video generation.
All other routes remain mocked unless separately implemented (text, image, audio are already real for OpenAI).

### Setup

1. Add your OpenAI API key to the global `.env` file:
   ```
   OPENAI_API_KEY=sk-proj-your-key-here
   ```
   Or use `.streamlit/secrets.toml` (copy from `secrets.toml.example`):
   ```toml
   OPENAI_API_KEY = "sk-proj-your-key-here"
   ```

2. Select **OpenAI** as provider, **text** as input modality, **video** as output modality.
3. Choose **sora-2** or **sora-2-pro** as the model.
4. Set video size and duration, then submit a prompt.

### How It Works

- Video generation is **asynchronous** — the app polls the OpenAI API until the job completes.
- A progress bar and status indicator show the current state (queued, in_progress, completed).
- Generated MP4 files are saved under `outputs/videos/`.
- The provider adapter is in `src/providers/openai_video_provider.py`, intentionally isolated for easy replacement if the API changes.

> **Note:** The OpenAI Sora 2 Videos API may change. The provider adapter is designed to be defensive against minor SDK differences.

## Notes

- No API keys are required to run the mock prototype.
- The `.env` file holds API keys (not committed to version control).
- Real OpenAI routes: text→text, text→image, text→audio, text→video.
- Mock outputs are generated locally using PIL (images) and numpy/wave (audio).
