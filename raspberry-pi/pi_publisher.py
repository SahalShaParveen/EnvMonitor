import paho.mqtt.client as mqtt
import psutil
import json
import time
from config import CONFIG

BROKER = CONFIG["mqtt"]["broker"]
PORT = CONFIG["mqtt"]["port"]
TOPIC = CONFIG["devices"]["pi"]["mqtt_topic"]

TEMPERATURE_PATH = "/sys/devices/virtual/thermal/thermal_zone0/temp"


def get_cpu_temp():
    with open(TEMPERATURE_PATH) as f:
        temperature = int(f.read()) / 1000
    return temperature


def on_connect(client, userdata, flags, rc):
    print("Connected with result code", rc)


client = mqtt.Client()
client.on_connect = on_connect

client.connect(BROKER, PORT, 60)
client.loop_start()

METRIC_READERS = {
    "cpu_temp": get_cpu_temp,
    "ram_usage": lambda: psutil.virtual_memory().percent,
    "disk_usage": lambda: psutil.disk_usage("/").percent
}

try:
    while True:
        payload = {}

        for metric in CONFIG["devices"]["pi"]["metrics"]:
            payload[metric] = METRIC_READERS[metric]()

        print("publishing: ", payload)
        client.publish(TOPIC, json.dumps(payload))
        time.sleep(CONFIG["devices"]["pi"]["update_interval"])
except KeyboardInterrupt:
    print("stopping")
finally:
    client.disconnect()
