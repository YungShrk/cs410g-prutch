import os
from langchain.agents import initialize_agent, AgentType, Tool
from langchain.llms import OpenAI
from langchain.tools import TerminalTool
from langchain.utilities import WolframAlphaAPIWrapper

def main():
    """
    Main function to initialize the agent and run queries.
    """

    # Set up OpenAI LLM
    llm = OpenAI(temperature=0)

    # Set up Wolfram Alpha tool
    wolframalpha_app_id = os.environ.get('WOLFRAMALPHA_APP_ID')
    if not wolframalpha_app_id:
        raise ValueError("Please set the WOLFRAMALPHA_APP_ID environment variable.")
    wolfram_alpha = WolframAlphaAPIWrapper()

    # Initialize tools
    terminal_tool = TerminalTool()
    tools = [
        Tool(
            name="Wolfram Alpha",
            func=wolfram_alpha.run,
            description="Useful for answering mathematical questions and computations."
        ),
        terminal_tool
    ]

    # Initialize the agent
    agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )

    # Example queries
    print(agent.run("What is the derivative of sin(x)?"))
    print(agent.run("List all files in the current directory"))

if __name__ == "__main__":
    main()

