from langchain_groq import ChatGroq
from langchain_classic.schema import HumanMessage, SystemMessage
from langchain_community.document_loaders import PyPDFLoader
from langchain_classic.chains.summarize import load_summarize_chain
from langchain_core.prompts import PromptTemplate
from langchain_classic.text_splitter import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

model = ChatGroq(model='llama-3.1-8b-instant')

loader = PyPDFLoader("Dharmender_Thakur_Data_Analyst_coverletter.pdf")

data = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
docs = splitter.split_documents(data)

initial_prompt = PromptTemplate(template="Write a concise summary of the following text:\n {text}",
                               input_variables=["text"])

refine_prompt = PromptTemplate(template="You current summary is {existing_answer}. Now refine and " \
"improve it with the following new text:\n {text}"
                               "Provide an updated, improved summary that includes important details from both the old and new text.",
                               input_variables=["existing_answer","text"])
chain = load_summarize_chain(llm=model, chain_type="refine", question_prompt=initial_prompt, refine_prompt=refine_prompt, verbose=True)
response = chain.run(docs)
print(response)