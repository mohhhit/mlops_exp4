import json
import pandas as pd

# Read raw artifact
with open("artifacts/raw_data.json", "r") as file:
    data = json.load(file)

print("Raw records:", len(data))

# Convert JSON into DataFrame
df = pd.json_normalize(data)

print("\nOriginal columns:")
print(df.columns.tolist())

# Select required columns
df = df[
    [
        "id",
        "name",
        "username",
        "email",
        "address.city",
        "company.name"
    ]
]

# Rename columns
df = df.rename(
    columns={
        "address.city": "city",
        "company.name": "company"
    }
)

# Remove duplicates
df = df.drop_duplicates()

# Handle missing values
df["city"] = df["city"].fillna("Unknown")
df["company"] = df["company"].fillna("Unknown")

# Clean text
df["name"] = df["name"].str.strip()
df["city"] = df["city"].str.strip()

# Save cleaned artifact
df.to_csv(
    "artifacts/cleaned_data.csv",
    index=False
)

print("\nPreprocessing completed.")

print("\nCleaned data:")
print(df.head())

print("\nSaved:")
print("artifacts/cleaned_data.csv")