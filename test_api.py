import requests

# Test Open-Meteo Air Quality API
CITY = "Mumbai"
LATITUDE = 19.0760
LONGITUDE = 72.8777
API_URL = (
    f"https://air-quality-api.open-meteo.com/v1/air-quality?"
    f"latitude={LATITUDE}&longitude={LONGITUDE}&"
    f"hourly=pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,sulphur_dioxide,ozone,us_aqi&"
    f"past_days=7"
)

print(f"Testing API connection for {CITY}...")
response = requests.get(API_URL, timeout=10)

print("Status code:", response.status_code)
response.raise_for_status()

data = response.json()
hourly_data = data.get("hourly", {})
time_records = hourly_data.get("time", [])

print("Number of hourly records received:", len(time_records))
print("Available metrics:", list(hourly_data.keys()))

print("\nSample first record:")
first_record = {key: hourly_data[key][0] for key in hourly_data.keys()}
print(first_record)

print("\nAPI connection test SUCCESSFUL!")
