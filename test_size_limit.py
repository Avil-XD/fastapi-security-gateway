import requests
import json

# Create a payload just over 1MB
data = {
    "data": "x" * (1024 * 1024 + 1)  # 1MB + 1 byte
}

try:
    response = requests.post(
        "http://127.0.0.1:8000/api/test",
        headers={"Content-Type": "application/json"},
        data=json.dumps(data)
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")