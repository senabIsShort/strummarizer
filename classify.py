from spacy.matcher import Matcher
from spacy.language import Language


def classify_utterance(
    utterance: str,
    nlp: Language,
    matcher: Matcher,
    conversation_history: dict,
    utterance_index: int,
) -> str:
    """Classifies an utterance based on Matcher patterns and other rules.

    Args:
        utterance (str): The utterance to classify.
        nlp (Language): The SpaCy language model used for processing the utterance.
        matcher (Matcher): The SpaCy Matcher object used to find patterns in the utterance. By default, matches the PROPOSAL, CHALLENGE, DEFERRAL, COMMITMENT classes.
        conversation_history (dict): A dictionary containing previous utterances and their classifications.
        utterance_index (int): The index of the current utterance in the conversation.

    Returns:
        str: The predicted class of the utterance, which can be one of:
            - "PROPOSAL"
            - "CHALLENGE"
            - "DEFERRAL"
            - "COMMITMENT"
            - "JUSTIFICATION"
            - "QUERY"
            - "OTHER"
    """
    # Use SpaCy to process the utterance and maybe find matches
    doc = nlp(utterance)
    matches = matcher(doc)

    predicted_class = None

    for match_id, start, end in matches:
        span = doc[start:end]
        # print(f"Match found: {span.text} (Rule : {nlp.vocab.strings[match_id]})")
        predicted_class = nlp.vocab.strings[match_id]

    if utterance_index == 0:
        return predicted_class if predicted_class else "OTHER"


    # Use rules based on previous utterance classifications
    prev_class = conversation_history[utterance_index - 1]["class"]
    prev_speaker = conversation_history[utterance_index - 1]["speaker"]
    curr_class = predicted_class
    curr_speaker = conversation_history[utterance_index]["speaker"]

    if (
        (prev_class == "CHALLENGE" and prev_speaker != curr_speaker)
        or (prev_class == "PROPOSAL" and prev_speaker == curr_speaker)
        and curr_class is None
    ):
        predicted_class = "JUSTIFICATION"
    elif curr_class is None and utterance.endswith("?"):
        predicted_class = "QUERY"
    elif curr_class is None:
        predicted_class = "OTHER"

    return predicted_class
