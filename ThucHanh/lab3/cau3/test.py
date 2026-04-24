import requests

for i in range(5):
    r = requests.get("http://localhost:8080")
    print(f"Request {i+1}: {r.text}")