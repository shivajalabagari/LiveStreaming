import json
from kafka import KafkaConsumer
from pymongo import MongoClient

# Kafka Configuration
KAFKA_TOPIC = "random_data"
KAFKA_BROKER = "localhost:9092"

# MongoDB Configuration
MONGO_URI = "mongodb://localhost:27017/"
MONGO_DB = "interaction_db"
MONGO_COLLECTION = "aggregations"

# Kafka Consumer Setup
consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

# MongoDB Connection
client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]

print("✅ Kafka Consumer is running...")

for message in consumer:
    data = message.value
    user_id = data.get("user_id", "unknown")
    item_id = data.get("item_id", "unknown")
    name = data.get("name", "Unknown")
    location = data.get("location", "Unknown")
    age = data.get("age", "Unknown")
    timestamp = data.get("timestamp", "Unknown")

    # Update MongoDB with aggregated data
    collection.update_one(
        {"user_id": user_id},
        {"$set": {
            "name": name,
            "item_id": item_id,
            "location": location,
            "age": age,
            "timestamp": timestamp,
            "total_interactions": 1
        }},
        upsert=True
    )

    print(f"✅ Processed Message: {data}")