import requests

url = "https://jsonplaceholder.typicode.com/users"

response = requests.get(url)

print("Status code:", response.status_code)

data = response.json()

print("Number of records:", len(data))

print("\nFirst record:")
print(data[0])