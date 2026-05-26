import paho.mqtt.client as mqtt
import json
import csv
from datetime import datetime

BROKER = "localhost"
TOPIC = "test"

CSV_FILE = "data/environment_log.csv"


def on_connect(client, userdata, flags, rc):
    print("Connected with result code: ", rc)
    client.subscribe(TOPIC)


def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode())

    timestamp = datetime.now().isoformat()
    temperature = payload.get("temperature")
    humidity = payload.get("humidity")

    print(timestamp, temperature, humidity)

    with open(CSV_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, temperature, humidity])


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, 1883, 60)
client.loop_forever()
