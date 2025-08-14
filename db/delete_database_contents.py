import sqlite3
import os

db_path = os.getenv("DB_PATH", "db/subscribers.db")

conn = sqlite3.connect(db_path)
cur = conn.cursor()

# Fetch all rows first
cur.execute("SELECT * FROM subscribers")
subscribers = cur.fetchall()

if subscribers:
    print("Deleting all subscribers:")
    for sub in subscribers:
        print(sub)
    
    cur.execute("DELETE FROM subscribers")
    conn.commit()
    print(f"Deleted {len(subscribers)} subscribers.")
else:
    print("No subscribers found. Nothing to delete.")

conn.close()
