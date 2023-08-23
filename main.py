from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
import redis
from datetime import datetime
import json

app = FastAPI()

mongo_client = MongoClient("mongodb://mongodb:27017/")
db = mongo_client["sensor_data"]
db_collection = db["temperature"]

redis_client = redis.Redis(host="redis", port=6379, db=0)


@app.get("/sensor_readings")
def get_sensor_readings(start: str, end: str):
    start_time = datetime.fromisoformat(start)
    end_time = datetime.fromisoformat(end)

    readings = db_collection.find({
        "timestamp": {"$gte": start_time, "$lte": end_time}
    })

    return list(readings)


@app.get("/last_ten_readings/{sensor_id}")
def get_last_ten_readings(sensor_id: str):
    cached_readings = redis_client.lrange(sensor_id, 0, 9)
    return [json.loads(reading) for reading in cached_readings]
