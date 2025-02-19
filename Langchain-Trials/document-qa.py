import os
from dotenv import load_dotenv
from langchain.chains.question_answering import load_qa_chain
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAI

# Load environment variables from the .env file
load_dotenv()

# Get the API key from the environment variable
api_key = os.getenv("OPENAI_API_KEY")

# Initialize the model with the API key
llm = OpenAI(api_key=api_key)

pdf_loader = PyPDFLoader('./IsilSuKarakuzuResume.pdf')
documents = pdf_loader.load()

chain = load_qa_chain(llm=llm)
query = 'Who is the CV about?'
response = chain.invoke({"input_documents": documents, "question": query})
print(response["output_text"])