"""Decode Sandborg-Petersen morphology tags."""

import re
from typing import Dict, List, Literal, Tuple, Union


DecodeMode = Literal["permissive", "strict"]
DecodeValue = Union[str, List[str]]
DecodeResult = Dict[str, DecodeValue]


POS_MAP = {
    "N-PRI": "Proper Noun Indeclinable",
    "N-LI": "Letter Indeclinable",
    "N-OI": "Noun Other Type Indeclinable",
    "N-": "Noun",
    "A-NUI": "Numeral Indeclinable",
    "A-": "Adjective",
    "T-": "Article",
    "V-": "Verb",
    "P-": "Personal Pronoun",
    "R-": "Relative Pronoun",
    "C-": "Reciprocal Pronoun",
    "D-": "Demonstrative Pronoun",
    "K-": "Correlative Pronoun",
    "I-": "Interrogative Pronoun",
    "X-": "Indefinite Pronoun",
    "Q-": "Correlative/Interrogative Pronoun",
    "F-": "Reflexive Pronoun",
    "S-": "Possessive Pronoun",
    "ADV": "Adverb",
    "CONJ": "Conjunction",
    "COND": "Conditional",
    "PRT": "Particle",
    "PREP": "Preposition",
    "INJ": "Interjection",
    "ARAM": "Aramaic",
    "HEB": "Hebrew",
    "PUNCT": "Punctuation",
}

CASE_MAP = {
    "V": "Vocative",
    "N": "Nominative",
    "G": "Genitive",
    "D": "Dative",
    "A": "Accusative",
}

NUMBER_MAP = {"S": "Singular", "P": "Plural", "D": "Dual"}
GENDER_MAP = {"M": "Masculine", "F": "Feminine", "N": "Neuter"}

TENSE_MAP = {
    "P": "Present",
    "I": "Imperfect",
    "F": "Future",
    "2F": "Second Future",
    "A": "Aorist",
    "2A": "Second Aorist",
    "R": "Perfect",
    "2R": "Second Perfect",
    "L": "Pluperfect",
    "2L": "Second Pluperfect",
    "X": "No Tense Stated",
}

VOICE_MAP = {
    "A": "Active",
    "M": "Middle",
    "P": "Passive",
    "E": "Middle or Passive",
    "D": "Middle Deponent",
    "O": "Passive Deponent",
    "N": "Middle or Passive Deponent",
    "Q": "Impersonal Active",
    "X": "No Voice",
}

MOOD_MAP = {
    "I": "Indicative",
    "S": "Subjunctive",
    "O": "Optative",
    "M": "Imperative",
    "N": "Infinitive",
    "P": "Participle",
    "R": "Imperative Participle",
}

PERSON_MAP = {"1": "First Person", "2": "Second Person", "3": "Third Person"}

VERB_EXTRA_MAP = {
    "-M": "Middle significance",
    "-C": "Contracted form",
    "-T": "Transitive",
    "-A": "Aeolic",
    "-ATT": "Attic",
    "-AP": "Apocopated form",
    "-IRR": "Irregular or impure form",
}

SUFFIX_MAP = {
    "-K": "Crasis",
    "-N": "Negative",
    "-S": "Superlative",
    "-C": "Comparative",
    "-ABB": "Abbreviated",
    "-I": "Interrogative",
    "-ATT": "Attic",
    "-P": "Particle Attached",
}


class MorphologyDecodeError(ValueError):
    """Raised when strict decoding encounters an invalid morphology tag."""

    def __init__(self, tag: str, errors: List[str], result: DecodeResult) -> None:
        self.tag = tag
        self.errors = tuple(errors)
        self.result = result
        details = "; ".join(errors)
        super().__init__(f"Could not decode {tag!r}: {details}")


