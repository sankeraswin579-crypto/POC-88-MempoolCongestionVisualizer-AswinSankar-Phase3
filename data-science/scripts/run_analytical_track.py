from __future__ import annotations

import subprocess
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Project paths
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

TRACK_SCRIPT = (
    PROJECT_ROOT
    / "data-science"
    / "scripts"
    / "track-specific"
    / "comparative_track.py"
)


# ---------------------------------------------------------------------------
# Main analytical-track runner
# ---------------------------------------------------------------------------

def main() -> None:
    """
    Run the approved Phase 3 Track A — Comparative analysis.

    Pipeline:
        canonical intelligence_data.csv
                    ↓
        comparative_track.py
                    ↓
        comparative_track_raw.json

    The runner does not perform the analysis itself.
    It executes the dedicated comparative analytical script.
    """

    print("=" * 70)
    print(
        "POC-88 Phase 3 — Track A: Comparative Analytical Track"
    )
    print("=" * 70)

    print(
        f"Project root:\n{PROJECT_ROOT}"
    )

    print(
        f"\nComparative track script:\n{TRACK_SCRIPT}"
    )

    print("-" * 70)

    # -----------------------------------------------------------------------
    # Verify analytical script exists
    # -----------------------------------------------------------------------

    if not TRACK_SCRIPT.exists():
        raise FileNotFoundError(
            "Comparative analytical track script not found:\n"
            f"{TRACK_SCRIPT}\n\n"
            "Expected file:\n"
            "data-science/scripts/track-specific/"
            "comparative_track.py"
        )

    # -----------------------------------------------------------------------
    # Execute Track A
    # -----------------------------------------------------------------------

    print(
        "\nStarting Track A — Comparative analysis..."
    )

    result = subprocess.run(
        [
            sys.executable,
            str(TRACK_SCRIPT),
        ],
        cwd=PROJECT_ROOT,
        check=False,
    )

    # -----------------------------------------------------------------------
    # Handle failure
    # -----------------------------------------------------------------------

    if result.returncode != 0:
        print("-" * 70)
        print(
            "Track A — Comparative analytical track FAILED."
        )
        print(
            f"Exit code: {result.returncode}"
        )
        print("-" * 70)

        raise SystemExit(
            result.returncode
        )

    # -----------------------------------------------------------------------
    # Success
    # -----------------------------------------------------------------------

    print("-" * 70)
    print(
        "Track A — Comparative analytical track "
        "completed successfully."
    )

    print(
        "\nPrimary analytical direction:"
        "\n  Track A — Comparative"
    )

    print(
        "\nExpected analytical output:"
        "\n  data-science/outputs/"
        "comparative_track_raw.json"
    )

    print("=" * 70)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    main()