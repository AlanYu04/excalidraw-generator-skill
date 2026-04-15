#!/usr/bin/env python3
"""
CI script for excalidraw-showcase project.

Runs golden rules checks + project-specific tests.
Exit 0 = all pass, Exit 1 = failures.

Usage:
    python scripts/run_ci.py
"""
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = Path(__file__).resolve().parent
PLANS_DIR = PROJECT_ROOT / ".plans" / "excalidraw-showcase"

# Source directories to check
SRC_DIRS = ["src", "."]

# Docs directory for freshness checks
DOCS_DIR = str(PLANS_DIR / "docs") if PLANS_DIR.exists() else None


def run_golden_rules():
    """Run golden rules checks."""
    print("Running Golden Rules...")
    from golden_rules import check_all

    src_paths = [str(PROJECT_ROOT / d) for d in SRC_DIRS]
    fails, warns, infos = check_all(src_paths, docs_dir=DOCS_DIR)
    return fails


def run_tests():
    """Run project tests. Add test commands as the project grows."""
    print("\nRunning tests...")
    # TODO: Add test commands as the project grows
    # Example: subprocess.run(["npm", "test"], check=True)
    print("  [SKIP] No tests configured yet.\n")
    return 0


def main():
    print("=" * 60)
    print("CI Pipeline: excalidraw-showcase")
    print("=" * 60 + "\n")

    total_fails = 0

    # Step 1: Golden rules
    total_fails += run_golden_rules()

    # Step 2: Tests
    total_fails += run_tests()

    print("=" * 60)
    if total_fails > 0:
        print(f"CI Result: FAILED ({total_fails} failures)")
        sys.exit(1)
    else:
        print("CI Result: PASSED")
        sys.exit(0)


if __name__ == "__main__":
    main()
