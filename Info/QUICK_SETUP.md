# Quick Setup Guide

Fast reference for creating new daily project folders (e.g., 04_12_2026).  
**Run all commands in VS Code terminal.**

## Overview

This workspace uses a **simplified shared environment** approach:
- ✅ One `.venv` at root level (shared by all folders)
- ✅ Dependencies managed in root `pyproject.toml`
- ✅ No individual `pyproject.toml` or `requirements.txt` in date folders
- ✅ Saves 10-15 GB disk space

---

## Create New Daily Folder

```powershell
# 1. Create folder and navigate
cd "c:\Exponent\Krish Naik Trainings\Gen AI & Agentic AI"
mkdir 04_12_2026
cd 04_12_2026

# 2. Create your notebooks or Python files
# That's it! The folder automatically uses the root .venv
```

---

## Add New Package (Once)

If you need a package not in root dependencies:

```powershell
# Navigate to root
cd "c:\Exponent\Krish Naik Trainings\Gen AI & Agentic AI"

# Add package to root pyproject.toml
uv add package-name

# Or manually edit pyproject.toml and run:
uv sync
```

---

## Verify Environment

```powershell
# From any folder, check Python and packages
..\.venv\Scripts\python.exe --version
..\.venv\Scripts\python.exe -c "import torch, transformers; print(f'torch: {torch.__version__}, transformers: {transformers.__version__}')"
```

**Expected:**
- Python: `3.12.x`
- torch: `2.11.0+`
- transformers: `4.57.6+`

---

## Troubleshooting

**Rebuild shared environment:**
```powershell
cd "c:\Exponent\Krish Naik Trainings\Gen AI & Agentic AI"
Remove-Item -Recurse -Force .venv
uv sync
```

**Check installed packages:**
```powershell
uv pip list
```
