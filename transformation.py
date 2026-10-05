import pandas as pd

# Read cleaned data
df = pd.read_csv(
    "artifacts/cleaned_data.csv"
)

# Create a new column
df["name_length"] = df["name"].str.len()

# Convert city to uppercase
df["city"] = df["city"].str.upper()

# Create user category
df["user_type"] = df["name_length"].apply(
    lambda x: "LONG_NAME"
    if x > 12
    else "SHORT_NAME"
)

# Save processed artifact
df.to_csv(
    "artifacts/processed_data.csv",
    index=False
)

print("Transformation completed.")

print("\nProcessed data:")
print(df.head())

print("\nSaved:")
print("artifacts/processed_data.csv")