# CMPE-492-SDN-LLM-Spring25

# LLM Load Testing with Locust

This project uses [Locust](https://locust.io/) to performance test LLM API endpoints. It supports switching between different models and simulating both general and code-generation workloads.

---

## 🚀 Models Supported

- `gemma3:4b`cd Locust
- `llama3:8b`
- `deepseek-coder:6.7b` (used for code generation)

---

## 📁 Project Structure

```
.
├── Locust/ # Locust load scripts
│ ├── locustfile.py
│ ├── run-locust-benchmark.py
│ └── requirements.txt
├── Prompts/ # Prompt data
│ ├── code-generation.txt
│ └── general-questions.txt
├── Ollama/ # Model deployment folders with Dockerfiles
├── Plotting/ # Visualizer and analysis scripts
│ ├── gcp-data-plotter.py
│ └── visualizer_stats.py
├── All Results/ # Raw test outputs for all models & GPUs
├── summary_complete.csv # Aggregated statistics
```

---

## 🔧 Setup

1. **Install dependencies**  
   *(Best inside a virtual environment)*

   ```bash
   cd Locust
   pip install -r requirements.txt
   ```

2. **Add your prompts (Optional)**  
   Change `code-generation.txt` and `general-questions.txt` with one prompt per line.

---

## 🧪 Running the Test

Use the `MODEL_NAME` environment variable to test different models.

```bash
# Test Gemma
MODEL_NAME="gemma3:4b" \
locust -f locustfile.py --host=https://ollama-gemma-587938011321.us-central1.run.app

# Test LLaMA
MODEL_NAME="llama3:8b" \
locust -f locustfile.py --host=https://ollama-llama-587938011321.us-central1.run.app

# Test DeepSeek (used for code-gen prompts + slower wait time)
MODEL_NAME="deepseek-coder:6.7b" \
locust -f locustfile.py --host=https://ollama-deepseek-587938011321.us-central1.run.app

# Test all scenarios (approximately 7 hour)
python3 run-locust-benchmark.py \
  --model deepseek-coder:6.7b \
  --host https://ollama-deepseek-312305340350.us-central1.run.app

python3 run-locust-benchmark.py \
  --model gemma3:4b \
  --host https://ollama-gemma-991933130001.us-central1.run.app

python3 run-locust-benchmark.py \
  --model llama3:8b \
  --host https://ollama-llama-994669362161.us-central1.run.app

# Plot results
python3.11 visualizer_stats.py --data-dir "../All Results/3 GPU/results_deepseek"
```

Then open your browser at `http://localhost:8089` to start the test.

---

## ⚙️ Behavior

- **DeepSeek** uses `code-generation.txt` and a slower wait time (5–8 seconds).
- **Gemma & LLaMA** use `general-questions.txt` and a faster wait time (1–3 seconds).
- Prompts are picked randomly on each request.
- Errors are logged if API responses are non-200.

---

## 📌 Notes

- Customize the wait times or model behavior directly in `locustfile.py`.
- Add more user load or adjust spawn rate from the Locust web UI.
