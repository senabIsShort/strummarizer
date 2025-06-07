# Strummarizer

Author : Abdurrahman SEN
This is my submission for the coding task: Structuring and Summarising Dialogue Progression.

A `requirements.txt` file is provided to install necessary libraries (spaCy + LLM for subtask 2).

## Subtask 1 : Utterance classification

For this subtask, both the lexical attributes SpaCy recognizes and a simple ruleset were used to classify utterances.

### How to run

At the root of the project, simply run the `subtask1.py` script.
You can provide a filename as an argument to the command, or keep it blank to use the `example-transcript.txt` by default.

### Rules

The first four label use SpaCy's matcher to recognize patterns that I deemed could fit the label description. Patterns are described using lemmas, part-of-speech tags etc.
Despite trying to be as generalizable as possible, this approach is completely reliant on the developer's knowledge of sentence structure and interpretation of dialogue flow. Trying to keep it lightweight is also a limiting factor in how expressive the rules can be made.

- Proposal – suggesting an action or idea
  - Sentence includes "think \* should \* VERB", or keywords "suggest/propose"
- Challenge – questioning or pushing back on a statement
  - Speaker change -> Sentence includes negation
- Deferral – delaying a decision or action
  - "until" "wait" "hold off"
- Commitment – agreement to take a future action
  - Future tense (using "will" auxiliary as a marker)
- Justification – supporting a claim with reasoning
  - Either response to Challenge or follow-up utterance after a Proposal
- Query – requesting clarification or further info
  - Question mark


