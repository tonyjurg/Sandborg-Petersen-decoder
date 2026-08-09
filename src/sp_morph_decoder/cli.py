"""Command-line interface for the Sandborg-Petersen decoder."""

import argparse
import json
import sys
from typing import List, Optional

from .decoder import MorphologyDecodeError, decode_tag


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sp-morph-decode",
        description="Decode a Sandborg-Petersen morphology tag.",
    )
    parser.add_argument("tag", help="Morphology tag, for example V-PAI-3S")
    parser.add_argument(
        "--mode",
        choices=("permissive", "strict"),
        default="permissive",
        help="Return partial results or fail on invalid input (default: permissive).",
    )
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        result = decode_tag(args.tag, mode=args.mode)
    except MorphologyDecodeError as error:
        print(json.dumps(error.result, indent=2, ensure_ascii=False))
        return 2

    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
