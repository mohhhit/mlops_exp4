import argparse
import os
import numpy as np
import pandas as pd

parser = argparse.ArgumentParser(description="Air Quality Feature Engineering & Transformation Pipeline")
parser.add_argument("--version", type=str, default="v1", help="Artifact version (e.g. v1, v2)")
args = parser.parse_args()

version = args.version
artifact_dir = os.path.join("artifacts", version)
cleaned_path = os.path.join(artifact_dir, "cleaned_data.csv")

if not os.path.exists(cleaned_path):
    cleaned_path = os.path.join("artifacts", "cleaned_data.csv")

print(f"[{version.upper()}] Starting Air Quality feature transformation...")
print(f"[{version.upper()}] Reading cleaned data from: {cleaned_path}")

df = pd.read_csv(cleaned_path)
df["time"] = pd.to_datetime(df["time"])

# 1. Temporal Feature Engineering
df["hour"] = df["time"].dt.hour
df["day_of_week"] = df["time"].dt.dayofweek
df["is_weekend"] = (df["day_of_week"] >= 5).astype(int)

# Cyclical encoding for hour (ML models learn periodic 24-hr cycle better)
df["hour_sin"] = np.sin(2 * np.pi * df["hour"] / 24.0)
df["hour_cos"] = np.cos(2 * np.pi * df["hour"] / 24.0)

# 2. Domain Feature: PM2.5 to PM10 fine particulate ratio
df["pm_ratio"] = (df["pm2_5"] / (df["pm10"] + 1e-5)).round(4)

# 3. Categorical Air Quality Index Label (EPA Standard)
def categorize_aqi(aqi):
    if aqi <= 50:
        return "Good"
    elif aqi <= 100:
        return "Moderate"
    elif aqi <= 150:
        return "Unhealthy_Sensitive"
    else:
        return "Unhealthy"

df["aqi_category"] = df["us_aqi"].apply(categorize_aqi)

# Numerical encoding for ML classification models
category_mapping = {
    "Good": 0,
    "Moderate": 1,
    "Unhealthy_Sensitive": 2,
    "Unhealthy": 3
}
df["aqi_category_code"] = df["aqi_category"].map(category_mapping)

# Save processed full dataset
processed_versioned_path = os.path.join(artifact_dir, "processed_data.csv")
df.to_csv(processed_versioned_path, index=False)
df.to_csv(os.path.join("artifacts", "processed_data.csv"), index=False)

# 4. Save Train and Test splits for ML Model
# 80/20 train/test split sorted by time (MLOps best practice for time-series)
train_size = int(len(df) * 0.8)
train_df = df.iloc[:train_size].copy()
test_df = df.iloc[train_size:].copy()

train_path = os.path.join(artifact_dir, "train_data.csv")
test_path = os.path.join(artifact_dir, "test_data.csv")
train_df.to_csv(train_path, index=False)
test_df.to_csv(test_path, index=False)

# Also copy to root artifacts
train_df.to_csv(os.path.join("artifacts", "train_data.csv"), index=False)
test_df.to_csv(os.path.join("artifacts", "test_data.csv"), index=False)

print(f"\n[{version.upper()}] Transformation completed.")
print(f"[{version.upper()}] Total transformed records: {len(df)}")
print(f"[{version.upper()}] Train set records: {len(train_df)}")
print(f"[{version.upper()}] Test set records: {len(test_df)}")
print(f"\n[{version.upper()}] Target distribution (aqi_category):")
print(df["aqi_category"].value_counts())

print(f"\n[{version.upper()}] Artifacts saved:")
print(f"- {processed_versioned_path}")
print(f"- {train_path}")
print(f"- {test_path}")
