# Data Engineer:Case Study

## 📌 Overview
This project implements a real-time data pipeline that:
- Generates user interaction data.
- Streams the data to Apache Kafka.
- Consumes and aggregates it in MongoDB.
- Displays the results on a real-time dashboard.

## 🏗️ Architecture
1. **Data Generation:** A script generates random user interactions.
2. **Streaming:** Data is published to a Kafka topic.
3. **Processing & Aggregation:** A Kafka consumer reads messages, performs real-time aggregations, and stores results in MongoDB.
4. **Visualization:** A Flask-based dashboard fetches and displays real-time aggregated data.

## 🚀 Setup Instructions
### **1️⃣ Install Dependencies**
```sh
pip install -r requirements.txt
```

### **2️⃣ Start Services (Kafka, Zookeeper, MongoDB)**
```sh
docker-compose up -d
```

### **3️⃣ Run Data Generator (Kafka Producer)**
```sh
python data_generator.py
```

### **4️⃣ Start Kafka Consumer (Aggregations to MongoDB)**
```sh
python consumer.py
```

### **5️⃣ Launch Flask Dashboard**
```sh
python dashboard/app.py
```

### **6️⃣ Fetch Data from the Dashboard API**
```sh
python dashboard/dashboard.py
```

## 🔧 Technologies Used
- **Python** (Kafka Producer, Consumer, Flask API)
- **Apache Kafka** (Real-time message streaming)
- **MongoDB** (NoSQL storage for aggregations)
- **Flask** (Web API and dashboard visualization)
- **Docker** (Containerization of services)

## 📂 Folder Structure
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

## 📝 Configuration Files
### **Kafka Configuration (`config/kafka_config.py`)**
```python
KAFKA_BROKER = "localhost:9092"
KAFKA_TOPIC = "user_interactions"
```

### **MongoDB Configuration (`config/db_config.py`)**
```python
MONGO_URI = "mongodb://localhost:27017/"
MONGO_DB = "interaction_db"
MONGO_COLLECTION = "aggregations"
```

## 🔄 Docker Configuration (`docker-compose.yml`)
```yaml
version: '3.8'
services:
  zookeeper:
    image: confluentinc/cp-zookeeper:latest
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
    ports:
      - "2181:2181"

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
```

## 🎯 Key Features
✔️ **Scalable Kafka Producer & Consumer**
✔️ **Real-time Data Aggregation**
✔️ **Interactive Dashboard with Auto-Refreshing Metrics**
✔️ **Dockerized Deployment**

## 📌 Future Enhancements
- 📊 **Integrate Kibana or Grafana for better visualization**
- 🔔 **Add alerting for high interaction volumes**
- 📈 **Optimize Kafka consumer for higher throughput**

---
🚀 **This project demonstrates end-to-end real-time data processing, aggregation, and visualization.**
Let me know if you need any improvements! 🔥
