import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "python" / "SP-Morph-decode.py"
SPEC = importlib.util.spec_from_file_location("sp_morph_decode", MODULE_PATH)
DECODER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(DECODER)


class DecodeTagTests(unittest.TestCase):
    def test_personal_pronoun_with_person(self):
        self.assertEqual(
            DECODER.decodeTag("P-1NS"),
            {
                "Part of Speech": "Personal Pronoun",
                "Person": "First Person",
                "Case": "Nominative",
                "Number": "Singular",
            },
        )

    def test_relative_pronoun_without_person(self):
        self.assertEqual(
            DECODER.decodeTag("R-NSM"),
            {
                "Part of Speech": "Relative Pronoun",
                "Case": "Nominative",
                "Number": "Singular",
                "Gender": "Masculine",
            },
        )

    def test_rejects_incomplete_noun(self):
        result = DECODER.decodeTag("N-")
        self.assertIn("Errors", result)
        self.assertIn("Invalid or incomplete noun tag structure", result["Errors"])

    def test_rejects_unknown_noun_features(self):
        result = DECODER.decodeTag("N-XYZ")
        self.assertIn("Errors", result)
        self.assertIn("Unknown case value", result["Errors"])

    def test_rejects_trailing_garbage(self):
        result = DECODER.decodeTag("N-NSF-GARBAGE")
        self.assertIn("Errors", result)
        self.assertIn("Invalid or incomplete noun tag structure", result["Errors"])

    def test_decodes_finite_verb_extra(self):
        result = DECODER.decodeTag("V-PAI-3S-M")
        self.assertEqual(result["Verb Extra"], "Middle significance")
        self.assertNotIn("Suffix", result)

    def test_uses_verb_context_for_contracted_form(self):
        result = DECODER.decodeTag("V-PAI-3S-C")
        self.assertEqual(result["Verb Extra"], "Contracted form")
        self.assertNotIn("Suffix", result)

    def test_decodes_infinitive_extra_without_person(self):
        result = DECODER.decodeTag("V-RAN-ATT")
        self.assertEqual(result["Verb Extra"], "Attic")
        self.assertNotIn("Person", result)
        self.assertNotIn("Number", result)
        self.assertNotIn("Errors", result)


if __name__ == "__main__":
    unittest.main()
