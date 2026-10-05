import pandas as pd
import json

df = pd.read_csv(
    "artifacts/processed_data.csv"
)

report = {}

# Number of records
report["total_records"] = len(df)

# Missing values
missing = int(
    df.isnull().sum().sum()
)

report["missing_values"] = missing

# Duplicate records
duplicates = int(
    df.duplicated().sum()
)

report["duplicates"] = duplicates

# Check IDs
invalid_ids = int(
    (df["id"] <= 0).sum()
)

report["invalid_ids"] = invalid_ids

# Overall status
if (
    missing == 0
    and duplicates == 0
    and invalid_ids == 0
):
    report["status"] = "PASS"
else:
    report["status"] = "FAIL"

# Save validation artifact
with open(
    "artifacts/validation_report.json",
    "w"
) as file:

    json.dump(
        report,
        file,
        indent=4
    )

print("Validation completed.")

print(json.dumps(
    report,
    indent=4
))