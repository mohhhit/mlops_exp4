import argparse
import json
import os
import pandas as pd

parser = argparse.ArgumentParser(description="Air Quality Data Validation Pipeline")
parser.add_argument("--version", type=str, default="v1", help="Artifact version (e.g. v1, v2)")
args = parser.parse_args()

version = args.version
artifact_dir = os.path.join("artifacts", version)
processed_path = os.path.join(artifact_dir, "processed_data.csv")
train_path = os.path.join(artifact_dir, "train_data.csv")
test_path = os.path.join(artifact_dir, "test_data.csv")

if not os.path.exists(processed_path):
    processed_path = os.path.join("artifacts", "processed_data.csv")
    train_path = os.path.join("artifacts", "train_data.csv")
    test_path = os.path.join("artifacts", "test_data.csv")

print(f"[{version.upper()}] Starting Air Quality data validation...")
print(f"[{version.upper()}] Reading: {processed_path}")

df = pd.read_csv(processed_path)
train_df = pd.read_csv(train_path) if os.path.exists(train_path) else pd.DataFrame()
test_df = pd.read_csv(test_path) if os.path.exists(test_path) else pd.DataFrame()

report = {}
report["version"] = version
report["total_records"] = len(df)
report["train_records"] = len(train_df)
report["test_records"] = len(test_df)

# Missing values check
missing = int(df.isnull().sum().sum())
report["missing_values"] = missing

# Duplicate check
duplicates = int(df.duplicated(subset=["time"]).sum()) if "time" in df.columns else int(df.duplicated().sum())
report["duplicates"] = duplicates

# Sanity check on target variable and key pollutants
invalid_aqi = int((df["us_aqi"] < 0).sum()) if "us_aqi" in df.columns else 0
report["invalid_aqi_values"] = invalid_aqi

invalid_pollutants = 0
for col in ["pm10", "pm2_5", "carbon_monoxide", "nitrogen_dioxide", "sulphur_dioxide", "ozone"]:
    if col in df.columns:
        invalid_pollutants += int((df[col] < 0).sum())
report["invalid_pollutant_values"] = invalid_pollutants

# Schema verification
required_cols = ["time", "pm10", "pm2_5", "us_aqi", "aqi_category", "aqi_category_code"]
missing_cols = [c for c in required_cols if c not in df.columns]
report["missing_required_columns"] = missing_cols

# Overall status check
if (
    missing == 0
    and duplicates == 0
    and invalid_aqi == 0
    and invalid_pollutants == 0
    and len(missing_cols) == 0
    and len(df) > 0
):
    report["status"] = "PASS"
else:
    report["status"] = "FAIL"

# Save validation artifact
report_path = os.path.join(artifact_dir, "validation_report.json")
with open(report_path, "w") as f:
    json.dump(report, f, indent=4)

with open(os.path.join("artifacts", "validation_report.json"), "w") as f:
    json.dump(report, f, indent=4)

print(f"\n[{version.upper()}] Validation completed.")
print(json.dumps(report, indent=4))
print(f"\n[{version.upper()}] Artifact saved: {report_path}")
