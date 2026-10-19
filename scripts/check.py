#!/usr/bin/env python3
"""Run every local quality gate in one command.

    python3 scripts/check.py

Equivalent to what CI runs: verify the generated homepage is current, then run
the content and site test suites.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STEPS = (
    ("build --check", [sys.executable, "scripts/build.py", "--check"]),
    ("unit tests", [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"]),
)


def main() -> int:
    for label, command in STEPS:
        print(f"\n== {label} ==", flush=True)
        result = subprocess.run(command, cwd=ROOT)
        if result.returncode != 0:
            print(f"\nFAILED: {label}", file=sys.stderr)
            return result.returncode
    print("\nAll checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
