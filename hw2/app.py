import os
from langchain.agents import initialize_agent, AgentType, Tool
from langchain.llms import OpenAI
from langchain.tools import TerminalTool, BaseTool
from langchain.utilities import WolframAlphaAPIWrapper

class PigLatinTranslatorTool(BaseTool):
    """
    A custom tool that translates English text into Pig Latin.
    """

    name = "pig_latin_translator"
    description = "Useful for translating English text into Pig Latin."

    def _run(self, text: str) -> str:
        """
        Translates the input text into Pig Latin.

        Args:
            text (str): The English text to translate.

        Returns:
            str: The translated Pig Latin text.
        """
        def pig_latin(word):
            first_letter = word[0]
            if first_letter.lower() in 'aeiou':
                return word + 'yay'
            else:
                return word[1:] + first_letter + 'ay'
        words = text.split()
        translated_words = [pig_latin(word) for word in words]
        return ' '.join(translated_words)

    async def _arun(self, text: str):
        """
        Asynchronous version is not implemented.

        Raises:
            NotImplementedError: Indicates the method is not implemented.
        """
        raise NotImplementedError("This tool does not support async")

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
    pig_latin_translator = PigLatinTranslatorTool()
    tools = [
        Tool(
            name="Wolfram Alpha",
            func=wolfram_alpha.run,
            description="Useful for answering mathematical questions and computations."
        ),
        terminal_tool,
        pig_latin_translator
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
    print(agent.run("Translate 'Hello world' into Pig Latin"))
    print(agent.run("List all files in the current directory"))

if __name__ == "__main__":
    main()

