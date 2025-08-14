import sys
import os

# Add project root to sys.path
# Needed for GH Actions to find the db module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db import get_conn, get_all_subscribers

DB_PATH = os.environ.get("DB_PATH", "/data/subscribers.db")  # Fly volume default
print(f"{DB_PATH=}")

# Fetch subscribers first
subs = get_all_subscribers(DB_PATH)
print(f"Found {len(subs)} subscribers.")
print(f"{subs=}")

if not subs:
    print("No subscribers found. Nothing to delete.")
else:
    print("Deleting all subscribers:")
    for sub in subs:
        print(sub)

    conn = get_conn(DB_PATH)
    conn.execute("DELETE FROM subscribers")
    conn.commit()
    conn.close()

    subs = get_all_subscribers(DB_PATH)
    print(f"Found {len(subs)} subscribers after deleting.")
    print(f"{subs=}")
