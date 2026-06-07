import sqlite3
conn = sqlite3.connect("data.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS readings (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    timestamp TEXT NOT NULL, 
    device TEXT NOT NULL,
    metric TEXT NOT NULL,
    value REAL NOT NULL
)
""")

conn.commit()
conn.close()

print("Database intialised.")
