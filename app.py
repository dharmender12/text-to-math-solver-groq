import streamlit as st
from pathlib import Path
from langchain_classic.agents import create_sql_agent
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
from langchain_classic.agents.agent_types import AgentType
from langchain_classic.agents.agent_toolkits import SQLDatabaseToolkit
from sqlalchemy import create_engine
import sqlite3
from langchain_groq import ChatGroq
from urllib.parse import quote_plus
from langchain_classic.sql_database import SQLDatabase
import os 
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

st.title("Langchain: Chat with SQL Database")

# Get database connection details from environment variables

LOCALDB = 'USE_LOCALDB'
MYSQLDB = 'USE_MYSQL'

radio_option = ['Use Local SQLite3 Database(student.db)', 'Connect to MySQL Database']

selected_option = st.sidebar.radio("Choose the DB you want to chat with", options = radio_option)

if selected_option == 'Connect to MySQL Database':
    db_url = MYSQLDB
    mysql_host = st.sidebar.text_input("Provide MySQL Hostname", value='localhost')
    mysql_user = st.sidebar.text_input("Provide MySQL Username", value='root')
    mysql_password = st.sidebar.text_input("Provide MySQL Password", type='password')
    mysql_db_name = st.sidebar.text_input("Provide MySQL Database Name", value='testdb')
    # connection_string = f"mysql+pymysql://{mysql_user}:{quote_plus(mysql_password)}@{mysql_host}/{mysql_db_name}"
    # engine = create_engine(connection_string)
else : 
    db_url = LOCALDB
    
default_api_key = os.environ.get("GROQ_API_KEY", "")
groq_api = st.sidebar.text_input(
    "Provide Groq API Key", 
    value=default_api_key, 
    type='password',
    help="Get your Groq API key from https://console.groq.com/"
)

# Sanitize key: remove spaces, emojis, and non-ASCII characters
if groq_api:
    groq_api = re.sub(r'[^\x21-\x7E]', '', groq_api)

import re

if not groq_api:
    # st.warning("Please provide your Groq API Key to proceed.")
    st.info("Please provide your Groq API Key to proceed.")
    st.stop()


model = ChatGroq(model='llama-3.3-70b-versatile',groq_api_key=groq_api,streaming=True)

@st.cache_resource(ttl=7200)
def configure_db(db_uri,mysql_host=None,mysql_user=None,mysql_password=None,mysql_db_name=None):
    if db_uri == LOCALDB:
        # Create a local SQLite database connection
        dbfilepath = (Path(__file__).parent / "agents.db").absolute()
        creator = lambda: sqlite3.connect(f'file:{dbfilepath}?mode=ro', uri=True)
        return SQLDatabase(create_engine('sqlite:///', creator=creator))
    
    elif db_uri == MYSQLDB:
        # Create a MySQL database connection
        if not(mysql_host and mysql_user and mysql_password and mysql_db_name):
            st.error("Please provide all MySQL connection Details")
            st.stop()
        encoded_password = quote_plus(mysql_password)
        connection_str = f"mysql+mysqlconnector://{mysql_user}:{encoded_password}@{mysql_host}/{mysql_db_name}"
        try: 
            db = SQLDatabase(create_engine(connection_str))
            st.success("Successfully connected to MySQL Database!")
            return db
        except Exception as e:
            st.error(f"Failed to connect to MySQL Database: {e}")
            st.stop() 
 

if db_url == MYSQLDB:
    db = configure_db(db_url, mysql_host, mysql_user, mysql_password, mysql_db_name)
else:
    db = configure_db(db_url)

toolkit = SQLDatabaseToolkit(db=db, llm=model)

agent = create_sql_agent(llm=model, toolkit=toolkit,verbose=True,agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION)

if 'messages' not in st.session_state or st.button("Clear Conversation"):
    st.session_state['messages'] = [{"role": "Assistant", "content": "How can I help you ?"}]
    for msg in st.session_state['messages']:
        st.chat_message(msg['role']).write(msg['content'])


user_query = st.chat_input("Ask anything from the database...")

if user_query:
    st.session_state['messages'].append({"role": "User", "content": user_query})
    st.chat_message("User").write(user_query)
    with st.chat_message("Assistant"):
        try:
            st_callback = StreamlitCallbackHandler(st.container())
            response = agent.run(user_query, callbacks=[st_callback])
            st.session_state['messages'].append({"role": "Assistant", "content": response})
            st.write(response)
        except Exception as e:
            error_msg = str(e)
            if "api_key" in error_msg.lower() or "authentication" in error_msg.lower() or "401" in error_msg:
                st.error("🔑 **Invalid or Missing Groq API Key!** Please check your API key in the sidebar and ensure it is valid.")
            else:
                st.error(f"⚠️ **An error occurred:** {error_msg}") 