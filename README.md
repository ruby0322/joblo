# joblo

## Cloud agent environment

This repo configures Cursor Cloud agents via `.cursor/environment.json`.

- Dependencies are installed from `requirements.txt`.
- The install step enforces Python 3.12+ before package installation.

After startup, these commands should run without additional setup:

- `ruff check .`
- `python3 -m unittest`
