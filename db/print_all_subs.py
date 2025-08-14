import sqlite3
import os

def print_all_subscribers():
    """Fetch and print all subscribers from the database."""

    import os
    import sqlite3

    # Path to the database
    db_path = os.getenv("DB_PATH", "db/subscribers.db")

    # Connect to the database
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Fetch all subscribers
    cur.execute("SELECT * FROM subscribers")
    rows = cur.fetchall()

    # If table has rows, print them
    if rows:
        print("All subscribers:")
        for row in rows:
            print(row)
    else:
        print("No subscribers found.")

    # Close connection
    conn.close()


if __name__ == "__main__":
    print_all_subscribers()
