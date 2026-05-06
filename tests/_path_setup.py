from __future__ import annotations

import sys
from pathlib import Path


def add_alignment_engine_src() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    candidates = [
        repo_root / "services" / "alignment-engine" / "src",
        repo_root / "src",
    ]
    for candidate in candidates:
        if candidate.exists():
            candidate_str = str(candidate)
            if candidate_str not in sys.path:
                sys.path.insert(0, candidate_str)
            return

