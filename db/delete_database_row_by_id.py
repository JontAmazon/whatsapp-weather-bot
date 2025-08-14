import sqlite3
import os

id_to_delete = 1337  # int (I think, otherwise try string)

db_path = os.getenv("DB_PATH", "db/subscribers.db")

conn = sqlite3.connect(db_path)
cur = conn.cursor()

cur.execute("SELECT * FROM subscribers WHERE id = ?", (id_to_delete,))
subscriber = cur.fetchone()

if subscriber:
    print("Deleting subscriber:", subscriber)
    cur.execute("DELETE FROM subscribers WHERE id = ?", (id_to_delete,))
    conn.commit()
    print(f"Subscriber with id {id_to_delete} deleted.")
else:
    print(f"No subscriber found with id {id_to_delete}.")

conn.close()
