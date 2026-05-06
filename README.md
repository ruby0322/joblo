# joblo

## Cloud agent environment

This repo configures Cursor Cloud agents via `.cursor/environment.json`.

- Dependencies are installed by `scripts/monorepo_bootstrap.py`.
- The install step enforces Python 3.12+ before package installation.
- The bootstrap script installs root `requirements.txt` and any future:
  - `services/*/requirements.txt`
  - `packages/*/requirements.txt`

After startup, these commands should run without additional setup:

- `ruff check .`
- `python3 -m unittest`

## Monorepo preparation

The repository is now prepared for a service/package workspace layout:

- `services/` for deployable applications
- `packages/` for shared libraries

Current code still works from the existing root layout, while test import
resolution already supports both current and future monorepo paths.