def _decode_permissively(tag: str) -> DecodeResult:
    input_str = tag.strip().upper()
    output: DecodeResult = {}

    if not input_str:
        output["Error"] = "Please enter a parsing tag."
        return output

    pos = next((key for key in POS_MAP if input_str.startswith(key)), None)
    if pos is None:
        output["Part of Speech"] = "Unknown or Unsupported"
        return output

    output["Part of Speech"] = POS_MAP[pos]
    input_str = input_str[len(pos) :]

    if pos in ["N-", "A-", "T-"] and len(input_str) >= 3:
        output["Case"] = CASE_MAP.get(input_str[0], "Unknown")
        output["Number"] = NUMBER_MAP.get(input_str[1], "Unknown")
        output["Gender"] = GENDER_MAP.get(input_str[2], "Unknown")

    elif pos == "V-":
        parts = input_str.split("-")
        first_part = parts[0]
        tense_key = next(
            (key for key in TENSE_MAP if first_part.startswith(key)), None
        )

        if tense_key is not None:
            output["Tense"] = TENSE_MAP[tense_key]
            remaining = first_part[len(tense_key) :]
            if len(remaining) >= 2:
                output["Voice"] = VOICE_MAP.get(remaining[0], "Unknown")
                output["Mood"] = MOOD_MAP.get(remaining[1], "Unknown")
        else:
            output["Tense"] = "Unknown"

        if len(parts) > 1 and output.get("Mood") != "Infinitive":
            second_part = parts[1]
            if output.get("Mood") == "Participle" and len(second_part) >= 3:
                output["Case"] = CASE_MAP.get(second_part[0], "Unknown")
                output["Number"] = NUMBER_MAP.get(second_part[1], "Unknown")
                output["Gender"] = GENDER_MAP.get(second_part[2], "Unknown")
            elif len(second_part) >= 2:
                output["Person"] = PERSON_MAP.get(second_part[0], "Unknown")
                output["Number"] = NUMBER_MAP.get(second_part[1], "Unknown")

        modifier_index = 1 if output.get("Mood") == "Infinitive" else 2
        if len(parts) > modifier_index:
            modifier = f"-{parts[modifier_index]}"
            if modifier in VERB_EXTRA_MAP:
                output["Verb Extra"] = VERB_EXTRA_MAP[modifier]
            else:
                output["Suffix"] = SUFFIX_MAP.get(modifier, "Unknown")

    elif pos == "F-" and len(input_str) >= 4:
        output["Person"] = PERSON_MAP.get(input_str[0], "Unknown")
        output["Case"] = CASE_MAP.get(input_str[1], "Unknown")
        output["Number"] = NUMBER_MAP.get(input_str[2], "Unknown")
        output["Gender"] = GENDER_MAP.get(input_str[3], "Unknown")

    elif pos == "S-" and len(input_str) >= 5:
        output["Person of Possessor"] = PERSON_MAP.get(input_str[0], "Unknown")
        output["Number of Possessor"] = NUMBER_MAP.get(input_str[1], "Unknown")
        output["Case of Possessed"] = CASE_MAP.get(input_str[2], "Unknown")
        output["Number of Possessed"] = NUMBER_MAP.get(input_str[3], "Unknown")
        output["Gender of Possessed"] = GENDER_MAP.get(input_str[4], "Unknown")

    elif pos in ["P-", "R-", "C-", "D-", "K-", "I-", "X-", "Q-", "S-"]:
        if len(input_str) >= 3 and input_str[0] in PERSON_MAP:
            output["Person"] = PERSON_MAP.get(input_str[0], "Unknown")
            output["Case"] = CASE_MAP.get(input_str[1], "Unknown")
            output["Number"] = NUMBER_MAP.get(input_str[2], "Unknown")
        elif len(input_str) >= 3:
            output["Case"] = CASE_MAP.get(input_str[0], "Unknown")
            output["Number"] = NUMBER_MAP.get(input_str[1], "Unknown")
            output["Gender"] = GENDER_MAP.get(input_str[2], "Unknown")

    suffix = next((value for value in SUFFIX_MAP if input_str.endswith(value)), None)
    if suffix and "Verb Extra" not in output:
        output["Suffix"] = SUFFIX_MAP[suffix]

    errors = [
        f"Unknown {field.lower()} value"
        for field, value in output.items()
        if value == "Unknown"
    ]

    suffix_pattern = r"(?:-(?:K|N|S|C|ABB|I|ATT|P))?"
    verb_tense_pattern = r"(?:2F|2A|2R|2L|P|I|F|A|R|L|X)"
    verb_voice_pattern = r"[AMPEDONQX]"
    verb_modifier_pattern = r"(?:-(?:M|C|T|A|ATT|AP|IRR|K|N|S|ABB|I|P))?"
    verb_pattern = (
        rf"{verb_tense_pattern}{verb_voice_pattern}"
        rf"(?:[ISOMR]-[123][SPD]|N|P-[VNGDA][SPD][MFN])"
        rf"{verb_modifier_pattern}"
    )
    expected_patterns = {
        "N-": rf"[VNGDA][SPD][MFN]{suffix_pattern}",
        "A-": rf"[VNGDA][SPD][MFN]{suffix_pattern}",
        "T-": rf"[VNGDA][SPD][MFN]{suffix_pattern}",
        "F-": rf"[123][VNGDA][SPD][MFN]{suffix_pattern}",
    }

    if pos in expected_patterns and not re.fullmatch(expected_patterns[pos], input_str):
        errors.append(f"Invalid or incomplete {POS_MAP[pos].lower()} tag structure")
    elif pos == "V-" and not re.fullmatch(verb_pattern, input_str):
        errors.append("Invalid or incomplete verb tag structure")
    elif pos == "S-" and not re.fullmatch(
        rf"(?:[123][SPD][VNGDA][SPD][MFN]|[VNGDA][SPD][MFN]){suffix_pattern}",
        input_str,
    ):
        errors.append("Invalid or incomplete possessive pronoun tag structure")
    elif pos in ["P-", "R-", "C-", "D-", "K-", "I-", "X-", "Q-"] and not re.fullmatch(
        rf"(?:[123][VNGDA][SPD]|[VNGDA][SPD][MFN]){suffix_pattern}",
        input_str,
    ):
        errors.append(f"Invalid or incomplete {POS_MAP[pos].lower()} tag structure")

    if errors:
        output["Errors"] = list(dict.fromkeys(errors))

    return output


