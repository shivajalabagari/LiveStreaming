import json
from kafka import KafkaConsumer
from pymongo import MongoClient

KAFKA_TOPIC = "user_interactions"
KAFKA_BROKER = "localhost:9092"
MONGO_URI = "mongodb://localhost:27017/"
MONGO_DB = "interaction_db"
MONGO_COLLECTION = "aggregations"
consumer = KafkaConsumer(KAFKA_TOPIC, bootstrap_servers=KAFKA_BROKER, auto_offset_reset='earliest', value_deserializer=lambda v: json.loads(v.decode('utf-8')))
client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]
aggregations = {}
for message in consumer:
    data = message.value
    user_id = data["user_id"]
    item_id = data["item_id"]
    if user_id not in aggregations:
        aggregations[user_id] = {"total_interactions": 0, "unique_items": set()}
    aggregations[user_id]["total_interactions"] += 1
    aggregations[user_id]["unique_items"].add(item_id)
    collection.update_one({"user_id": user_id}, {"$set": {"total_interactions": aggregations[user_id]["total_interactions"], "unique_items": list(aggregations[user_id]["unique_items"])}}, upsert=True)
