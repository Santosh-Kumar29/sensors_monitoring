import paho.mqtt.client as mqtt
import json
from pymongo import MongoClient


def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe("sensors/temperature")


def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload)
        db_collection.insert_one(data)
        print("Message inserted into MongoDB:", data)
    except Exception as e:
        print("Error:", e)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("mosquitto", 1883)

mongo_client = MongoClient("mongodb://mongodb:27017/")
db = mongo_client["sensor_data"]
db_collection = db["temperature"]

client.loop_forever()