def _strict_errors(result: DecodeResult) -> List[str]:
    errors: List[str] = []
    embedded = result.get("Errors")
    if isinstance(embedded, list):
        errors.extend(embedded)

    single_error = result.get("Error")
    if isinstance(single_error, str):
        errors.append(single_error)

    if result.get("Part of Speech") == "Unknown or Unsupported":
        errors.append("Unknown or unsupported morphology tag")

    return list(dict.fromkeys(errors))


def decode_tag(tag: str, *, mode: DecodeMode = "permissive") -> DecodeResult:
    """Decode a Sandborg-Petersen morphology tag.

    In ``permissive`` mode, the decoder returns all recoverable fields and places
    validation messages in ``Errors``. In ``strict`` mode, the same partial
    result is attached to :class:`MorphologyDecodeError` and the exception is
    raised whenever the tag cannot be decoded cleanly.
    """

    if not isinstance(tag, str):
        raise TypeError("tag must be a string")
    if mode not in ("permissive", "strict"):
        raise ValueError("mode must be 'permissive' or 'strict'")

    result = _decode_permissively(tag)
    errors = _strict_errors(result)
    if mode == "strict" and errors:
        raise MorphologyDecodeError(tag, errors, result)
    return result


def decodeTag(tagInput: str, *, mode: DecodeMode = "permissive") -> DecodeResult:
    """Backward-compatible alias for :func:`decode_tag`."""

    return decode_tag(tagInput, mode=mode)
