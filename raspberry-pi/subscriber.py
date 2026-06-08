import paho.mqtt.client as mqtt
import sqlite3
import json
from datetime import datetime, UTC

BROKER = "localhost"
TOPIC = "sensors/#"

conn = sqlite3.connect("data.db")
cursor = conn.cursor()


def insert_reading(device, metric, value):
    timestamp = datetime.now(UTC).isoformat()

    cursor.execute("""
    INSERT INTO readings (timestamp, device, metric, value)
    VALUES (?, ?, ?, ?)
    """, (timestamp, device, metric, value))

    conn.commit()


def close_db():
    conn.close()


def on_connect(client, userdata, flags, rc):
    print("Connected with result code: ", rc)
    print(f"Subscribing to {TOPIC}")
    client.subscribe(TOPIC)


def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
    except json.JSONDecodeError:
        print("Invalid JSON payload.")
        return

    device = msg.topic.split("/")[1]

    for metric, value in payload.items():
        print(f"[{device}] {metric} = {value}")
        insert_reading(device, metric, value)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, 1883, 60)
client.loop_forever()
