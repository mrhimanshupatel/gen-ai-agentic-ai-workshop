# Gen AI & Agentic AI Training

Training workspace for Gen AI and Agentic AI projects.

## Workspace Structure

**Simplified shared environment approach:**
- ✅ Single `.venv` at root (shared by all date folders)
- ✅ All dependencies in root `pyproject.toml`
- ✅ Saves 10-15 GB disk space

## Training Folders
- 03_22_2026 - Initial projects
- 03_28_2026 - Early training
- 03_29_2026 - Encoding & Embedding
- 04_04_2026 - Encoding practice
- 04_05_2026 - Classical word embeddings
- 04_11_2026 - Ready for content

## Setup

### Initial Setup
```bash
# Install dependencies (first time only)
uv sync
```

### Create New Daily Folder
```bash
# Just create and start working
mkdir 04_12_2026
cd 04_12_2026
# Create notebooks/scripts - automatically uses root .venv
```

### Add New Package
```bash
# From root directory
uv add package-name
```

## Documentation
- [QUICK_SETUP.md](QUICK_SETUP.md) - Fast reference
- [DAILY_NEW_SETUP.md](DAILY_NEW_SETUP.md) - Complete guide
- [NEW_PROJECT_SETUP.md](NEW_PROJECT_SETUP.md) - Detailed setup
