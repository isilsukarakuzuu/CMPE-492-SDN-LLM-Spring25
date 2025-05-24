import os
import random
import time
import csv
from locust import HttpUser, task, between

class OllamaUser(HttpUser):
    wait_time = between(5, 10)

    def on_start(self):
        self.model_name = os.getenv("MODEL_NAME")

        # Choose prompt source file based on model
        if "deepseek" in self.model_name.lower():
            self.prompt_file = "../Prompts/code-generation.txt"
        else:
            self.prompt_file = "../Prompts/general-questions.txt"

        # Load prompts into memory once
        try:
            with open(self.prompt_file, "r") as f:
                self.prompts = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"Prompt file {self.prompt_file} not found.")

        self.metrics_file = "metrics.csv"
        
        with open(self.metrics_file, mode="w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Model", "Prompt", "Tokens", "TTFT (s)", "Avg Time/Token (s)"])

    @task
    def chat_request(self):
        prompt = random.choice(self.prompts)
        payload = {
            "model": self.model_name,
            "prompt": prompt,
        }

        start_time = time.time()
        first_token_arrival = None
        token_count = 0

        with self.client.post("/api/generate", json=payload, stream=True) as response:
            if response.status_code != 200:
                print(f"Error: {response.status_code}, {response.text}")
                return

            try:
                for line in response.iter_lines():
                    if not line:
                        continue

                    if first_token_arrival is None:
                        first_token_arrival = time.time()

                    token_count += 1

                end_time = time.time()

                ttft = first_token_arrival - start_time if first_token_arrival else None
                duration = end_time - first_token_arrival if first_token_arrival else None
                avg_time_per_token = duration / token_count if token_count else None

                # Write metrics to CSV
                with open(self.metrics_file, mode="a", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow([
                        self.model_name,
                        prompt[:60] + ("..." if len(prompt) > 60 else ""),
                        token_count,
                        f"{ttft:.3f}" if ttft else "N/A",
                        f"{avg_time_per_token:.4f}" if avg_time_per_token else "N/A"
                    ])

            except Exception as e:
                print(f"Error parsing stream: {e}")
