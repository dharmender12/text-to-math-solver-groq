'''
from langchain_groq import ChatGroq
from langchain_classic.schema import HumanMessage, SystemMessage
from dotenv import load_dotenv

load_dotenv()

model = ChatGroq(model='llama-3.1-8b-instant')

speech = """
The quick brown fox jumps over the lazy dog. 
The dog was not happy about this and barked loudly. 
The fox, however, was quite pleased with itself and 
continued on its way. The dog eventually calmed down and 
went back to sleep, while the fox found a nice spot to rest 
in the sun. The moral of the story is that sometimes 
it's best to just let things go and not get too 
worked up about small annoyances.
"""     

chat_messages = [
    SystemMessage(content="You are an expert with expertise in summarizing provided text."),
    HumanMessage(content=f"Please provide a short and concise summary for the provided text:\n\n{speech.strip()}")
]

response = model.invoke(chat_messages)
print(response.content)
'''
# from langchain_classic.chains import LLMChain
# from langchain_core.prompts import PromptTemplate

# from langchain_groq import ChatGroq
# from langchain_classic.schema import HumanMessage, SystemMessage
# from dotenv import load_dotenv

# load_dotenv()

# model = ChatGroq(model='llama-3.1-8b-instant')

speech = """
The quick brown fox jumps over the lazy dog. 
The dog was not happy about this and barked loudly. 
The fox, however, was quite pleased with itself and 
continued on its way. The dog eventually calmed down and 
went back to sleep, while the fox found a nice spot to rest 
in the sun. The moral of the story is that sometimes 
it's best to just let things go and not get too 
worked up about small annoyances.
"""  
# generic_prompt = '''Summarize the following text: 
# {text} to be concise in this language: {language}'''

# prompt = PromptTemplate(template=generic_prompt,
#                                       input_variables=['text', 'language'])

# complete_prompt = prompt.format(text=speech, language='hindi')

# # print(model.get_num_tokens(complete_prompt))

# chain = LLMChain(llm=model, prompt=prompt)
# response = chain.invoke({'text': speech, 'language': 'hindi'})
# print(response)

from langchain_community.document_loaders import PyPDFLoader
from langchain_classic.chains.summarize import load_summarize_chain
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_classic.text_splitter import RecursiveCharacterTextSplitter

from dotenv import load_dotenv

load_dotenv()


model = ChatGroq(model='llama-3.1-8b-instant')

loader = PyPDFLoader("Dharmender_Thakur_Data_Analyst_coverletter.pdf")

docs = loader.load_and_split()
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splitter_docs = splitter.split_documents(docs)
prompt = PromptTemplate(template="Write a detailed summary of the following text:\n {text}",
                        input_variables=["text"])

chain = load_summarize_chain(llm=model, chain_type="map_reduce", map_prompt=prompt, combine_prompt=prompt, verbose=True)
# chain = load_summarize_chain(llm = model, chain_type="map_reduce", prompt=prompt,verbose=True)
response = chain.run(docs)
print(response)