import sys
import os

import spacy
from spacy.matcher import Matcher

from custom_utils import read_file
from classifier import classify_utterance

if __name__ == "__main__":
    nlp = spacy.load("en_core_web_sm")

    if len(sys.argv) > 1:
        if not os.path.exists(sys.argv[1]):
            print(
                f"File {sys.argv[1]} does not exist. Using example-transcript.txt as default input file."
            )
            file = os.path.relpath("example-transcript.txt")
        else:
            print(f"Using input file: {sys.argv[1]}")
            file = os.path.relpath(sys.argv[1])
    else:
        print("Usage: python subtask1.py <filename>")
        print("Using example-transcript.txt as default input file.")
        file = os.path.relpath("example-transcript.txt")

    print(f"\nProcessing {file}...\n")
    content = read_file(file)
    print(f"Dialogue:\n{content}\n")
    doc = nlp(content)

    matcher = Matcher(nlp.vocab)

    proposal_patterns = [
        # Modal verb + action
        [
            {"POS": "VERB", "LEMMA": "think", "DEP": "ROOT", "OP": "?"},
            {"OP": "*"},
            {
                "POS": "AUX",
                "LEMMA": {"IN": ["should"]},
            },
            {"OP": "*"},
            {"POS": "VERB", "DEP": {"IN": ["xcomp", "ccomp", "ROOT"]}},
        ],
        # Suggest/recommend patterns
        [
            {"LEMMA": {"IN": ["suggest", "recommend", "propose", "advise"]}},
            {"OP": "*"},
            {"POS": "VERB", "DEP": {"IN": ["xcomp", "ccomp", "ROOT"]}, "OP": "?"},
        ],
        # Let's patterns
        [
            {"POS": "VERB", "LEMMA": "let", "DEP": "ROOT"},
            {"POS": "PRON", "LEMMA": r"'s"},
            {"POS": "VERB"},
        ],
        # What if pattern
        [{"LEMMA": "what"}, {"LEMMA": "if"}, {"OP": "*"}],
        # How about pattern
        [{"LEMMA": "how"}, {"LEMMA": "about"}, {"OP": "*"}],
    ]

    challenge_patterns = [
        [{"LEMMA": {"IN": ["disagree", "doubt", "question", "hesitant"]}}],
        # Don't think/believe/convince/sure/agree patterns
        [
            {"DEP": "neg"},
            {"OP": "*"},
            {
                "LEMMA": {"IN": ["think", "believe", "convince", "sure", "agree"]},
            },
        ],
    ]

    deferral_patterns = [
        # Wait until patterns
        [
            {"LEMMA": {"IN": ["defer", "postpone", "delay", "wait", "hold"]}},
            {"OP": "*"},
            {"LEMMA": "until"},
        ],
        # Before action pattern
        [{"LEMMA": "before"}, {"POS": "VERB"}],
    ]

    commitment_patterns = [
        [{"POS": "AUX", "LEMMA": {"IN": ["will", r"’ll"]}}],
    ]

    matcher.add("PROPOSAL", proposal_patterns)
    matcher.add("CHALLENGE", challenge_patterns)
    matcher.add("DEFERRAL", deferral_patterns)
    matcher.add("COMMITMENT", commitment_patterns)

    conversation = {}

    utterances = content.split("\n")
    if utterances[-1] == "":
        # Remove the last empty line if it exists
        utterances = utterances[:-1]

    for index, line in enumerate(utterances):
        speaker, utterance = line.split(":")
        speaker = speaker.strip()
        utterance = utterance.strip()
        conversation[index] = {
            "speaker": speaker,
            "utterance": utterance,
            "class": None,
        }

        prediction = classify_utterance(utterance, nlp, matcher, conversation, index)

        conversation[index]["class"] = prediction

    print("\nClassification Results:\n")
    previous_speaker = conversation[0]["speaker"]
    left_aligned = True
    for item in conversation.values():
        if item["speaker"] != previous_speaker:
            left_aligned = not left_aligned
            previous_speaker = item["speaker"]
        if left_aligned:
            print(f"{item['speaker']} -> {item['utterance']}".ljust(80))
            print(f"{item['class']}".ljust(80))
            print("----\n".ljust(80))
        else:
            print(f"{item['utterance']} <- {item['speaker']}".rjust(80))
            print(f"{item['class']}".rjust(80))
            print("----\n".rjust(80))
