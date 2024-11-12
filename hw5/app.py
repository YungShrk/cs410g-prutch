from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.text_splitter import TokenTextSplitter
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.document_loaders import AsyncHtmlLoader, UnstructuredMarkdownLoader
from langchain_core.prompts import PromptTemplate

import os
import argparse

# Initialize vector store using Chroma for storing and retrieving documents
vectorstore = Chroma(
    persist_directory="./vulnerable_code_data/.chromadb",
    embedding_function=GoogleGenerativeAIEmbeddings(
        api_key=os.getenv("GOOGLE_API_KEY"),
        model="models/embedding-001"
    )
)

def load_code_files(directory, file_extension):
    """
    Load code files from a specified directory.
    Args:
        directory (str): Path to the directory containing code files.
        file_extension (str): The extension of code files to load (e.g., '.py', '.php').
    Returns:
        list: List of document objects.
    """
    docs = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(file_extension):
                file_path = os.path.join(root, file)
                loader = UnstructuredMarkdownLoader(file_path)
                docs.extend(loader.load())
    return docs

def process_documents(docs):
    """
    Split documents into smaller chunks and add to vector store.
    Args:
        docs (list): List of Document objects to process.
    """
    text_splitter = TokenTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_documents(docs)
    vectorstore.add_documents(documents=chunks)

def analyze_code_for_vulnerabilities(docs):
    """
    Analyze code files for potential vulnerabilities.
    Args:
        docs (list): List of Document objects containing code.
    """
    prompt = PromptTemplate.from_template("Analyze this code and list any potential vulnerabilities: {text}")
    llm = GoogleGenerativeAI(model="gemini-1.5-pro-latest", temperature=0.7)

    chain = (
        {"text": RunnablePassthrough()} |
        prompt |
        llm |
        RunnablePassthrough()
    )
    for doc in docs:
        analysis = chain.invoke(doc.page_content)
        print(f"Vulnerability Analysis for file {doc.metadata['source']}:\n{analysis}\n")

def main():
    parser = argparse.ArgumentParser(description="Vulnerability Scanner using LangChain")
    parser.add_argument('--task', type=str, required=True, choices=['analyze'], help='Task to perform')
    parser.add_argument('--directory', type=str, required=True, help='Directory to scan for code files')
    parser.add_argument('--file_extension', type=str, default='.php', help='Code file extension to scan (e.g., .py, .php)')
    args = parser.parse_args()

    docs = load_code_files(args.directory, args.file_extension)
    process_documents(docs)

    if args.task == 'analyze':
        analyze_code_for_vulnerabilities(docs)

if __name__ == "__main__":
    main()

