import os
import pandas as pd
import csv
from datetime import datetime
from io import StringIO
from sklearn.cluster import KMeans
import numpy as np

# --- CONFIG ---
BASE_DIR = "./All Results"
OUTPUT_DIR = "./GCP CSVs"

user_counts = [100, 500, 1000, 1500, 2000]
ramp_counts = [10, 100]
gpu_configs = ["3GPU", "5GPU"]

RESULTS = {
    ("timestamp", "latency_p99"): "Request_Latencies_1.csv",
    ("timestamp", "latency_p95"): "Request_Latencies_2.csv",
    ("timestamp", "latency_p50"): "Request_Latencies_3.csv",
    ("timestamp", "sent_bytes_google", "sent_bytes_internet", "sent_bytes_private"): "Sent_bytes.csv",
    ("timestamp", "recv_bytes"): "Received_bytes.csv",
    ("timestamp", "request_count_2xx"): "Request_count.csv",
    ("timestamp", "Max_concurrent_requests_p99"): "Max_concurrent_requests_1.csv",
    ("timestamp", "Max_concurrent_requests_p95"): "Max_concurrent_requests_2.csv",
    ("timestamp", "Max_concurrent_requests_p50"): "Max_concurrent_requests_3.csv",
    ("timestamp", "GPU_utilization_p99"): "GPU_utilization_1.csv",
    ("timestamp", "GPU_utilization_p95"): "GPU_utilization_2.csv",
    ("timestamp", "GPU_utilization_p50"): "GPU_utilization_3.csv",
    ("timestamp", "GPU_memory_utilization_p99"): "GPU_memory_utilization_1.csv",
    ("timestamp", "GPU_memory_utilization_p95"): "GPU_memory_utilization_2.csv",
    ("timestamp", "GPU_memory_utilization_p50"): "GPU_memory_utilization_3.csv",
    ("timestamp", "Container_CPU_utilization_p99"): "Container_CPU_utilization_1.csv",
    ("timestamp", "Container_CPU_utilization_p95"): "Container_CPU_utilization_2.csv",
    ("timestamp", "Container_CPU_utilization_p50"): "Container_CPU_utilization_3.csv",
    ("timestamp", "Container_memory_utilization_p99"): "Container_memory_utilization_1.csv",
    ("timestamp", "Container_memory_utilization_p95"): "Container_memory_utilization_2.csv",
    ("timestamp", "Container_memory_utilization_p50"): "Container_memory_utilization_3.csv",
}

