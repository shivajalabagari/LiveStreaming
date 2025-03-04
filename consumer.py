import json
import time
from kafka import KafkaConsumer
from pymongo import MongoClient
from datetime import datetime

KAFKA_TOPIC = "user_interactions"
KAFKA_BROKER = "localhost:9092"
MONGO_URI = "mongodb://localhost:27017/"
MONGO_DB = "interaction_db"
MONGO_COLLECTION = "aggregations"

consumer = KafkaConsumer(
    KAFKA_TOPIC, 
    bootstrap_servers=KAFKA_BROKER, 
    auto_offset_reset='earliest', 
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]

# Dictionary to track user and item-based aggregations
user_aggregations = {}
item_aggregations = {}

# Serial number counter for sequence number
sequence_number = 1

for message in consumer:
    data = message.value
    user_id = data["user_id"]
    item_id = data["item_id"]
    interaction_type = data["interaction_type"]
    interaction_timestamp = data["timestamp"]  # The timestamp of the interaction

    # Add the processed timestamp when the consumer processes the message
    processed_timestamp = int(time.time())  # Current time in seconds since epoch

    # Add sequence number to the interaction
    interaction = {**data, "sequence_number": sequence_number, "processed_timestamp": processed_timestamp}

    # User aggregation: total interactions and unique items
    if user_id not in user_aggregations:
        user_aggregations[user_id] = {
            "total_interactions": 0, 
            "unique_items": set(), 
            "last_interaction_time": 0  # Track the last interaction timestamp
        }
    
    user_aggregations[user_id]["total_interactions"] += 1
    user_aggregations[user_id]["unique_items"].add(item_id)
    user_aggregations[user_id]["last_interaction_time"] = max(user_aggregations[user_id]["last_interaction_time"], interaction_timestamp)

    # Item aggregation: max and min interactions per item
    if item_id not in item_aggregations:
        item_aggregations[item_id] = {
            "max_interactions": 0, 
            "min_interactions": float('inf'), 
            "last_interaction_time": 0  # Track the last interaction timestamp
        }
    
    # Update max/min interactions for items
    item_aggregations[item_id]["max_interactions"] = max(item_aggregations[item_id]["max_interactions"], 1)
    item_aggregations[item_id]["min_interactions"] = min(item_aggregations[item_id]["min_interactions"], 1)
    item_aggregations[item_id]["last_interaction_time"] = max(item_aggregations[item_id]["last_interaction_time"], interaction_timestamp)

    # Update MongoDB with the aggregated data
    collection.update_one(
        {"user_id": user_id},
        {"$set": {
            "total_interactions": user_aggregations[user_id]["total_interactions"],
            "unique_items": list(user_aggregations[user_id]["unique_items"]),
            "last_interaction_time": user_aggregations[user_id]["last_interaction_time"],
            "serial_number": sequence_number,
            "processed_timestamp": processed_timestamp  # Storing processed timestamp in MongoDB
        }},
        upsert=True
    )
    
    collection.update_one(
        {"item_id": item_id},
        {"$set": {
            "max_interactions": item_aggregations[item_id]["max_interactions"],
            "min_interactions": item_aggregations[item_id]["min_interactions"],
            "last_interaction_time": item_aggregations[item_id]["last_interaction_time"],
            "serial_number": sequence_number,
            "processed_timestamp": processed_timestamp  # Storing processed timestamp in MongoDB
        }},
        upsert=True
    )

    # Increment sequence number for the next interaction
    sequence_number += 1

    # Print for debugging
    print(f"Processed interaction {sequence_number - 1}: {interaction}")
