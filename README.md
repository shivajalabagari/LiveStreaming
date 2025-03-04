# Data Engineer Hiring Case Study

## 📌 Overview

This project is a **real-time data pipeline** designed to simulate user interactions, stream them through Kafka, process them with real-time aggregations, and visualize the results using a Flask-based dashboard.

## 📂 Project Structure

| Directory/File         | Description                                   |
| ---------------------- | --------------------------------------------- |
| **config/**            | Configuration files for MongoDB and Kafka     |
| ├── db_config.py      | Configuration for MongoDB                     |
| ├── kafka_config.py   | Kafka connection settings                     |
| **dashboard/**         | Contains dashboard-related files              |
| ├── templates/        | Stores HTML templates                         |
| │   ├── index.html    | Frontend UI for real-time visualization       |
| ├── app.py            | Flask application setup                       |
| ├── dashboard.py      | Dashboard logic to fetch aggregated data      |
| **.gitignore**         | Specifies files to ignore in version control  |
| **.gitpod.yml**        | Gitpod environment configuration              |
| **consumer.py**        | Kafka consumer for real-time processing       |
| **data_generator.py**  | Generates random interaction data             |
| **producer.py**        | Kafka producer publishing data to Kafka topic |
| **docker-compose.yml** | Docker setup for running services             |
| **requirements.txt**   | Python dependencies                           |
| **setup.sh**           | Setup script to initialize environment        |

---

## 🚀 Features

1. **Data Generation & Kafka Streaming**
   - Generates simulated interaction data (user_id, item_id, interaction_type, timestamp).
   - Publishes data to Kafka topic at a controlled rate.

2. **Real-time Data Processing & NoSQL Storage**
   - Kafka consumer fetches and aggregates data (average interactions per user, min/max interactions per item).
   - Stores processed data in **MongoDB**.

3. **Interactive Dashboard for Visualization**
   - Fetches aggregated data from MongoDB.
   - Displays real-time analytics using a Flask-powered web dashboard.

---

## 📦 Tech Stack

- **Kafka** - Message streaming
- **MongoDB** - NoSQL storage
- **Flask** - Web framework
- **Docker** - Containerized deployment
- **Gitpod/GitHub** - Development environment

---

## 🛠️ Setup & Installation

### Prerequisites

Ensure you have the following installed:

- Docker & Docker Compose
- Python 3.8+
- Kafka & Zookeeper
- MongoDB

### Login to GITPOD

1️⃣ Open Gitpod using the following link:
   [Gitpod Workspace](https://gitpod.io/#https://github.com/shivajalabagari/dataengineer_casestudy)

2️⃣ Select `PyCharm 2025.1`

3️⃣ Choose the standard configuration:
   - **Class:** Up to 4 Cores
   - **Memory:** 8GB RAM
   - **Storage:** 30GB

### Installation Steps

1️⃣ Clone the repository:
```bash
git clone <repo-url>
cd <project-folder>
```

2️⃣ Install dependencies:
```bash
pip install -r requirements.txt
```

3️⃣ Start the services using Docker:
```bash
docker-compose up -d
```

4️⃣ Stop the services:
```bash
docker-compose down
```

5️⃣ Start the Flask application manually (if needed):
```bash
python dashboard/app.py
```

6️⃣ Run the Kafka producer:
```bash
python producer.py
```

7️⃣ Start the Kafka consumer:
```bash
python consumer.py
```

8️⃣ Launch the Flask dashboard:
```bash
python dashboard/dashboard.py
```

9️⃣ Open the browser and visit:
```
http://localhost:5000
```

---

## 📊 Dashboard Metrics

- **Average Interactions per User** 📈
- **Max & Min Interactions per Item** 🔢
- **Live Updates with New Data** 🔄

---
🤝 Contribution

Feel free to fork this repository, create feature branches, and submit PRs. Suggestions and feedback are always welcome! 🎉


