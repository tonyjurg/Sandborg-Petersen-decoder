"""Compatibility entry point for the installable ``sp_morph_decoder`` package."""

import json
import sys
from pathlib import Path


source_directory = Path(__file__).parents[1] / "src"
if source_directory.is_dir():
    # Prefer the adjacent source tree when this file runs from a checkout.
    sys.path.insert(0, str(source_directory))

from sp_morph_decoder import MorphologyDecodeError, decode_tag, decodeTag


__all__ = ["MorphologyDecodeError", "decode_tag", "decodeTag"]


if __name__ == "__main__":
    print(json.dumps(decode_tag("N-NSF"), indent=2))
