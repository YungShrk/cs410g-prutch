from langchain.document_loaders import GenericLoader
from langchain.parsers import LanguageParser
import os

def load_python_files(directory):
    """
    Load Python files from a specified directory.
    Args:
        directory (str): Path to the directory containing Python scripts.
    Returns:
        list: List of document objects.
    """
    loader = GenericLoader.from_filesystem(
        directory,
        glob="*",
        suffixes=[".py"],
        parser=LanguageParser()
    )
    docs = loader.load()
    return docs

if __name__ == "__main__":
    directory = "./sample_scripts"
    docs = load_python_files(directory)
    print(f"Loaded {len(docs)} Python files.")

