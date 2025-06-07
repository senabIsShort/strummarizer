import os
import sys

import ollama

from custom_utils import read_file

if __name__ == "__main__":

    if len(sys.argv) > 1:
        if not os.path.exists(sys.argv[1]):
            print(f"File {sys.argv[1]} does not exist. Using example-transcript.txt as default input file.")
            file = os.path.relpath("example-transcript.txt")
        else:
            print(f"Using input file: {sys.argv[1]}")
            file = os.path.relpath(sys.argv[1])
    else:
        print("Usage: python subtask2.py <filename>")
        print("Using example-transcript.txt as default input file.")
        file = os.path.relpath("example-transcript.txt")

    dialogue = read_file(file)

    model_name = "llama3.2:3b"

    # Construct the prompt
    prompt = f"""You are a conversation analyst.
Given the following dialogue, generate a **structured summary paragraph** that outlines the flow of the conversation. Respond only with the structured summary paragraph, without any additional text or explanation.

Dialogue:
{dialogue}

Structured Summary:
"""

    # Pull the model (only if not already present)
    print(f"Ensuring model '{model_name}' is available locally...")
    ollama.pull(model_name)

    print(f"\nQuerying model '{model_name}' with the following prompt:\n\n{prompt}\n")
    response = ollama.chat(
        model=model_name,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    # Stream the response
    for chunk in ollama.chat(
    model=model_name,
    messages=[{"role": "user", "content": prompt}],
    stream=True
    ):
        print(chunk['message']['content'], end='', flush=True)
    print()
