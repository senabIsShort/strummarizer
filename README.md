# Strummarizer

Author : Abdurrahman SEN  
This is my submission for the coding task: Structuring and Summarising Dialogue Progression.  

A `requirements.txt` file is provided to install necessary libraries (spaCy + Ollama).  

Each subtasks is treated independently, with the output printed in the terminal.  

## How to run

At the root of the project, simply run the `subtask1.py` or `subtask2.py` script.
You can provide a filename as an argument to the command, or keep it blank to use the `example-transcript.txt` by default.  

## Subtask 1 : Utterance classification

For this subtask, both the lexical attributes SpaCy recognizes and a simple ruleset were used to classify utterances.
I attempted to recreate a messaging style output between two speakers by alternatively aligning utterances left and right. The label follows on a new line.

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

## Subtask 2 : LLM-based summarization

For this subtask, I decided against using an OpenAI API endpoint simply due to potential incurred costs. Instead I use Ollama, it has the drawbacks of needing a bit of time and space to download models locally.  

### Prerequisites

If it isn't installed yet, install Ollama using `curl -fsSL https://ollama.com/install.sh | sh`.  
Afterwards, either use the `requirements.txt` or install the python ollama package using `pip install ollama`.  

Please pull the `llama3.2:3b` model on your machine using `ollama pull llama3.2:3b` in a terminal (requires around 2GB of space).  
Afterwards, you may run `python subtask2.py` to generate a summary.

### Approach used

This subtask can essentially be solved using prompt engineering. By assigning a role to the model at the beginning of the prompt, we contextualize the task.  
Testing was satisfying enough to not require few-shot prompting.  
