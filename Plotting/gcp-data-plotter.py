import os
import pandas as pd

# --- CONFIG ---
BASE_DIR = "../All Results"
RESULTS = {
    "latency_p99": "Request_Latencies_1.csv",
    "latency_p95": "Request_Latencies_2.csv",
    "latency_p50": "Request_Latencies_3.csv",
    "sent_bytes": "Sent_bytes.csv",
    "recv_bytes": "Received_bytes.csv",
    "request_count": "Request_count.csv",
    "Max_concurrent_requests_p99": "Max_concurrent_requests_1.csv",
    "Max_concurrent_requests_p95": "Max_concurrent_requests_2.csv",
    "Max_concurrent_requests_p50": "Max_concurrent_requests_3.csv",
    "GPU_utilization_p99": "GPU_utilization_1.csv",
    "GPU_utilization_p95": "GPU_utilization_2.csv",
    "GPU_utilization_p50": "GPU_utilization_3.csv",
    "GPU_memory_utilization_p99": "GPU_memory_utilization_1.csv",
    "GPU_memory_utilization_p95": "GPU_memory_utilization_2.csv",
    "GPU_memory_utilization_p50": "GPU_memory_utilization_3.csv",
    "Container_CPU_utilization_p99": "Container_CPU_utilization_1.csv",
    "Container_CPU_utilization_p95": "Container_CPU_utilization_2.csv",
    "Container_CPU_utilization_p50": "Container_CPU_utilization_3.csv",
    "Container_memory_utilization_p99": "Container_memory_utilization_1.csv",
    "Container_memory_utilization_p95": "Container_memory_utilization_2.csv",
    "Container_memory_utilization_p50": "Container_memory_utilization_3.csv",
}

OUTPUT_DIR = "./plots"

def load_clean_csv(file_path: str, value_col_name: str) -> pd.DataFrame:
    """
    Load a Cloud Monitoring CSV file, skipping metadata and cleaning column names.

    Parameters:
        file_path (str): Full path to the .csv file
        value_col_name (str): Name to assign to the value column (e.g., 'latency_p95')

    Returns:
        pd.DataFrame: Cleaned DataFrame with ['timestamp', value_col_name]
    """
    def detect_data_start_line(path):
        with open(path) as f:
            for i, line in enumerate(f):
                # Check for a timestamp-like line
                if " May " in line:
                    return i
        return 0

    skip = detect_data_start_line(file_path)

    try:
        df = pd.read_csv(file_path, skiprows=skip, header=None)
        df.columns = ['timestamp', value_col_name]
        df.dropna(subset=['timestamp', value_col_name], inplace=True)
        df.reset_index(drop=True, inplace=True)
        return df
    except Exception as e:
        print(f"[ERROR] Failed to load {file_path}: {e}")
        return pd.DataFrame(columns=['timestamp', value_col_name])

def load_all_metrics(base_path: str, results_map: dict):
    all_metrics = {}
    for key, filename in results_map.items():
        path = os.path.join(base_path, filename)
        df = load_clean_csv(path, key)
        all_metrics[key] = df
    return all_metrics

def process_all_runs(root_dir: str, results_map: dict):
    all_results = {}

    for gpu_config in ["3 GPU", "5 GPU"]:
        gpu_path = os.path.join(root_dir, gpu_config)

        for model_folder in os.listdir(gpu_path):
            if not model_folder.startswith("results_"):
                continue

            model_name = model_folder.replace("results_", "")
            run_id = f"{model_name}_{gpu_config.replace(' ', '')}"

            gcp_results_path = os.path.join(gpu_path, model_folder, "GCP Results")
            if not os.path.isdir(gcp_results_path):
                print(f"[WARN] GCP Results folder missing in: {gcp_results_path}")
                continue

            print(f"[INFO] Loading {run_id}")
            metrics = load_all_metrics(gcp_results_path, results_map)
            all_results[run_id] = metrics

    return all_results

def main():
    all_results = process_all_runs(BASE_DIR, RESULTS)

    for run_id, metrics in all_results.items():
        print(f"[INFO] Processing run: {run_id}")
        for metric_name, df in metrics.items():
            if df.empty:
                print(f"[WARN] No data for {metric_name} in {run_id}")
                continue

            output_file = os.path.join(OUTPUT_DIR, f"{run_id}_{metric_name}.csv")
            df.to_csv(output_file, index=False)
            print(f"[INFO] Saved {metric_name} data to {output_file}")

if __name__ == "__main__":
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    main()
    print("[INFO] All metrics processed and saved.")
