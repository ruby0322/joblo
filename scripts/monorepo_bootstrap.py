from __future__ import annotations

import subprocess
import sys
from pathlib import Path


REQUIRED_PYTHON = (3, 12)


def run(command: list[str]) -> None:
    subprocess.run(command, check=True)


def install_requirements(requirements_file: Path) -> None:
    print(f"Installing dependencies from {requirements_file}")
    run([sys.executable, "-m", "pip", "install", "-r", str(requirements_file)])


def iter_requirement_files(root: Path) -> list[Path]:
    candidates = [root / "requirements.txt"]
    patterns = [
        "services/*/requirements.txt",
        "packages/*/requirements.txt",
    ]
    for pattern in patterns:
        candidates.extend(sorted(root.glob(pattern)))
    return [path for path in candidates if path.exists()]


def main() -> int:
    if sys.version_info[:2] < REQUIRED_PYTHON:
        required = ".".join(str(part) for part in REQUIRED_PYTHON)
        print(f"Python {required}+ is required, got {sys.version.split()[0]}")
        return 1

    repo_root = Path(__file__).resolve().parents[1]
    run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])

    requirement_files = iter_requirement_files(repo_root)
    if not requirement_files:
        print("No requirements files found. Nothing to install.")
        return 0

    for requirements_file in requirement_files:
        install_requirements(requirements_file)

    print("Monorepo bootstrap completed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
