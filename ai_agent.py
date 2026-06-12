from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import BaseTool, tool
import requests

from langchain_community.tools import DuckDuckGoSearchResults
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.9)

from langchain_classic.agents import create_react_agent, AgentExecutor
# from langchain_classic import hub 
# 1. Replace "from langchain import hub" with this:
from langchain_classic import hub
from langsmith import Client

client = Client()

# 2. Pull the prompt directly via the client:
# prompt = client.pull_prompt(
#     "hwchase17/react", 
#     dangerously_pull_public_prompt=True
# )
prompt = client.pull_prompt(
    "hwchase17/structured-chat-agent", 
    dangerously_pull_public_prompt=True
)
search_tool = DuckDuckGoSearchResults()
agent = create_react_agent(llm, tools=[search_tool],prompt=prompt)

agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=[search_tool], verbose=True,handle_parsing_errors=True)

response = agent_executor.invoke({"input":"3 ways to visit Goa from Pune?"})
print(response['output'])
  