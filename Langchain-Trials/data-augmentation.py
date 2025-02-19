import os
from langchain.llms import OpenAI
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Get the API key from the environment variable
api_key = os.getenv("OPENAI_API_KEY")

# Initialize the model with the API key
llm = OpenAI(api_key=api_key)

# Generate synthetic data
prompt = "Generate 10 sentences for sentiment analysis labeled as positive."
synthetic_data = llm.generate([prompt])
print(synthetic_data)
