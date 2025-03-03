import random
import time
import json
from kafka import KafkaProducer
from kafka.errors import KafkaError

KAFKA_TOPIC = "user_interactions"
KAFKA_BROKER = "localhost:9092"

# Adding retries and exception handling
while True:
    try:
        producer = KafkaProducer(
            bootstrap_servers=KAFKA_BROKER,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            retries=5
        )
        print("✅ Successfully connected to Kafka")
        break
    except KafkaError as e:
        print(f"❌ Failed to connect to Kafka: {e}")
        time.sleep(5)  # Wait before retrying


def generate_interaction():
    return {
        "user_id": random.randint(1, 100),
        "item_id": random.randint(1, 50),
        "interaction_type": random.choice(["click", "view", "purchase"]),
        "timestamp": int(time.time())
    }

while True:
    interaction = generate_interaction()
    try:
        producer.send(KAFKA_TOPIC, interaction)
        print(f"Produced: {interaction}")
    except KafkaError as e:
        print(f"❌ Failed to send message: {e}")
    time.sleep(random.uniform(0.5, 2))
