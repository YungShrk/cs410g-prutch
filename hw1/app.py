# Imports from LangChain and standard Python libraries
from langchain import hub  # LangChain Hub for loading prompt templates
from langchain.text_splitter import TokenTextSplitter  # Splits documents into smaller chunks for processing
from langchain_chroma import Chroma  # Updated import path for Chroma vector storage
from langchain_core.output_parsers import StrOutputParser  # Output parser for formatting LLM responses
from langchain_core.runnables import RunnablePassthrough  # Pass-through operation for chain elements
from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings  # Google Generative AI wrapper for LLM and embeddings

# Standard Python libraries
import readline  # For interactive user input
import os  # OS library for environment variables and file operations
import requests  # For making HTTP requests
import argparse
import random  # For random operations used in selecting content
from langchain.schema import Document  # Document schema for content storage

# Configuration
DEBUG_MODE = False  # Set to True to enable debugging output

# Wikipedia topics to load
wiki_topics = [
    "Batman",
    "Computer Science",
    "AI",
    "Video Games",
    "South America"
]

# Initialize cache to store previous user queries and their relevant documents
cache = {}

# Initialize vector store using Chroma for storing and retrieving documents
vectorstore = Chroma(
    persist_directory="./rag_data/.chromadb",  # Path to store data persistently
    embedding_function=GoogleGenerativeAIEmbeddings(
        api_key=os.getenv("GOOGLE_API_KEY"), model="models/embedding-001"
    )
)

# Load URLs to be processed
urls = [
    "https://www.pdx.edu/academics/programs/undergraduate/computer-science",
    "https://www.pdx.edu/computer-science/"
]

# Document loading functions
def load_documents_from_folder(folder_path):
    """
    Load documents from a specified folder.
    Args:
        folder_path (str): Path to the folder containing documents.
    """
    print(f"Loading documents from folder: {folder_path}...")
    docs = DirectoryLoader(folder_path).load()
    process_documents(docs)

def load_urls(urls):
    """
    Load documents from a list of URLs asynchronously.
    Args:
        urls (list): List of URLs to load.
    """
    docs = AsyncHtmlLoader(urls).load()
    process_documents(docs)

def load_wikipedia_articles(query, max_docs=20):
    """
    Load Wikipedia articles based on a search query.
    Args:
        query (str): Search term for Wikipedia articles.
        max_docs (int): Maximum number of articles to load.
    """
    print(f"Loading up to {max_docs} Wikipedia articles for query: '{query}'...")
    docs = WikipediaLoader(query=query, load_max_docs=max_docs).load()
    if docs:
        print(f"Loaded {len(docs)} articles for '{query}'.")
        process_documents(docs)
    else:
        print(f"No articles found for query: {query}")

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

