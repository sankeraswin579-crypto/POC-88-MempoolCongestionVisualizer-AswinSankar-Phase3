from __future__ import annotations

import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

TRACK_SCRIPT = (
    PROJECT_ROOT
    / "data-science"
    / "scripts"
    / "track-specific"
    / "temporal_track.py"
)


def main() -> None:
    print("Running POC-88 Phase 3 analytical track...")
    print(f"Track script: {TRACK_SCRIPT}")

    if not TRACK_SCRIPT.exists():
        raise FileNotFoundError(
            f"Temporal track script not found: {TRACK_SCRIPT}"
        )

    result = subprocess.run(
        [sys.executable, str(TRACK_SCRIPT)],
        cwd=PROJECT_ROOT,
        check=False,
    )

    if result.returncode != 0:
        raise SystemExit(
            f"Analytical track failed with exit code "
            f"{result.returncode}."
        )

    print("Analytical track completed successfully.")


if __name__ == "__main__":
    main()