## consumer.py
```python
import json
from kafka import KafkaConsumer
from pymongo import MongoClient

consumer = KafkaConsumer(
    "user_interactions", 
    bootstrap_servers="localhost:9092", 
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

client = MongoClient("mongodb://localhost:27017/")
db = client["interaction_db"]
collection = db["aggregations"]

for message in consumer:
    data = message.value
    collection.update_one(
        {"user_id": data["user_id"]},
        {"$inc": {"total_interactions": 1}},
        upsert=True
    )
    print(f"Updated MongoDB: {data}")
