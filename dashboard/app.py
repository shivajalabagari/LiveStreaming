from flask import Flask, jsonify, render_template
from pymongo import MongoClient

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["interaction_db"]
collection = db["aggregations"]

@app.route("/metrics", methods=["GET"])
def get_metrics():
    """Fetch aggregated interaction metrics from MongoDB"""
    data = list(collection.find({}, {"_id": 0}))
    return jsonify(data)

@app.route("/")
def index():
    """Render the real-time dashboard page"""
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
