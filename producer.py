import json
from kafka import KafkaProducer
from data_generator import generate_interaction

KAFKA_TOPIC = "user_interactions"
KAFKA_BROKER = "localhost:9092"
producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER, value_serializer=lambda v: json.dumps(v).encode('utf-8'))

while True:
    producer.send(KAFKA_TOPIC, generate_interaction())