# .gitignore
__pycache__/
*.log
*.db
*.sqlite
.env
venv/
.DS_Store

# README.md
# Data Engineer Hiring Case Study

## Overview
This project implements a real-time data pipeline that:
- Generates user interaction data.
- Streams it to Kafka.
- Consumes and aggregates it in MongoDB.
- Displays results on a dashboard.

## Setup Instructions
1. Install dependencies: `pip install -r requirements.txt`
2. Start Kafka, MongoDB, and services using `docker-compose up -d`
3. Run the data generator: `python data_generator.py`
4. Start the producer: `python producer.py`
5. Start the consumer: `python consumer.py`
6. Launch the dashboard: `python dashboard/app.py`

## Technologies Used
- Python
- Apache Kafka
- MongoDB
- Flask (for dashboard)
- Docker (for containerization)

## Folder Structure
```
.gitignore
README.md
docker-compose.yml
requirements.txt
setup.sh
data_generator.py
producer.py
consumer.py
dashboard/
    ├── app.py
    ├── dashboard.py
config/
    ├── kafka_config.py
    ├── db_config.py
```

---

# docker-compose.yml
version: '3.8'
services:
  zookeeper:
    image: confluentinc/cp-zookeeper:latest
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
  kafka:
    image: confluentinc/cp-kafka:latest
    depends_on:
      - zookeeper
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
    ports:
      - "9092:9092"
  mongo:
    image: mongo:latest
    ports:
      - "27017:27017"

---

# requirements.txt
flask
kafka-python
pymongo
docker

---

# setup.sh
#!/bin/bash
pip install -r requirements.txt
docker-compose up -d

---

# data_generator.py
import random
import time
import json
from kafka import KafkaProducer

KAFKA_TOPIC = "user_interactions"
KAFKA_BROKER = "localhost:9092"
producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER, value_serializer=lambda v: json.dumps(v).encode('utf-8'))

def generate_interaction():
    return {"user_id": random.randint(1, 100), "item_id": random.randint(1, 50), "interaction_type": random.choice(["click", "view", "purchase"]), "timestamp": int(time.time())}

while True:
    interaction = generate_interaction()
    producer.send(KAFKA_TOPIC, interaction)
    print(f"Produced: {interaction}")
    time.sleep(random.uniform(0.5, 2))

---

# producer.py
import json
from kafka import KafkaProducer
from data_generator import generate_interaction

KAFKA_TOPIC = "user_interactions"
KAFKA_BROKER = "localhost:9092"
producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER, value_serializer=lambda v: json.dumps(v).encode('utf-8'))

while True:
    interaction = generate_interaction()
    producer.send(KAFKA_TOPIC, interaction)
    print(f"Produced: {interaction}")

---

# consumer.py
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
    print(f"Consumed and Aggregated: {data}")

---

# dashboard/app.py
from flask import Flask, jsonify
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017/")
db = client["interaction_db"]
collection = db["aggregations"]

@app.route("/metrics", methods=["GET"])
def get_metrics():
    data = list(collection.find({}, {"_id": 0}))
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True, port=5000)

---

# dashboard/dashboard.py
import requests

def fetch_data():
    response = requests.get("http://localhost:5000/metrics")
    return response.json()

if __name__ == "__main__":
    print(fetch_data())

---

# config/kafka_config.py
KAFKA_BROKER = "localhost:9092"
KAFKA_TOPIC = "user_interactions"

---

# config/db_config.py
MONGO_URI = "mongodb://localhost:27017/"
MONGO_DB = "interaction_db"
MONGO_COLLECTION = "aggregations"