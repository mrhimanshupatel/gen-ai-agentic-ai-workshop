# Daily New Folder Setup Guide

Complete step-by-step guide for creating new daily/weekly project folders (e.g., 04_12_2026, 04_13_2026).  
**Run all commands in VS Code terminal (PowerShell).**

---

## Current Workspace Structure

This workspace uses a **simplified shared environment**:
- One `.venv` at root level (shared by all date folders)
- All dependencies in root `pyproject.toml`
- No individual `pyproject.toml` or `requirements.txt` per folder
- Saves ~10-15 GB disk space

---

## Prerequisites

- Shared `.venv` folder exists at root level
- Python 3.12 installed
- Root `pyproject.toml` contains all required dependencies

---

## Setup Steps

### 1. Create New Folder

```powershell
cd "c:\Exponent\Krish Naik Trainings\Gen AI & Agentic AI"
mkdir 04_12_2026
cd 04_12_2026
```

### 2. Start Working

Create notebooks, Python files, or any code:

```powershell
# Create a Jupyter notebook
code encoding.ipynb

# Or create a Python script
code main.py
```

**That's it!** The folder automatically uses the shared root `.venv`.

---

## Adding New Dependencies (When Needed)

If you need a package not currently installed:

### Option A: Using uv add (Recommended)

```powershell
cd "c:\Exponent\Krish Naik Trainings\Gen AI & Agentic AI"
uv add package-name==version
```

### Option B: Manual Edit

1. Edit root `pyproject.toml` and add to `dependencies` list
2. Run sync:

```powershell
cd "c:\Exponent\Krish Naik Trainings\Gen AI & Agentic AI"
uv sync
```

---

## Verification

### Verify Environment from Any Folder

```powershell
cd 04_12_2026
..\.venv\Scripts\python.exe --version
```

**Expected:** `Python 3.12.0`

### Verify Package Installation

```powershell
..\.venv\Scripts\python.exe -c "import sklearn, numpy; print(f'sklearn: {sklearn.__version__}, numpy: {numpy.__version__}')"
```

**Expected:** `sklearn: 1.4.2, numpy: 1.26.4`

---

## Project Structure Created

```
04_12_2026/
├── .git/
├── .gitignore
├── .python-version       (3.12)
├── main.py              (starter file)
├── pyproject.toml       (with all dependencies)
├── README.md
└── requirements.txt     (copied)
```

---

## Important Notes

### ✅ What You Have
- **One shared `.venv`** at root level for ALL day folders
- **Root `pyproject.toml`** defines workspace dependencies (NO build-system)
- Each day folder is a **workspace member** (auto-added by `uv init`)

### ❌ What You DON'T Need
- Separate `.venv` in each day folder
- `[build-system]` section in root `pyproject.toml`
- Manual workspace member updates (uv handles this)

### 🔧 Root pyproject.toml Configuration

Your root `pyproject.toml` should look like this (NO build-system):

```toml
[project]
name = "gen-ai-agentic-ai"
version = "0.1.0"
description = "Gen AI & Agentic AI Training"
readme = "README.md"
requires-python = ">=3.10"
dependencies = [
    "scikit-learn==1.4.2",
    "rank-bm25==0.2.2",
    "numpy==1.26.4",
    # ... other dependencies
]
```

**Do NOT include:**
```toml
[build-system]  # ❌ Remove this section
requires = ["hatchling"]
build-backend = "hatchling.build"
```

---

## Running Your Code

```powershell
cd "c:\Exponent\Krish Naik Trainings\Gen AI & Agentic AI\04_12_2026"
..\.venv\Scripts\python.exe main.py
```

Or activate the virtual environment:
```powershell
& "c:\Exponent\Krish Naik Trainings\Gen AI & Agentic AI\.venv\Scripts\Activate.ps1"
python main.py
```

---

## Troubleshooting

### Error: "Unable to determine which files to ship inside the wheel"

**Problem:** Root `pyproject.toml` has `[build-system]` section

**Solution:** Remove the `[build-system]` section from root `pyproject.toml` (it's a workspace container, not a package)

### Wrong Python Version

```powershell
cd "c:\Exponent\Krish Naik Trainings\Gen AI & Agentic AI"
Remove-Item -Recurse -Force .venv
uv venv --python 3.12
uv sync
```

### Packages Not Found

```powershell
cd "c:\Exponent\Krish Naik Trainings\Gen AI & Agentic AI"
uv sync --reinstall
```

---

**Last Updated:** April 5, 2026  
**Tested Setup:** 04_11_2026
