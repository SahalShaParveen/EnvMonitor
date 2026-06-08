import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

conn = sqlite3.connect("data.db")

df = pd.read_sql_query("""
    SELECT timestamp, value 
    FROM readings 
    WHERE device = 'esp32_1'
    AND metric = 'temperature' 
    ORDER BY timestamp 
""", conn)

df["timestamp"] = pd.to_datetime(df["timestamp"])

plt.plot(df["timestamp"], df["value"])
plt.show()
