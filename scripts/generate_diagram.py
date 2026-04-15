#!/usr/bin/env python3
"""Stable entrypoint for DiagramSpec-driven generation."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.pipeline import generate_diagram, save_generated_diagram


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate an Excalidraw diagram from DiagramSpec JSON.")
    parser.add_argument("spec", help="Path to the DiagramSpec JSON file.")
    parser.add_argument("output", help="Output path (.excalidraw or .excalidraw.md).")
    parser.add_argument("--artifacts", help="Optional directory for pipeline artifacts.", default=None)
    parser.add_argument("--no-repair", action="store_true", help="Disable automatic repair pass.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    with open(args.spec, "r", encoding="utf-8") as f:
        spec = json.load(f)

    result = generate_diagram(spec, auto_repair=not args.no_repair)
    if result.final_status != "PASS":
        print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
        return 1

    save_generated_diagram(args.output, result, artifact_dir=args.artifacts)
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
