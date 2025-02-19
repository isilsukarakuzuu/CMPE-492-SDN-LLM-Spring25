import os
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Get the API key from the environment variable
api_key = os.getenv("OPENAI_API_KEY")

# Initialize the model with the API key
llm = OpenAI(api_key=api_key)

# Define a custom prompt
custom_prompt = PromptTemplate(input_variables=["task"], template="Explain {task} in detail.")

# Create LLM Chain
custom_chain = LLMChain(prompt=custom_prompt, llm=llm)

# Run the custom chain
task_description = "how to train a neural network"
response = custom_chain.run({"task": task_description})
print(response)
