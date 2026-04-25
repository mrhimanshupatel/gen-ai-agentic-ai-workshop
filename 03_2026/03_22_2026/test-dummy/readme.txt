# Initialize a new uv project
uv init my-project

# Or in current directory
uv init

# This creates:
# - pyproject.toml
# - README.md  
# - hello.py (sample file)
# - .python-version

# Create virtual environment
uv venv

# Add dependencies (automatically updates pyproject.toml and creates uv.lock)
uv add numpy

# Sync/install all dependencies
uv sync
