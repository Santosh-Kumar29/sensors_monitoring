import paho.mqtt.client as mqtt
import json
import time
from datetime import datetime


def on_publish(client, userdata, mid):
    print(f"Published message {mid}")


client = mqtt.Client()
client.connect("mosquitto", 1883)

while True:
    sensor_data = {
        "sensor_id": "sensor001",
        "value": str(round(20 + (time.time() % 5), 2)),
        "timestamp": datetime.now().isoformat()
    }
    payload = json.dumps(sensor_data)
    client.publish("sensors/temperature", payload)
    time.sleep(5)
