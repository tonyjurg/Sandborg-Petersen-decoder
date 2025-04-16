def decodeTag(tag):
    posMap = {
        "N-": "Noun",
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
        "N-PRI": "Proper Noun Indeclinable",
        "A-NUI": "Numeral Indeclinable",
        "N-LI": "Letter Indeclinable",
        "N-OI": "Noun Other Type Indeclinable",
        "PUNCT": "Punctuation"
    }

    caseMap = {
        "N": "Nominative",
        "V": "Vocative",
        "G": "Genitive",
        "D": "Dative",
        "A": "Accusative"
    }

    numberMap = {
        "S": "Singular",
        "P": "Plural"
    }

    genderMap = {
        "M": "Masculine",
        "F": "Feminine",
        "N": "Neuter"
    }

    tenseMap = {
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
        "X": "No Tense Stated"
    }

    voiceMap = {
        "A": "Active",
        "M": "Middle",
        "P": "Passive",
        "E": "Middle or Passive",
        "D": "Middle Deponent",
        "O": "Passive Deponent",
        "N": "Middle or Passive Deponent",
        "Q": "Impersonal Active",
        "X": "No Voice"
    }

    moodMap = {
        "I": "Indicative",
        "S": "Subjunctive",
        "O": "Optative",
        "M": "Imperative",
        "N": "Infinitive",
        "P": "Participle",
        "R": "Imperative Participle"
    }

    personMap = {
        "1": "First Person",
        "2": "Second Person",
        "3": "Third Person"
    }

    # Start decoding
    output = {}
    remainingTag = tag.strip()

    # Decode part of speech
    pos = next((key for key in posMap if remainingTag.startswith(key)), None)
    if pos:
        output["partOfSpeech"] = posMap[pos]
        remainingTag = remainingTag[len(pos):]
    else:
        output["partOfSpeech"] = "Unknown"
        return output

    # Further decoding
    if pos in ["N-", "A-", "T-"]:
        output["case"] = caseMap.get(remainingTag[0], "Unknown")
        output["number"] = numberMap.get(remainingTag[1], "Unknown")
        output["gender"] = genderMap.get(remainingTag[2], "Unknown")
    elif pos == "V-":
        output["tense"] = tenseMap.get(remainingTag[0], "Unknown")
        output["voice"] = voiceMap.get(remainingTag[1], "Unknown")
        output["mood"] = moodMap.get(remainingTag[2], "Unknown")
        if len(remainingTag) > 3:
            output["person"] = personMap.get(remainingTag[3], "Unknown")
            output["number"] = numberMap.get(remainingTag[4], "Unknown")

    return output


# Example usage:
tag = "V-PAI3S"  # Replace with any tag you want to decode
result = decodeTag(tag)
print(result)
