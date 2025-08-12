import sqlite3
import os

def print_all_subscribers():
    """Fetch and print all subscribers from the database."""

    db_path = os.getenv("DB_PATH", "db/subscribers.db")

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Check if the table exists
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='subscribers';")
    table_exists = cur.fetchone()

    if table_exists:
        print("Table 'subscribers' exists.")

        # Now fetch subscribers
        cur.execute("SELECT * FROM subscribers")
        rows = cur.fetchall()

        if not rows:
            print("No subscribers found.")
        else:
            for row in rows:
                print(row)

    else:
        print("Table 'subscribers' does NOT exist.")

    conn.close()

if __name__ == "__main__":
    print_all_subscribers()
