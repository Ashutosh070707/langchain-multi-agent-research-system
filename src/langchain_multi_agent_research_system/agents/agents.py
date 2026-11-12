import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq

from src.langchain_multi_agent_research_system.tools.tools import scrape_url, search_web

load_dotenv()

os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# Model initialization
gemini_model = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    max_retries=1,
    timeout=60,
)
groq_model = ChatGroq(model="openai/gpt-oss-120b", temperature=0)


# 1st agent: Search Agent
def build_search_agent():
    return create_agent(
        model=gemini_model,
        tools=[search_web],
        system_prompt="You are a research assistant. Your task is to search the web for information on a given topic.",
    )


# 2nd agent: Reader agent
def build_reader_agent():
    return create_agent(
        model=gemini_model,
        tools=[scrape_url],
        system_prompt="You are a research assistant. Your task is to read and summarize information from web pages.",
    )


# writer chain
writer_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert research writer. Write clear, structured and insightful reports.",
        ),
        (
            "human",
            """Write a detailed research report on the topic below.

Topic: {topic}

Research Gathered:
{research}

Structure the report as:
- Introduction
- Key Findings (minimum 3 well-explained points)
- Conclusion
- Sources (list all URLs found in the research)

Be detailed, factual and professional.""",
        ),
    ]
)

writer_chain = writer_prompt | groq_model | StrOutputParser()


# critic_chain
critic_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a sharp and constructive research critic. Be honest and specific.",
        ),
        (
            "human",
            """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
...""",
        ),
    ]
)

critic_chain = critic_prompt | groq_model | StrOutputParser()
