import subprocess
import time
import os
import argparse
import shutil

# --- Parse command-line arguments ---
parser = argparse.ArgumentParser(description="Run Locust benchmarks with various user loads.")
parser.add_argument("--model", type=str, required=True, help="Model name (e.g., gemma3:4b, llama3:8b, deepseek-coder:6.7b)")
parser.add_argument("--host", type=str, required=True, help="Target host URL (e.g., https://your-cloud-run-url.run.app)")
args = parser.parse_args()

# --- Constants ---
locustfile = "locustfile.py"
output_dir = "results"
run_duration = "30m"
cooldown_duration = 60 * 10  # 10 minutes in seconds

user_counts = [100, 500, 1000, 1500, 2000]
spawn_rates = [10, 100]

# Create output directory
os.makedirs(output_dir, exist_ok=True)

# --- Run all tests ---
for users in user_counts:
    for rate in spawn_rates:
        test_name = f"{args.model.replace(':', '_')}_u{users}_r{rate}"
        print(f"\n🚀 Starting test: {test_name}")

        # Save test configuration
        config_path = f"{output_dir}/{test_name}_config.txt"
        with open(config_path, "w") as f:
            f.write(f"MODEL_NAME={args.model}\n")
            f.write(f"USERS={users}\n")
            f.write(f"SPAWN_RATE={rate}\n")
            f.write(f"DURATION={run_duration}\n")
            f.write(f"HOST={args.host}\n")

        # Run Locust
        cmd = [
            "locust",
            "-f", locustfile,
            "--headless",
            "--host", args.host,
            "--users", str(users),
            "--spawn-rate", str(rate),
            "--run-time", run_duration,
            "--csv", f"{output_dir}/{test_name}",
            "--csv-full-history"
        ]

        env = os.environ.copy()
        env["MODEL_NAME"] = args.model
        env["USERS"] = str(users)
        env["SPAWN_RATE"] = str(rate)


        subprocess.run(cmd, env=env)

        metrics_src = "metrics.csv"
        metrics_dst = f"{output_dir}/{test_name}_metrics.csv"

        if os.path.exists(metrics_src):
            shutil.move(metrics_src, metrics_dst)
            print(f"📊 Saved metrics file to: {metrics_dst}")
        else:
            print("⚠️ No metrics file found.")

        print(f"✅ Test {test_name} finished. Cooling down for {cooldown_duration / 60} minutes...")
        time.sleep(cooldown_duration)

print("\n🎉 All tests completed.")
