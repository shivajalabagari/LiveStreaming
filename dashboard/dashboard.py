import requests

API_URL = "http://localhost:5000/metrics"  # Change from "http://dashboard:5000"

def fetch_data():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()  # Raises an error for HTTP failures
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to fetch data: {e}")
        return {}

if __name__ == "__main__":
    print(fetch_data())
