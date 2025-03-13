import json
import requests
from kafka import KafkaProducer
import time

# Kafka Configuration
KAFKA_BROKER = "localhost:9092"
KAFKA_TOPIC = "random_data"

# API to fetch random user data
API_URL = "https://randomuser.me/api/?results=5"

def fetch_random_data():
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            user_data = response.json()
            print(f"Raw API Response: {json.dumps(user_data, indent=2)}")  # Debugging
            
            if "results" in user_data and user_data["results"]:
                users = user_data["results"]
                formatted_users = []
                
                for user in users:
                    formatted_user = {
                        "user_id": user.get("login", {}).get("uuid", "unknown"),  # Unique user ID
                        "name": f"{user.get('name', {}).get('first', 'Unknown')} {user.get('name', {}).get('last', 'Unknown')}",
                        "interaction_type": "generated",
                        "timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime()),  # Adding formatted timestamp
                        "email": user.get("email", "Unknown Email"),
                        "location": f"{user.get('location', {}).get('city', 'Unknown')}, {user.get('location', {}).get('country', 'Unknown')}",
                        "age": user.get("dob", {}).get("age", "Unknown Age")
                    }
                    formatted_users.append(formatted_user)
                
                return formatted_users
            
            print("No user data found.")
        else:
            print(f"Error fetching data: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Exception occurred: {e}")
    return None

# Kafka Producer Setup
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def produce_messages(rate=1):
    while True:
        users = fetch_random_data()
        if users:
            for user in users:
                producer.send(KAFKA_TOPIC, value=user)
                print(f"Sent: {user}")
        time.sleep(10)  # Fetch every 10 seconds

if __name__ == "__main__":
    produce_messages(rate=2)  # Adjust rate as needed