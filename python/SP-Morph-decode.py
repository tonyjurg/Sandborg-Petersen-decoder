# Main Part of Speech mapping
posMap = {
    "N-PRI": "Proper Noun Indeclinable",  # first the subset since decoding is based on 'first match'
    "N-LI": "Letter Indeclinable",
    "N-OI": "Noun Other Type Indeclinable",
    "N-": "Noun",  # generic Noun
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
    "PUNCT": "Punctuation"
}

# grammatical case mapping
caseMap = {
    "V": "Vocative",
    "N": "Nominative",
    "G": "Genitive",
    "D": "Dative",
    "A": "Accusative"
}

# grammatical number mapping
numberMap = {
    "S": "Singular",
    "P": "Plural"
}

# grammatical gender mapping
genderMap = {
    "M": "Masculine",
    "F": "Feminine",
    "N": "Neuter"
}

# verb tense mapping
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

# verb voice mapping
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

# verb mode mapping
moodMap = {
    "I": "Indicative",
    "S": "Subjunctive",
    "O": "Optative",
    "M": "Imperative",
    "N": "Infinitive",
    "P": "Participle",
    "R": "Imperative Participle"
}

# grammatical person mapping
personMap = {
    "1": "First Person",
    "2": "Second Person",
    "3": "Third Person"
}

# Extra verb info mapping
verbExtraMap = {
    "-M": "Middle significance",
    "-C": "Contracted form",
    "-T": "Transitive",
    "-A": "Aeolic",
    "-ATT": "Attic",
    "-AP": "Apocopated form",
    "-IRR": "Irregular or impure form"
}

# suffix mapping
suffixMap = {
    "-K": "Crasis",
    "-N": "Negative",
    "-S": "Superlative",
    "-C": "Comparative",
    "-ABB": "Abbreviated",
    "-I": "Interrogative",
    "-ATT": "Attic",
    "-P": "Particle Attached"
}


def decodeTag(tagInput):
    input_str = tagInput.strip().upper()
    output = {}

    if not input_str:
        output["Error"] = "Please enter a parsing tag."
        return output

    # Decode part of speech
    # The first line retrieve an array of all the keys from posMap.
    # We will iterating and find the first matching key.
    pos = None
    for key in posMap.keys():
        if input_str.startswith(key):
            pos = key
            break

    if pos is not None:
        output["Part of Speech"] = posMap[pos]
        input_str = input_str[len(pos):]
    else:
        output["Part of Speech"] = "Unknown or Unsupported"
        return output

    # Further decoding based on the detected part of speech
    if pos in ["N-", "A-", "T-"] and len(input_str) >= 3:
        output["Case"] = caseMap.get(input_str[0], "Unknown")
        output["Number"] = numberMap.get(input_str[1], "Unknown")
        output["Gender"] = genderMap.get(input_str[2], "Unknown")

    # Verbs
    elif pos == "V-":
        # Split the remaining tag into parts
        parts = input_str.split('-')

        # Analyze Tense, Voice, Mood from the first part
        if len(parts) > 0:
            firstPart = parts[0]
            tenseKey = None
            for tk in tenseMap.keys():
                if firstPart.startswith(tk):
                    tenseKey = tk
                    break

            if tenseKey is not None:
                output["Tense"] = tenseMap[tenseKey]
                remaining = firstPart[len(tenseKey):]
                if len(remaining) >= 2:
                    output["Voice"] = voiceMap.get(remaining[0], "Unknown")
                    output["Mood"] = moodMap.get(remaining[1], "Unknown")
            else:
                output["Tense"] = "Unknown"

        # Analyze Person/Number or Case/Number/Gender for the second part
        if len(parts) > 1:
            secondPart = parts[1]
            if output.get("Mood") == "Participle" and len(secondPart) >= 3:
                output["Case"] = caseMap.get(secondPart[0], "Unknown")
                output["Number"] = numberMap.get(secondPart[1], "Unknown")
                output["Gender"] = genderMap.get(secondPart[2], "Unknown")
            elif len(secondPart) >= 2:
                output["Person"] = personMap.get(secondPart[0], "Unknown")
                output["Number"] = numberMap.get(secondPart[1], "Unknown")

        # Analyze verb extra info or suffix in the third part
        if len(parts) > 2:
            thirdPart = parts[2]
            extraKey = None
            for vk in verbExtraMap.keys():
                if vk in thirdPart:
                    extraKey = vk
                    break
            if extraKey:
                output["Verb Extra"] = verbExtraMap[extraKey]
            else:
                output["Suffix"] = suffixMap.get(thirdPart, "Unknown")

    # Reflexive Pronoun
    elif pos in ["F-"]:
        if len(input_str) >= 4:
            output["Person"] = personMap.get(input_str[0], "Unknown")
            output["Case"] = caseMap.get(input_str[1], "Unknown")
            output["Number"] = numberMap.get(input_str[2], "Unknown")
            output["Gender"] = genderMap.get(input_str[3], "Unknown")

    # Possessive Pronoun
    elif pos == "S-" and len(input_str) >= 5:
        output["Person of Possessor"] = personMap.get(input_str[0], "Unknown")
        output["Number of Possessor"] = numberMap.get(input_str[1], "Unknown")
        output["Case of Possessed"] = caseMap.get(input_str[2], "Unknown")
        output["Number of Possessed"] = numberMap.get(input_str[3], "Unknown")
        output["Gender of Possessed"] = genderMap.get(input_str[4], "Unknown")

    elif pos in ["P-", "R-", "C-", "D-", "K-", "I-", "X-", "Q-", "S-"]:
        # Pattern 1: [person, case, number]
        if len(input_str) >= 3 and re.match(r'^[123]$', input_str[0]):
            output["Person"] = personMap.get(input_str[0], "Unknown")
            output["Case"]   = caseMap.get(input_str[1], "Unknown")
            output["Number"] = numberMap.get(input_str[2], "Unknown")
    
        # Pattern 2: [case, number, gender]
        elif len(input_str) >= 3:
            output["Case"]   = caseMap.get(input_str[0], "Unknown")
            output["Number"] = numberMap.get(input_str[1], "Unknown")
            output["Gender"] = genderMap.get(input_str[2], "Unknown")

    # Decode suffix if present
    for suf in suffixMap.keys():
        if input_str.endswith(suf):
            output["Suffix"] = suffixMap[suf]
            break

    return output


# Example usage:
result = decodeTag("N-PRS")
print(result)
