from weather_bot_utils import send_to_subscribers, DB_PATH
from db import get_all_subscribers

subs = get_all_subscribers(DB_PATH)
print(f"Found {len(subs)} subscribers in the database.")
print(f"{subs=}")

send_to_subscribers(subs)
