from flask import Flask, request, render_template
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)
DB = "data.db"


def get_latest_metric(metric_name, device_name):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT value
    FROM readings
    WHERE metric = ? AND device=?
    ORDER BY id DESC
    LIMIT 1
    """, (metric_name, device_name))

    row = cursor.fetchone()
    conn.close()

    value = row[0] if row is not None else None
    return value


@app.route("/api/latest")
def latest_data():
    return {
        "esp32_1": {
            "temperature": get_latest_metric("temperature", "esp32_1"),
            "humidity": get_latest_metric("humidity", "esp32_1"),
        },
        "pi": {
            "cpu_temp": get_latest_metric("cpu_temp", "pi"),
            "ram_usage": get_latest_metric("ram_usage", "pi"),
            "disk_usage": get_latest_metric("disk_usage", "pi")
        }
    }


@app.route("/api/history")
def history():
    metric = request.args.get("metric")
    device = request.args.get("device")
    period = request.args.get("period", "24h")

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    now = datetime.utcnow()

    if period == "1h":
        start_time = now - timedelta(hours=1)
    elif period == "24h":
        start_time = now - timedelta(days=1)
    elif period == "7d":
        start_time = now - timedelta(days=7)
    else:
        start_time = now - timedelta(days=1)

    cursor.execute("""
        SELECT timestamp, value
        FROM readings
        WHERE metric = ?
        AND device = ?
        AND timestamp >= ?
        ORDER BY timestamp ASC
    """, (metric, device, start_time.isoformat()))

    rows = cursor.fetchall()
    conn.close()

    return {
        "data": rows
    }


@app.route("/")
def home():
    return render_template("index.html")


app.run(host="0.0.0.0", port=5000)
