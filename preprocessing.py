import argparse
import json
import os
import pandas as pd

parser = argparse.ArgumentParser(description="Air Quality Data Preprocessing Pipeline")
parser.add_argument("--version", type=str, default="v1", help="Artifact version (e.g. v1, v2)")
args = parser.parse_args()

version = args.version
artifact_dir = os.path.join("artifacts", version)
raw_path = os.path.join(artifact_dir, "raw_data.json")

if not os.path.exists(raw_path):
    raw_path = os.path.join("artifacts", "raw_data.json")

print(f"[{version.upper()}] Starting Air Quality data preprocessing...")
print(f"[{version.upper()}] Reading raw artifact from: {raw_path}")

with open(raw_path, "r") as f:
    raw_json = json.load(f)

metadata = raw_json.get("_metadata", {})
city = metadata.get("city", "Unknown")

# Flatten hourly data into DataFrame
hourly_data = raw_json.get("hourly", {})
df = pd.DataFrame(hourly_data)

print(f"[{version.upper()}] Raw records loaded: {len(df)}")
print(f"[{version.upper()}] Original columns:", df.columns.tolist())

# Record initial null count
initial_nulls = int(df.isnull().sum().sum())
print(f"[{version.upper()}] Initial missing values count: {initial_nulls}")

# 1. Parse timestamps
df["time"] = pd.to_datetime(df["time"])

# 2. Add city identifier
df["city"] = city

# 3. Remove duplicate timestamps/rows
initial_rows = len(df)
df = df.drop_duplicates(subset=["time"])
removed_dups = initial_rows - len(df)
print(f"[{version.upper()}] Removed duplicate records: {removed_dups}")

# 4. Handle missing values (Sensor / time-series data imputation)
# Use forward fill then backward fill for continuous temporal continuity
numeric_cols = [
    "pm10", "pm2_5", "carbon_monoxide",
    "nitrogen_dioxide", "sulphur_dioxide", "ozone", "us_aqi"
]

for col in numeric_cols:
    if col in df.columns:
        # Time-series ffill then bfill
        df[col] = df[col].ffill().bfill()
        # Fallback to column median if entire range was null
        if df[col].isnull().sum() > 0:
            df[col] = df[col].fillna(df[col].median())

# 5. Sanity check: Ensure non-negative pollutant concentrations
for col in numeric_cols:
    if col in df.columns:
        df[col] = df[col].clip(lower=0.0)

remaining_nulls = int(df.isnull().sum().sum())
print(f"[{version.upper()}] Remaining missing values: {remaining_nulls}")

# Save cleaned artifact
os.makedirs(artifact_dir, exist_ok=True)
cleaned_versioned_path = os.path.join(artifact_dir, "cleaned_data.csv")
df.to_csv(cleaned_versioned_path, index=False)

# Also save to base artifacts folder
base_cleaned_path = os.path.join("artifacts", "cleaned_data.csv")
df.to_csv(base_cleaned_path, index=False)

print(f"\n[{version.upper()}] Preprocessing completed successfully.")
print(f"[{version.upper()}] Cleaned records count: {len(df)}")
print(f"[{version.upper()}] Sample cleaned data:")
print(df.head(3))
print(f"\n[{version.upper()}] Saved artifact: {cleaned_versioned_path}")
