import os
from dotenv import load_dotenv
from langchain.chains import ConversationChain
from langchain.llms import OpenAI

# Load environment variables from the .env file
load_dotenv()

# Get the API key from the environment variable
api_key = os.getenv("OPENAI_API_KEY")

# Initialize the model with the API key
llm = OpenAI(api_key=api_key)

# Create Conversation Chain
conversation = ConversationChain(llm=llm)

# Simulate conversation
conversation_input = "Hello, who won the 2024 World Cup?"
response = conversation.run(conversation_input)
print(response)