def load_clean_csv(file_path: str, col_names) -> pd.DataFrame:
    """
    Load a Cloud Monitoring CSV file, skipping metadata and cleaning column names.

    Parameters:
        file_path (str): Full path to the .csv file
        col_names (list or tuple): Column names to assign (will be adjusted to match file's columns)

    Returns:
        pd.DataFrame: Cleaned DataFrame with the specified column names
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
        # First determine the number of columns in the file
        with open(file_path) as f:
            for i, line in enumerate(f):
                if i >= skip:
                    num_cols = len(line.split(','))
                    break
        
        # Convert col_names to list if it's a tuple
        col_names = list(col_names)
        
        # Adjust column names to match file's column count
        if len(col_names) > num_cols:
            print(f"[WARN] File {file_path} has fewer columns ({num_cols}) than expected ({len(col_names)}). Using first {num_cols} columns.")
            used_col_names = col_names[:num_cols]
        elif len(col_names) < num_cols:
            print(f"[WARN] File {file_path} has more columns ({num_cols}) than expected ({len(col_names)}). Adding dummy columns.")
            used_col_names = col_names + [f'extra_{i}' for i in range(num_cols - len(col_names))]
        else:
            used_col_names = col_names

        df = pd.read_csv(file_path, skiprows=skip, header=None, names=used_col_names)
        df.dropna(how='all', inplace=True)  # Drop rows that are all NA
        df.reset_index(drop=True, inplace=True)
        return df
    except Exception as e:
        print(f"[ERROR] Failed to load {file_path}: {str(e)}")
        # Return empty DataFrame with at least timestamp column if available
        if len(col_names) > 0:
            return pd.DataFrame(columns=[col_names[0]])
        return pd.DataFrame()

def load_all_metrics(base_path: str, results_map: dict):
    all_metrics = {}
    for columns, filename in results_map.items():
        path = os.path.join(base_path, filename)
        if not os.path.exists(path):
            print(f"[WARN] File not found: {path}")
            continue
            
        df = load_clean_csv(path, columns)

        # Save each metric column (excluding 'timestamp') under its name
        for col_name in columns:
            if col_name in df.columns and col_name != "timestamp":
                all_metrics[col_name] = df[["timestamp", col_name]].copy()
            elif col_name != "timestamp":
                print(f"[WARN] Column {col_name} not found in {path}")

    return all_metrics

def process_all_runs(root_dir: str, results_map: dict):
    all_results = {}

    for gpu_config in ["3 GPU", "5 GPU"]:
        gpu_path = os.path.join(root_dir, gpu_config)

        if not os.path.isdir(gpu_path):
            print(f"[WARN] GPU config folder missing: {gpu_path}")
            continue

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
            try:
                metrics = load_all_metrics(gcp_results_path, results_map)
                all_results[run_id] = metrics
            except Exception as e:
                print(f"[ERROR] Failed to process {run_id}: {e}")

    return all_results

def infer_all_gpu_utilization_runs(output_dir=OUTPUT_DIR):
    """
    Process all GPU utilization CSV files in the directory using KMeans to infer run intervals.
    Extracts (model, gpu) from filename, returns a pandas DataFrame keyed by (model, gpu).
    """

    def kmeans_threshold(utilizations):
        """Estimate dynamic threshold using 2-cluster KMeans."""
        X = np.array(utilizations).reshape(-1, 1)
        kmeans = KMeans(n_clusters=2, random_state=0).fit(X)
        centers = sorted(kmeans.cluster_centers_.flatten())
        return sum(centers) / 2

    def infer_from_file(filepath):
        with open(filepath, 'r') as f:
            data = f.read()

        reader = csv.DictReader(StringIO(data))
        rows = [(datetime.strptime(r['timestamp'].split(' GMT')[0], '%a %b %d %Y %H:%M:%S'),
                 float(r['GPU_utilization_p99'])) for r in reader]

        if not rows:
            return None  # Skip empty

        utils = [util for _, util in rows]
        threshold = kmeans_threshold(utils)

        # Detect intervals of high utilization
        blocks = []
        in_block = False
        block_start = None

        for i, (ts, util) in enumerate(rows):
            if util > threshold:
                if not in_block:
                    in_block = True
                    block_start = ts
            else:
                if in_block:
                    in_block = False
                    block_end = rows[i - 1][0]
                    blocks.append((block_start, block_end))

        if in_block:
            blocks.append((block_start, rows[-1][0]))

        configs = [(u, r) for u in user_counts for r in ramp_counts]

        if len(blocks) > len(configs):
            raise ValueError(f"More detected blocks ({len(blocks)}) than config runs ({len(configs)}) in file {filepath}.")

        # Build dataframe rows
        df_rows = []
        for (start, end), (user, ramp) in zip(blocks, configs):
            df_rows.append({
                "user": user,
                "ramp_up": ramp,
                "time_start": start,
                "time_end": end
            })
        return pd.DataFrame(df_rows)

    all_results = []
    index_keys = []

    for fname in os.listdir(output_dir):
        if "GPU_utilization_p99" in fname and fname.endswith('.csv'):
            try:
                full_path = os.path.join(output_dir, fname)

                # Extract model and gpu from filename (e.g. gemma_5GPU_GPU_utilization_p99.csv)
                parts = fname.split('_')
                if len(parts) < 3:
                    print(f"[!] Skipping file with unexpected name format: {fname}")
                    continue
                model = parts[0]
                gpu_part = parts[1]
                if not gpu_part.endswith("GPU"):
                    print(f"[!] Skipping file with unexpected GPU info: {fname}")
                    continue
                gpu = int(gpu_part[:-3])  # remove 'GPU' and convert to int

                df = infer_from_file(full_path)
                if df is not None and not df.empty:
                    df['model'] = model
                    df['gpu'] = gpu
                    all_results.append(df)
                index_keys.append((model, gpu))

                print(f"[✓] Processed {fname}")

            except Exception as e:
                print(f"[!] Failed to process {fname}: {e}")

    if not all_results:
        print("[!] No data processed.")
        return pd.DataFrame()  # empty

    combined_df = pd.concat(all_results, ignore_index=True)

    # Set multi-index (model, gpu)
    combined_df.set_index(['model', 'gpu'], inplace=True)

    return combined_df


import pandas as pd
import os
import re
import itertools

def collect_summary_results(all_results: dict, output_dir: str, intervals_df: pd.DataFrame):
    intervals_df['time_start'] = pd.to_datetime(intervals_df['time_start'])
    intervals_df['time_end'] = pd.to_datetime(intervals_df['time_end'])

    models = set()
    gpus = set()
    user_counts = intervals_df['user'].unique()
    ramp_counts = intervals_df['ramp_up'].unique()

    # Extract models and gpus from intervals df MultiIndex
    for index in intervals_df.index:
        model, gpu = index  # Unpack MultiIndex
        models.add(model)
        gpus.add(str(gpu))
    models = sorted(models)
    gpus = sorted(gpus)

    # Prepare summary dict with keys (model, gpu, user, ramp)
    all_combinations = list(itertools.product(models, gpus, user_counts, ramp_counts))
    summary_dict = {
        (model, gpu, user, ramp): {metric: [] for metric in [
            "latency_p99", "latency_p95", "latency_p50", "sent_bytes_internet", "recv_bytes",
            "request_count_2xx",
            "sent_bytes_google", "sent_bytes_private",
            'Max_concurrent_requests_p99', 'Max_concurrent_requests_p95', 'Max_concurrent_requests_p50',
            'GPU_utilization_p99', 'GPU_utilization_p95', 'GPU_utilization_p50',
            'GPU_memory_utilization_p99', 'GPU_memory_utilization_p95', 'GPU_memory_utilization_p50',
            'Container_CPU_utilization_p99', 'Container_CPU_utilization_p95', 'Container_CPU_utilization_p50',
            'Container_memory_utilization_p99', 'Container_memory_utilization_p95', 'Container_memory_utilization_p50',
        ]} for model, gpu, user, ramp in all_combinations
    }

    def clean_timestamp(ts):
        return re.sub(r" GMT.*", "", ts)

    for run_id, metrics in all_results.items():
        # Extract model and gpu from run_id
        parts = run_id.split('_')
        model = parts[0]
        gpu = parts[1][0]

        # Get all intervals for this model and gpu using MultiIndex
        try:
            intervals_sub = intervals_df.xs((model, int(gpu)), level=['model', 'gpu'])
        except KeyError:
            print(f"[WARN] No intervals found for model {model} and GPU {gpu}")
            continue

        # For each metric, assign rows to the correct (user, ramp) based on timestamp in intervals
        for metric_name, df_metric in metrics.items():
            if df_metric is None or df_metric.empty:
                continue

            # Clean and parse timestamps
            df_metric = df_metric.copy()
            df_metric['timestamp_clean'] = df_metric['timestamp'].apply(clean_timestamp)
            df_metric['timestamp_dt'] = pd.to_datetime(df_metric['timestamp_clean'])

            # For each row, find which interval it falls into
            def find_interval_row(ts):
                # Filter intervals_sub where time_start <= ts < time_end
                mask = (intervals_sub['time_start'] <= ts) & (intervals_sub['time_end'] > ts)
                filtered = intervals_sub.loc[mask]
                if filtered.empty:
                    return None
                # If multiple intervals match (unlikely), pick first
                return filtered.iloc[0]

            # Map each timestamp to (user, ramp)
            user_ramp_list = []
            for ts in df_metric['timestamp_dt']:
                interval_row = find_interval_row(ts)
                if interval_row is not None:
                    user_ramp_list.append((interval_row['user'], interval_row['ramp_up']))
                else:
                    user_ramp_list.append((None, None))

            df_metric['user_ramp'] = user_ramp_list

            # Filter out rows without a matching interval
            df_metric = df_metric[df_metric['user_ramp'].apply(lambda x: x[0] is not None)]

            # Group by (user, ramp) and aggregate metric values
            for (user, ramp), group_df in df_metric.groupby('user_ramp'):
                # Values excluding timestamp columns (assuming metric values start from col 1)
                values = group_df.select_dtypes(include='number')
                if values.empty:
                    print(f"[WARN] No numeric data for metric {metric_name} in run {run_id}")
                    continue
                if metric_name in ["sent_bytes_internet", "recv_bytes", "sent_bytes_google", "sent_bytes_private"]:
                    agg_val = values.sum().sum()
                else:
                    # Take mean of first data column (usually the metric)
                    agg_val = values.iloc[:, 0].mean()

                summary_dict[(model, gpu, user, ramp)][metric_name].append(agg_val)

    # Build final DataFrame
    summary_rows = []
    for (model, gpu, user, ramp), metrics_values in summary_dict.items():
        row = {
            "Model": model,
            "GPU": gpu,
            "Users": user,
            "Ramp": ramp,
        }
        for metric, vals in metrics_values.items():
            if vals:  # Only calculate average if there are values
                row[metric] = sum(vals) / len(vals)
            else:
                row[metric] = pd.NA
        summary_rows.append(row)

    summary_df = pd.DataFrame(summary_rows)
    summary_df = summary_df.sort_values(by=["Model", "GPU", "Users", "Ramp"]).reset_index(drop=True)

    summary_file = os.path.join(output_dir, "summary_complete.csv")
    summary_df.to_csv(summary_file, index=False, float_format='%.3f')
    print(f"[INFO] Complete summary CSV saved to {summary_file}")

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

    df = infer_all_gpu_utilization_runs()
    print(df)
    collect_summary_results(all_results, "./", df)

if __name__ == "__main__":
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    main()
    print("[INFO] All metrics processed and saved.")
