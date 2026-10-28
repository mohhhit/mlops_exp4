import argparse
import json
import os
import requests

# Preset location configurations for versioning
LOCATIONS = {
    "v1": {
        "city": "Mumbai",
        "latitude": 19.0760,
        "longitude": 72.8777,
        "past_days": 7
    },
    "v2": {
        "city": "Delhi",
        "latitude": 28.6139,
        "longitude": 77.2090,
        "past_days": 14
    }
}

parser = argparse.ArgumentParser(description="Air Quality Data Ingestion Pipeline")
parser.add_argument("--version", type=str, default="v1", help="Artifact version (e.g. v1, v2)")
parser.add_argument("--city", type=str, default=None, help="City name override")
parser.add_argument("--past_days", type=int, default=None, help="Number of past days override")
args = parser.parse_args()

version = args.version
config = LOCATIONS.get(version, LOCATIONS["v1"]).copy()
if args.city:
    config["city"] = args.city
if args.past_days:
    config["past_days"] = args.past_days

city = config["city"]
lat = config["latitude"]
lon = config["longitude"]
past_days = config["past_days"]

api_url = (
    f"https://air-quality-api.open-meteo.com/v1/air-quality?"
    f"latitude={lat}&longitude={lon}&"
    f"hourly=pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,sulphur_dioxide,ozone,us_aqi&"
    f"past_days={past_days}"
)

print(f"[{version.upper()}] Starting Air Quality data ingestion for {city}...")
print(f"[{version.upper()}] Querying URL: {api_url}")

# Ensure artifacts directories exist
artifact_dir = os.path.join("artifacts", version)
os.makedirs(artifact_dir, exist_ok=True)
os.makedirs("artifacts", exist_ok=True)

# Fetch data from API
response = requests.get(api_url, timeout=15)
print(f"[{version.upper()}] API response status:", response.status_code)
response.raise_for_status()

raw_data = response.json()
hourly_records = len(raw_data.get("hourly", {}).get("time", []))
print(f"[{version.upper()}] Records received: {hourly_records} hourly data points")

# Metadata tag
raw_data["_metadata"] = {
    "version": version,
    "city": city,
    "latitude": lat,
    "longitude": lon,
    "past_days": past_days,
    "total_records": hourly_records
}

# Save versioned artifact
versioned_path = os.path.join(artifact_dir, "raw_data.json")
with open(versioned_path, "w") as f:
    json.dump(raw_data, f, indent=4)

# Also save to base artifacts folder for quick access
base_path = os.path.join("artifacts", "raw_data.json")
with open(base_path, "w") as f:
    json.dump(raw_data, f, indent=4)

print(f"[{version.upper()}] SUCCESS!")
print(f"[{version.upper()}] Artifact created: {versioned_path}")
