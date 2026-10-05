import requests
import json
import os

API_URL = "https://jsonplaceholder.typicode.com/users"

print("Starting data ingestion...")

# Make sure artifacts folder exists
os.makedirs("artifacts", exist_ok=True)

# Call API
response = requests.get(API_URL, timeout=10)

print("API status:", response.status_code)

# Check API response
response.raise_for_status()

# Convert response to JSON
data = response.json()

print("Records received:", len(data))

# Save raw API response
with open("artifacts/raw_data.json", "w") as file:
    json.dump(data, file, indent=4)

print("SUCCESS!")
print("Artifact created: artifacts/raw_data.json")