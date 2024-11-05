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

