import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from collections import defaultdict
import re

# --- CONFIG ---
BASE_DIR = Path("../All Results")
OUTPUT_DIR = Path("./plots")
OUTPUT_DIR.mkdir(exist_ok=True)

# --- Helpers ---
def parse_experiment_metadata(filename):
    name = filename.stem  # remove .csv
    match = re.search(r"(.*)_u(\d+)_r(\d+)", name)
    if not match:
        raise ValueError(f"Filename format not recognized: {name}")
    model = match.group(1)
    users = int(match.group(2))
    ramp = int(match.group(3))
    return model, users, ramp

def collect_files(data_type):
    records = []
    for gpu_dir in BASE_DIR.glob("* GPU"):
        gpu_count = int(gpu_dir.name.split()[0])
        for model_dir in gpu_dir.iterdir():
            if not model_dir.is_dir():
                continue
            for file in model_dir.glob(f"*{data_type}.csv"):
                records.append((gpu_count, file))
            for gcp_dir in model_dir.glob("GCP*"):
                for file in gcp_dir.glob(f"*{data_type}.csv"):
                    records.append((gpu_count, file))
    return records

def collect_records(data_type):
    metrics_files = collect_files(data_type)
    metrics_data = defaultdict(pd.DataFrame)

    for gpu_count, filepath in metrics_files:
        try:
            df = pd.read_csv(filepath)
            df.dropna(inplace=True)
            model, users, ramp = parse_experiment_metadata(filepath)
            key = (gpu_count, model, users, ramp, data_type)
            if key in metrics_data:
                print(f"[WARNING] Duplicate entry for {key}, merging data.")
            else:
                metrics_data[key] = df
        except Exception as e:
            print(f"[ERROR] Failed to process {filepath.name}: {e}")
    return metrics_data

# --- Plotting Functions ---


# --- Main Routine ---
def main():
    exceptions = collect_records("exceptions")
    failures = collect_records("failures")
    metrics = collect_records("metrics")
    stats_history = collect_records("stats_history")
    stats = collect_records("stats")

    


if __name__ == "__main__":
    main()
