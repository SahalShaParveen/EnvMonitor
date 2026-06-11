from flask import Flask
import sqlite3

app = Flask(__name__)
DB = "data.db"


def get_latest():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT timestamp, device, metric, value
    FROM readings
    ORDER by id DESC
    LIMIT 1                               
    """)

    row = cursor.fetchone()
    conn.close()

    return row


@app.route("/")
def home():
    row = get_latest()

    if row is None:
        return "No data yet."

    timestamp, device, metric, value = row

    return f"""
        <h1>IoT Monitor</h1>
        <p><b>Device:</b> {device}</p>
        <p><b>Metric:</b> {metric}</p>
        <p><b>Value:</b> {value}</p>
        <p><b>Time:</b> {timestamp}</p>
    """


app.run(host="0.0.0.0", port=5000)
