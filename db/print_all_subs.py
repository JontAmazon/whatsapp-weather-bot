import sys
import os

# Add project root to sys.path
# Needed for GH Actions to find the db module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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
