import os


def read_file(path: os.path) -> str:
    """Reads the content of a text file and returns it as a string.

    Args:
        path (os.path): Path to the text file to read.

    Returns:
        str: The content of the text file as a string.
    """
    with open(path, "r") as f:
        content = f.read()
    return content
