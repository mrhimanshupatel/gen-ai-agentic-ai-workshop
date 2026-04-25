# New Project Setup Instructions

Guide to setting up new daily folders (e.g., 04_12_2026) with simplified shared environment.

---

## Workspace Structure (Simplified)

This workspace uses a **shared virtual environment** approach:

```
Root/
├── pyproject.toml        ← All dependencies here
├── .python-version       ← Python 3.12
├── .venv/                ← Shared by all folders
├── 03_29_2026/           ← Just notebooks/scripts
├── 04_04_2026/           ← Just notebooks/scripts  
├── 04_05_2026/           ← Just notebooks/scripts
└── 04_12_2026/           ← New folder (just notebooks/scripts)
```

**Benefits:**
- ✅ 10-15 GB disk space saved
- ✅ One place to manage dependencies
- ✅ Faster setup for new folders

---

## Quick Setup (2 Steps)

### 1. Create the new folder

```powershell
cd "c:\Exponent\Krish Naik Trainings\Gen AI & Agentic AI"
mkdir 04_12_2026
cd 04_12_2026
```

### 2. Start coding

Create notebooks or Python files:

```powershell
# Create a Jupyter notebook
code my_notebook.ipynb

# Or a Python script
code main.py
```

**Done!** The folder uses the shared root `.venv` automatically.

---

## Managing Dependencies

### View Installed Packages

```powershell
cd "c:\Exponent\Krish Naik Trainings\Gen AI & Agentic AI"
uv pip list
```

### Add New Package

```powershell
cd "c:\Exponent\Krish Naik Trainings\Gen AI & Agentic AI"
uv add package-name==1.2.3
```

Or edit root `pyproject.toml` manually and sync:

```powershell
uv sync
```

This will:
- Read dependencies from all workspace members
- Create/update `uv.lock` lockfile
- Install all packages into the shared `.venv` at the parent level

**Note:** If the `.venv` doesn't exist yet, it will be created automatically with Python 3.12.

### 8. Activate virtual environment (when needed)

```powershell
cd 04_06_2026
..\.venv\Scripts\activate
```

The prompt will show `(.venv)` when activated.

Alternatively, run Python directly without activating:
```powershell
..\.venv\Scripts\python.exe your_script.py
```

## Key Points

- **Shared .venv**: All projects in the workspace share the same virtual environment located at the parent level (`c:\Exponent\Krish Naik Trainings\Gen AI & Agentic AI\.venv`)
- **Workspace management**: Each daily folder is a workspace member that contributes to the shared dependency set
- **Python version**: Using Python 3.12.0 (specified in `.python-version` file in each project folder)
- **Version matching**: Dependencies in `pyproject.toml` must match `requirements.txt` exactly
- **Lock file**: `uv.lock` at workspace root ensures reproducible installs across all projects

## Quick Reference Commands

```powershell
# Create and sync new project
cd "parent-directory"
mkdir new_folder
cd new_folder
uv init
# Edit pyproject.toml to add dependencies
cd ..
uv sync

# Add a new package to existing project
cd project_folder
uv add package-name

# Sync environment with pyproject.toml
cd "parent-directory"
uv sync

# Activate venv
.venv\Scripts\activate  # From parent dir
..\.venv\Scripts\activate  # From project dir

# Run Python without activating
..\.venv\Scripts\python.exe script.py

# List installed packages
..\.venv\Scripts\python.exe -m pip list
```

## Complete Example Workflow

Here's a complete example for creating `04_06_2026`:

```powershell
# 1. Navigate to parent and create folder
cd "c:\Exponent\Krish Naik Trainings\Gen AI & Agentic AI"
mkdir 04_06_2026
cd 04_06_2026

# 2. Copy requirements.txt
Copy-Item ..\04_05_2026\requirements.txt .

# 3. Initialize project
uv init

# 4. Update .python-version
Set-Content .python-version "3.12"

# 5. Edit pyproject.toml
# - Change requires-python to ">=3.12"
# - Copy dependencies from requirements.txt with exact versions

# 6. Edit parent pyproject.toml
# - Add "04_06_2026" to workspace members

# 7. Sync
cd ..
uv sync

# 8. Test
cd 04_06_2026
..\.venv\Scripts\python.exe -c "import sklearn; print(f'scikit-learn: {sklearn.__version__}')"
```

## Troubleshooting

### Version mismatches between requirements.txt and pyproject.toml
Ensure versions match exactly. Compare:
- `requirements.txt`: `scikit-learn==1.4.2`
- `pyproject.toml`: `"scikit-learn==1.4.2"` ✅ (not `>=1.4.2`)

### Wrong Python version in venv
If the `.venv` was created with a different Python version:
```powershell
cd "parent-directory"
Remove-Item -Recurse -Force .venv
uv venv --python 3.12
uv sync
```

### Wrong Python version in venv
If the `.venv` was created with a different Python version:
```powershell
cd "parent-directory"
Remove-Item -Recurse -Force .venv
uv venv --python 3.12
uv sync
```

### Workspace not found
Make sure you run `uv sync` from the parent directory where the main `pyproject.toml` with `[tool.uv.workspace]` is located.

### Virtual environment not activated
If packages aren't found, ensure the venv is activated or use the full path to the Python interpreter:
```powershell
..\.venv\Scripts\python.exe script.py
```

### uv sync fails with build errors
- Check that all version numbers in `pyproject.toml` match `requirements.txt` exactly
- Ensure Python 3.12 is being used (check `.python-version` file)
- Delete `.venv` and `uv.lock`, then run `uv sync` again

## Verification

After setup, verify everything works:

```powershell
cd your_project_folder

# Check Python version
..\.venv\Scripts\python.exe --version
# Should show: Python 3.12.0

# Test core packages
..\.venv\Scripts\python.exe -c "import sklearn, numpy, scipy; print('✓ Core packages working!'); print(f'scikit-learn: {sklearn.__version__}'); print(f'numpy: {numpy.__version__}'); print(f'scipy: {scipy.__version__}')"

# Expected output:
# ✓ Core packages working!
# scikit-learn: 1.4.2
# numpy: 1.26.4
# scipy: 1.11.4
```
