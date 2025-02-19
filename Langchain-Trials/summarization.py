import os
from dotenv import load_dotenv
from langchain.chains.summarize import load_summarize_chain
from langchain.llms import OpenAI
from langchain.schema import Document

# Load environment variables from the .env file
load_dotenv()

# Get the API key from the environment variable
api_key = os.getenv("OPENAI_API_KEY")

# Initialize the model with the API key
llm = OpenAI(api_key=api_key)

# Get the long text from file
with open('big.txt', 'r') as file:
    long_text = file.read()

# Break the text into smaller chunks
chunk_size = 1000  # Adjust chunk size based on token limits
chunks = [long_text[i:i + chunk_size] for i in range(0, len(long_text), chunk_size)]

# Process each chunk individually
summaries = []
chain = load_summarize_chain(llm=llm)

for chunk in chunks:
    document = [Document(page_content=chunk)]
    response = chain.invoke({"input_documents": document})
    summaries.append(response["output_text"])

# Combine summaries
final_summary = ' '.join(summaries)

print(final_summary)
