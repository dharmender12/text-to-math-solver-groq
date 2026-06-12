import streamlit as st 
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_classic.chains import LLMChain, LLMMathChain
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_classic.agents.agent_types import AgentType
from langchain_classic.agents import Tool, initialize_agent
from langchain_classic.callbacks import StreamlitCallbackHandler
import re
import os
from dotenv import load_dotenv

load_dotenv()

st.title("Text TO Math Solver Using Groq LLama")

default_api_key = os.environ.get("GROQ_API_KEY", "")
groq_api_key = st.sidebar.text_input(
    "Enter your Groq API Key", 
    value=default_api_key, 
    key="groq_api_key", 
    type="password",
    help="Get your Groq API key from https://console.groq.com/"
)

if not groq_api_key:
    st.warning("Please enter your Groq API Key:")
    st.stop()


model = ChatGroq(model="llama-3.1-8b-instant", api_key=groq_api_key)

## Initialize Agents
wiki = WikipediaAPIWrapper()

def safe_wiki_run(query):
    try:
        return wiki.run(query)
    except Exception as e:
        return f"Error: Failed to query Wikipedia due to a network or parsing error ({str(e)}). Please try again or use another tool."

wiki_tool = Tool(
    name="Wikipedia",
    func=safe_wiki_run,
    description="Agent used for searching over the internet to find various informations."
)

math_chain = LLMMathChain.from_llm(llm=model)

def math_tool_func(question):
    try:
        # Keep only digits, operators, dots, parentheses, and spaces
        clean_question = ''.join(re.findall(r'[\d\.\+\-\*\/\^\(\)\s]', question))
        # Replace caret with python exponentiation operator
        clean_question = clean_question.replace('^', '**').strip()
        if clean_question:
            import numexpr
            result = numexpr.evaluate(clean_question).item()
            return str(result)
        else:
            raise ValueError("Empty math expression")
    except Exception as e:
        try:
            return math_chain.run(question)
        except Exception:
            return "Sorry, I couldn't solve the math problem. Please check the input and try again."
    

calculator = Tool(
    name="Calculator",
    func=math_tool_func,
    description='Tool used for answering math related questions. Only input' \
    'matheatics expressions needed. '

    )

prompt = '''You are an agent tasked with solving user mathematical problem.
Logically arrive at the solution and display it point wise for the question below:
Question: {question}
Answer:
'''
prompt_template = PromptTemplate(template=prompt, input_variables=["question"])

chain = LLMChain(llm=model, prompt=prompt_template)

def reasoning_tool_func(question):
    return chain.run(question)

Reasoning_agent = Tool(
    name="Reasoning Agent",
    func=reasoning_tool_func,
    description="A Tool used for answering logic based and reasoning questions. "
)
## Build the Agent 
assistant_agent = initialize_agent(
    tools=[wiki_tool, calculator, Reasoning_agent],
    llm=model,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False,
    handle_parsing_errors=True

)

if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        {"role": "assistant", 
         "content": "Hi ! I am Math Chatbot who can answer all your math Questions. "}

    ] 


for msg in st.session_state.messages:
    st.chat_message(msg['role'] ).write(msg['content'])


question = st.chat_input("Please Ask Your Question:")

if question: 
    with st.spinner("Thinking..."):
        st.session_state.messages.append({"role": "user", "content": question})
        st.chat_message("user").write(question)
        
        # Check if the question is a pure mathematical expression
        if re.match(r'^[\d\.\+\-\*\/\^\(\)\s]+$', question):
            try:
                # Evaluate pure math expression directly for instant response
                clean_expr = question.replace('^', '**').strip()
                import numexpr
                result = numexpr.evaluate(clean_expr).item()
                response = f"Answer: {result}"
            except Exception as e:
                # Fallback to agent if direct evaluation fails
                st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
                response = assistant_agent.run(question, callbacks=[st_cb])
        else:
            # Run the agent and show thoughts using the callback handler
            st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
            response = assistant_agent.run(question, callbacks=[st_cb])
            
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.chat_message("assistant").write(response)
        