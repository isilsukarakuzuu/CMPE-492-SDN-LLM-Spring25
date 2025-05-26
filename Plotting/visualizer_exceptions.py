import os
import argparse
import pandas as pd
import matplotlib.pyplot as plt
from glob import glob

# --- Argument parser ---
parser = argparse.ArgumentParser(description="Plot Locust test metrics by user count and ramp rate.")
parser.add_argument("--data-dir", type=str, required=True, help="Path to directory containing *_exceptions.csv files")
args = parser.parse_args()

data_dir = args.data_dir

# --- Metrics to plot ---
columns_to_plot = [
    "Count"
]

# --- Find all *_exceptions.csv files ---
stats_files = glob(os.path.join(data_dir, "**/*_exceptions.csv"), recursive=True)

data = []

# --- Extract metrics for each file ---
for file in stats_files:
    try:
        df = pd.read_csv(file)

        row = df.iloc[0]
        filename = os.path.basename(file).replace("_exceptions.csv", "")
        parts = filename.split("_")

        model = parts[0]  # You can also join parts[:-3] if model has underscores
        user_count = next(int(p[1:]) for p in parts if p.startswith("u"))
        ramp_up    = next(int(p[1:]) for p in parts if p.startswith("r"))


        record = {
            "Model": model,
            "Users": user_count,
            "Ramp": ramp_up
        }

        for col in columns_to_plot:
            record[col] = row[col]

        data.append(record)
    except Exception as e:
        print(f"[ERROR] Skipping {file}: {e}")

df_all = pd.DataFrame(data)

if df_all.empty:
    raise ValueError("No valid data collected. Check filenames and file contents.")

# --- Generate plots ---
# Ensure output directory exists
plot_dir = "../Plots/3 GPU/Llama"
os.makedirs(plot_dir, exist_ok=True)

for metric in columns_to_plot:
    plt.figure(figsize=(10, 6))

    for ramp in [10, 100]:
        subset = df_all[df_all["Ramp"] == ramp].sort_values("Users")
        x = subset["Users"]
        y = subset[metric]

        # Plot with markers and line
        plt.plot(x, y, marker='o', label=f"Ramp {ramp}")

        # Add value labels on each point
        for i, val in enumerate(y):
            if isinstance(val, (int, float)) and not pd.isna(val):
                fmt = f"{val:.2f}" if isinstance(val, float) and not val.is_integer() else str(int(val))
                plt.text(x.iloc[i], y.iloc[i], fmt, ha='center', va='bottom', fontsize=8)

    # Title formatting
    pretty_title = metric.replace("pct", "%").replace("/", " per ").replace("_", " ")
    pretty_title = pretty_title.title()

    # Dynamic y-axis margin
    all_vals = df_all[metric].dropna().astype(float)
    if not all_vals.empty:
        ymin, ymax = all_vals.min(), all_vals.max()
        margin = (ymax - ymin) * 0.15 if ymax > ymin else 1
        plt.ylim([ymin - margin, ymax + margin])

    plt.title(f"{pretty_title} vs Number of Users")
    plt.xlabel("Number of Users")
    # Define units for y-axis based on metric name
    if metric == "Count":
        y_unit = "(Exception Count)"
    else:
        y_unit = ""


    plt.ylabel(f"{pretty_title} {y_unit}")

    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()

    # Save plot
    safe_name = metric.replace("/", "_").replace("%", "pct").replace(" ", "_")
    output_path = os.path.join(plot_dir, f"plot_{safe_name}.png")
    plt.savefig(output_path)
    plt.close()
    print(f"✅ Saved plot for {metric} to {output_path}")

print("✅ All metric plots saved to:", data_dir)
