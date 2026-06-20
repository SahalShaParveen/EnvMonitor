from flask import Flask, request, render_template
import sqlite3
from datetime import datetime, timedelta, timezone
from config import CONFIG

app = Flask(__name__)
DB = CONFIG["database"]["filename"]

FRESHNESS_SECONDS = CONFIG["dashboard"]["freshness_seconds"]


def get_latest_metric(metric_name, device_name):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT value, timestamp
    FROM readings
    WHERE metric = ? AND device=?
    ORDER BY id DESC
    LIMIT 1
    """, (metric_name, device_name))

    row = cursor.fetchone()
    conn.close()

    if row is None:
        return None, None

    value = row[0]
    timestamp = row[1]

    return value, timestamp


def is_fresh(timestamp):
    if timestamp is None:
        return False

    last = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    now = datetime.now(timezone.utc)
    return (now - last) < timedelta(seconds=FRESHNESS_SECONDS)


@app.route("/api/latest")
def latest_data():
    data = {}

    for device_name, device_config in CONFIG["devices"].items():
        data[device_name] = {}
        for metric in device_config["metrics"]:
            value, value_ts = get_latest_metric(metric, device_name)
            fresh = is_fresh(value_ts)
            data[device_name][metric] = value if fresh else None

    return data


@app.route("/api/history")
def history():
    metric = request.args.get("metric")
    device = request.args.get("device")
    period = request.args.get("period", "24h")

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    now = datetime.now(timezone.utc)

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

    data = []

    for timestamp, value in rows:
        data.append({
            "x": timestamp,
            "y": value
        })

    return {
        "data": data
    }


@app.route("/api/config")
def config():
    return CONFIG


@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
