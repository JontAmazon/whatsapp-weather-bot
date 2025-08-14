import os
from db import get_all_subscribers

DB_PATH = os.environ.get("DB_PATH", "/data/subscribers.db")  # Fly volume default
print(f"{DB_PATH=}")

subs = get_all_subscribers(DB_PATH)

if not subs:
    print("No subscribers found.")
else:
    print(f"Found {len(subs)} subscribers:")
    for sub in subs:
        print(sub)
