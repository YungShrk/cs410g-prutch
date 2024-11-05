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

