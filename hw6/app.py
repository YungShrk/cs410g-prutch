# Import necessary modules for LangChain, including GoogleGenerativeAI for LLM and embeddings
from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.text_splitter import TokenTextSplitter
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from langchain.schema import Document
import os
import subprocess

# ---------------- CONFIGURATION ----------------
DEBUG_MODE = False  # Set to True to enable debugging output
COMMAND_TIMEOUT = 60  # Timeout for command execution in seconds

# Initialize vector store for storing and retrieving documents
vectorstore = Chroma(
    persist_directory="./command_data/.chromadb",
    embedding_function=GoogleGenerativeAIEmbeddings(
        api_key=os.getenv("GOOGLE_API_KEY"),
        model="models/embedding-001"
    )
)

# -------------- COMMAND GENERATION AND EXECUTION --------------

def generate_command(task_description):
    """
    Use LLM to generate a command-line command based on the given task description.
    Args:
        task_description (str): Description of the task to generate the command for.
    Returns:
        str: Generated command.
    """
    prompt = PromptTemplate.from_template("Generate a command for the following task: {text}")
    llm = GoogleGenerativeAI(model="gemini-1.5-pro-latest", temperature=0.7)
    chain = ({"text": RunnablePassthrough()} | prompt | llm | RunnablePassthrough())

    command = chain.invoke(task_description)
    return command


def execute_command(command):
    """
    Execute a generated command-line command.
    Args:
        command (str): The command to execute.
    Returns:
        str: The output of the command.
    """
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=COMMAND_TIMEOUT)
        return result.stdout.decode('utf-8')
    except subprocess.TimeoutExpired:
        return "Error: Command timed out."
    except subprocess.CalledProcessError as e:
        return f"Error executing command: {e.stderr.decode('utf-8')}"


def automate_tool_usage(task_descriptions):
    """
    Automate the generation and execution of commands for multiple tasks.
    Args:
        task_descriptions (list): List of task descriptions to automate.
    """
    for task in task_descriptions:
        print(f"Task: {task}")
        command = generate_command(task)
        print(f"Generated Command: {command}")
        if "tcpdump" in command or "nikto" in command or "dnsenum" in command:
            command = f"sudo {command}"
            print("Note: The generated command may require elevated privileges (e.g., using 'sudo').")
        output = execute_command(command)
        print(f"Command Output:\n{output}\n")

# -------------- RAG-INFORMED TOOL USING MAN PAGES --------------

def load_man_pages(tool_list):
    """
    Load the manual pages for the specified tools into the vector store for reference.
    Args:
        tool_list (list): List of tool names to load manual pages for.
    """
    docs = []
    for tool in tool_list:
        try:
            result = subprocess.run(f"man {tool}", shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            doc_content = result.stdout.decode('utf-8')
            docs.append(Document(page_content=doc_content, metadata={"source": tool}))
        except subprocess.CalledProcessError as e:
            print(f"Error loading man page for {tool}: {e.stderr.decode('utf-8')}")

    # Split and add documents to vector store
    if docs:
        text_splitter = TokenTextSplitter(chunk_size=1000, chunk_overlap=100)
        chunks = text_splitter.split_documents(docs)
        vectorstore.add_documents(documents=chunks)


def inform_command_with_rag(command_query):
    """
    Use retrieved information from manual pages to refine the command generation.
    Args:
        command_query (str): Query to refine the command using the manual pages.
    Returns:
        str: Refined command.
    """
    # Use vector store to retrieve relevant information
    results = vectorstore.similarity_search(command_query, k=3)
    context = "\n".join([doc.page_content for doc in results])

    # Use LLM to refine command with context from retrieved manual pages
    prompt = PromptTemplate.from_template("Refine the command for the following task based on the context: {context}\nTask: {text}")
    llm = GoogleGenerativeAI(model="gemini-1.5-pro-latest", temperature=0.7)
    chain = ({"text": RunnablePassthrough(), "context": RunnablePassthrough()} | prompt | llm | RunnablePassthrough())

    refined_command = chain.invoke({"text": command_query, "context": context})
    return refined_command

# -------------- MAIN FUNCTION --------------

def main():
    # Define a list of task descriptions for command generation
    task_descriptions = [
        "Capture network packets using tcpdump for 30 seconds",
        "Perform a vulnerability scan using nikto on the target IP 10.x.y.z",
        "Enumerate DNS information for the domain example.com using dnsenum"
    ]

    # Automate the generation and execution of commands for the tasks
    automate_tool_usage(task_descriptions)

    # Load manual pages for tools into vector store
    tool_list = ["tcpdump", "nikto", "dnsenum", "nmap", "sqlmap"]
    load_man_pages(tool_list)

    # Use RAG-informed approach to refine command generation
    command_query = "How can I use nmap to scan all open ports on an internal network?"
    refined_command = inform_command_with_rag(command_query)
    print(f"Refined Command: {refined_command}")


if __name__ == "__main__":
    main()

