import json
import sys
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path


ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / "src"))

from sp_morph_decoder import (  # noqa: E402
    MorphologyDecodeError,
    __version__,
    decode_tag,
    decodeTag,
)
from sp_morph_decoder.cli import main  # noqa: E402


class PackageApiTests(unittest.TestCase):
    def test_permissive_mode_returns_partial_result_and_errors(self):
        result = decode_tag("N-XYZ")

        self.assertEqual(result["Part of Speech"], "Noun")
        self.assertEqual(result["Case"], "Unknown")
        self.assertIn("Unknown case value", result["Errors"])

    def test_strict_mode_returns_valid_result(self):
        result = decode_tag("V-RAN-ATT", mode="strict")

        self.assertEqual(result["Mood"], "Infinitive")
        self.assertEqual(result["Verb Extra"], "Attic")
        self.assertNotIn("Errors", result)

    def test_strict_mode_raises_with_partial_result(self):
        with self.assertRaises(MorphologyDecodeError) as context:
            decode_tag("N-XYZ", mode="strict")

        error = context.exception
        self.assertEqual(error.tag, "N-XYZ")
        self.assertEqual(error.result["Part of Speech"], "Noun")
        self.assertIn("Unknown case value", error.errors)

    def test_strict_mode_rejects_unsupported_tag(self):
        with self.assertRaisesRegex(
            MorphologyDecodeError, "Unknown or unsupported morphology tag"
        ):
            decode_tag("UNKNOWN", mode="strict")

    def test_strict_mode_rejects_empty_tag(self):
        with self.assertRaises(MorphologyDecodeError):
            decode_tag("  ", mode="strict")

    def test_invalid_mode_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "mode must be"):
            decode_tag("N-NSF", mode="invalid")  # type: ignore[arg-type]

    def test_non_string_tag_is_rejected(self):
        with self.assertRaisesRegex(TypeError, "tag must be a string"):
            decode_tag(None)  # type: ignore[arg-type]

    def test_camel_case_alias_remains_compatible(self):
        self.assertEqual(decodeTag("N-NSF"), decode_tag("N-NSF"))

    def test_version_is_available(self):
        self.assertIsInstance(__version__, str)
        self.assertTrue(__version__)

    def test_every_known_morphology_tag_passes_strict_mode(self):
        tags = json.loads((ROOT / "testing" / "output" / "morph_tags.json").read_text())

        for tag in tags:
            with self.subTest(tag=tag):
                decode_tag(tag, mode="strict")


class CommandLineTests(unittest.TestCase):
    def test_cli_prints_decoded_json(self):
        stdout = StringIO()
        with redirect_stdout(stdout):
            exit_code = main(["V-PAI-3S", "--mode", "strict"])

        self.assertEqual(exit_code, 0)
        self.assertEqual(json.loads(stdout.getvalue())["Person"], "Third Person")

    def test_strict_cli_returns_nonzero_for_invalid_tag(self):
        stdout = StringIO()
        with redirect_stdout(stdout):
            exit_code = main(["N-XYZ", "--mode", "strict"])

        self.assertEqual(exit_code, 2)
        self.assertIn("Errors", json.loads(stdout.getvalue()))


if __name__ == "__main__":
    unittest.main()
