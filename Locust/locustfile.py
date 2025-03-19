from locust import HttpUser, task, between
import google.auth
import google.auth.transport.requests

import os   
from dotenv import load_dotenv

load_dotenv()

# Get the API key from the environment variable
token = os.getenv("GOOGLE_IDENTITY_TOKEN")


class OllamaUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        self.token = token

    @task
    def chat_request(self):
        payload = {
            "model": "gemma3:4b",
            "prompt": "How are you?",
        }
        headers = {
            "Authorization": f"Bearer {self.token}"
        }

        response = self.client.post("/api/generate", json=payload, headers=headers)
        if response.status_code != 200:
            print(f"Error: {response.status_code}, {response.text}")
