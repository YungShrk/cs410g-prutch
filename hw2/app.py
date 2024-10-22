import os
from langchain.agents import initialize_agent, AgentType, Tool
from langchain.llms import OpenAI
from langchain.tools import TerminalTool

def main():
    """
    Main function to initialize the agent and run queries.
    """

    # Set up OpenAI LLM
    llm = OpenAI(temperature=0)

    # Initialize tools
    terminal_tool = TerminalTool()
    tools = [terminal_tool]

    # Initialize the agent
    agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )

    # Example query using the TerminalTool
    print(agent.run("List all files in the current directory"))

if __name__ == "__main__":
    main()
