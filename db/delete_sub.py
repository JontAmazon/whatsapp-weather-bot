import sqlite3
import os

phone_to_delete = "+46760944048"

db_path = os.getenv("DB_PATH", "db/subscribers.db")

conn = sqlite3.connect(db_path)
cur = conn.cursor()


cur.execute("DELETE FROM subscribers WHERE phone_number = ?", (phone_to_delete,))
conn.commit()

print(f"Deleted subscriber with phone number {phone_to_delete}.")

conn.close()
