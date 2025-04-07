import os
import random
from locust import HttpUser, task, between

token = os.getenv("API_TOKEN")

class OllamaUser(HttpUser):
    wait_time = None  # will be set in on_start

    def on_start(self):
        self.model_name = os.getenv("MODEL_NAME")
        self.token = token

        # Choose prompt source file based on model
        if "deepseek" in self.model_name.lower():
            self.prompt_file = "./Prompts/code-generation.txt"
            self.wait_time = between(8, 11)
        else:
            self.prompt_file = "./Prompts/general-questions.txt"
            self.wait_time = between(1, 3)

        # Load prompts into memory once
        try:
            with open(self.prompt_file, "r") as f:
                self.prompts = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"Prompt file {self.prompt_file} not found.")

    @task
    def chat_request(self):
        prompt = random.choice(self.prompts)

        payload = {
            "model": self.model_name,
            "prompt": prompt,
        }
        headers = {
            "Authorization": f"Bearer {self.token}"
        }

        response = self.client.post("/api/generate", json=payload, headers=headers)
        if response.status_code != 200:
            print(f"Error: {response.status_code}, {response.text}")
