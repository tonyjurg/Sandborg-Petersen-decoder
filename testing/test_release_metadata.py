import importlib.util
import unittest
from datetime import date
from pathlib import Path


ROOT = Path(__file__).parents[1]
MODULE_PATH = ROOT / "scripts" / "validate_release.py"
SPEC = importlib.util.spec_from_file_location("validate_release", MODULE_PATH)
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


class ReleaseMetadataTests(unittest.TestCase):
    def test_current_citation_matches_current_version(self):
        self.assertEqual(
            VALIDATOR.validate_release(
                ROOT / "CITATION.cff", tag="v1.1", today=date(2026, 8, 9)
            ),
            [],
        )

    def test_rejects_tag_mismatch(self):
        errors = VALIDATOR.validation_errors(
            {"version": "v1.2", "date-released": "2026-08-09"},
            tag="v1.3",
            today=date(2026, 8, 9),
        )
        self.assertIn(
            "CITATION.cff version 'v1.2' does not match release tag 'v1.3'",
            errors,
        )

    def test_rejects_invalid_version_and_future_date(self):
        errors = VALIDATOR.validation_errors(
            {"version": "release-2", "date-released": "2026-08-10"},
            today=date(2026, 8, 9),
        )
        self.assertIn(
            "CITATION.cff version must use vMAJOR.MINOR or vMAJOR.MINOR.PATCH",
            errors,
        )
        self.assertIn("CITATION.cff date-released cannot be in the future", errors)

    def test_rejects_missing_fields(self):
        errors = VALIDATOR.validation_errors({})
        self.assertEqual(
            errors,
            ["Missing CITATION.cff field(s): version, date-released"],
        )


if __name__ == "__main__":
    unittest.main()
