from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings  # Google Generative AI wrapper for LLM and embeddings
from langchain.text_splitter import TokenTextSplitter  # Alternative text splitter for handling documents
from langchain_chroma import Chroma  # Updated import path for Chroma vector storage
from langchain_core.output_parsers import StrOutputParser  # Output parser for formatting LLM responses
from langchain_core.runnables import RunnablePassthrough  # Pass-through operation for chain elements
from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings  # Google Generative AI wrapper for LLM and embeddings

from langchain_community.document_loaders import (
    AsyncHtmlLoader, PyPDFDirectoryLoader, Docx2txtLoader,
    UnstructuredMarkdownLoader, WikipediaLoader, ArxivLoader,
    CSVLoader, GithubFileLoader
)
from langchain_core.prompts import PromptTemplate

# Standard Python libraries
import readline  # For interactive user input
import os  # OS library for environment variables and file operations
import requests  # For making HTTP requests
import argparse
import random  # For random operations used in selecting content
from langchain.schema import Document  # Document schema for content storage

# ---------------------------------- CONFIGURATION AND INITIALIZATION ----------------------------------
DEBUG_MODE = False  # Set to True to enable debugging output

# Initialize cache to store previous user queries and their relevant documents
cache = {}

# Initialize vector store using Chroma for storing and retrieving documents
vectorstore = Chroma(
    persist_directory="./rag_data/.chromadb",  # Path to store data persistently
    embedding_function=GoogleGenerativeAIEmbeddings(
        api_key=os.getenv("GOOGLE_API_KEY"), model="models/embedding-001"
    )
)

# ---------------------------------- DOCUMENT LOADING FUNCTIONS ----------------------------------
def load_python_files(directory):
    """
    Load Python files from a specified directory.
    Args:
        directory (str): Path to the directory containing Python scripts.
    Returns:
        list: List of document objects.
    """
    docs = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                loader = UnstructuredMarkdownLoader(file_path)
                docs.extend(loader.load())
    return docs

# Function for processing documents
def process_documents(docs):
    """
    Split documents into smaller chunks and add to vector store.
    Args:
        docs (list): List of Document objects to process.
    """
    text_splitter = TokenTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_documents(docs)
    vectorstore.add_documents(documents=chunks)

# ---------------------------------- SUMMARIZATION FUNCTION ----------------------------------
def summarize_code(docs):
    """
    Summarize Python code to generate documentation.
    Args:
        docs (list): List of Document objects containing Python code.
    """
    prompt = PromptTemplate.from_template("Summarize this Python code: {text}")
    llm = GoogleGenerativeAI(model="gemini-1.5-pro-latest", temperature=0.7)  # Initialize Google Gemini LLM

    chain = (
        {"text": RunnablePassthrough()} |
        prompt |
        llm |
        RunnablePassthrough()
    )

    for doc in docs:
        summary = chain.invoke(doc.page_content)
        print(f"Summary for file {doc.metadata['source']}:\n{summary}\n")

# ---------------------------------- ANALYSIS FUNCTION ----------------------------------
def analyze_code_for_vulnerabilities(docs):
    """
    Analyze Python code for potential vulnerabilities.
    Args:
        docs (list): List of Document objects containing Python code.
    """
    prompt = PromptTemplate.from_template("Analyze this Python code and list any potential vulnerabilities: {text}")
    llm = GoogleGenerativeAI(model="gemini-1.5-pro-latest", temperature=0.7)  # Initialize Google Gemini LLM

    chain = (
        {"text": RunnablePassthrough()} |
        prompt |
        llm |
        RunnablePassthrough()
    )

    for doc in docs:
        analysis = chain.invoke(doc.page_content)
        print(f"Vulnerability Analysis for file {doc.metadata['source']}:\n{analysis}\n")

# ---------------------------------- DEOBFUSCATION FUNCTION ----------------------------------
def deobfuscate_code(docs):
    """
    Deobfuscate obfuscated Python code.
    Args:
        docs (list): List of Document objects containing obfuscated Python code.
    """
    prompt = PromptTemplate.from_template("Deobfuscate the following Python code: {text}")
    llm = GoogleGenerativeAI(model="gemini-1.5-pro-latest", temperature=0.7)
   
    chain = (
        {"text": RunnablePassthrough()} |
        prompt |
        llm |
        RunnablePassthrough()
    )

    for doc in docs:
        deobfuscated_code = chain.invoke(doc.page_content)
        print(f"Deobfuscated Code for file {doc.metadata['source']}:\n{deobfuscated_code}\n")

# ---------------------------------- MAIN CLI APPLICATION ----------------------------------
def main():
    parser = argparse.ArgumentParser(description="LangChain Reverse Engineering Tool")
    parser.add_argument('--task', type=str, required=True, choices=['summarize', 'analyze', 'deobfuscate'], help='Task to perform')

    args = parser.parse_args()
    docs = load_python_files("./sample_scripts")

    if args.task == 'summarize':
        summarize_code(docs)
    elif args.task == 'analyze':
        analyze_code_for_vulnerabilities(docs)
    elif args.task == 'deobfuscate':
        deobfuscate_code(docs)

if __name__ == "__main__":
    main()
