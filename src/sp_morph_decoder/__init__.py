"""Public API for the Sandborg-Petersen morphology decoder."""

from importlib.metadata import PackageNotFoundError, version

from .decoder import (
    DecodeMode,
    DecodeResult,
    MorphologyDecodeError,
    decode_tag,
    decodeTag,
)

try:
    from ._version import __version__
except ImportError:
    try:
        __version__ = version("sandborg-petersen-decoder")
    except PackageNotFoundError:
        __version__ = "0+unknown"

__all__ = [
    "DecodeMode",
    "DecodeResult",
    "MorphologyDecodeError",
    "__version__",
    "decode_tag",
    "decodeTag",
]
