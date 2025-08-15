""" To be run on Fly.io via GH Action "delete_database_row_by_id.yml". """
# Note to self: instead of GH action, I should make a script that uses SSH and does everything ^^
    # See print_all_subs2.py (WIP)
import sys
import os

# Add project root to sys.path
# Needed for GH Actions to find the db module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db import get_conn, get_all_subscribers

DB_PATH = os.environ.get("DB_PATH", "/data/subscribers.db")  # Fly volume default
print(f"{DB_PATH=}")

id_to_delete = 1  # should be an int, I think. Otherwise, try string.

subs = get_all_subscribers(DB_PATH)
print(f"Found {len(subs)} subscribers before deletion.")
print(f"{subs=}")

# Find the subscriber with the given ID
sub_to_delete = [sub for sub in subs if sub["id"] == id_to_delete]

if not sub_to_delete:
    print(f"No subscriber found with id={id_to_delete}. Nothing to delete.")
else:
    print(f"Deleting subscriber with id={id_to_delete}:")
    for sub in sub_to_delete:
        print(sub)

    conn = get_conn(DB_PATH)
    conn.execute("DELETE FROM subscribers WHERE id = ?", (id_to_delete,))
    conn.commit()
    conn.close()

    # Check results
    subs = get_all_subscribers(DB_PATH)
    print(f"Found {len(subs)} subscribers after deletion.")
    print(f"{subs=}")
