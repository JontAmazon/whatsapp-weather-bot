"""
weather_bot_dev.py

Like weather_bot.py, except only for a selected few users, e.g. only myself?
"""
import os
from db import get_all_subscribers
from weather_bot_utils import send_to_subscribers, DB_PATH
from dotenv import load_dotenv
load_dotenv()

RECIPIENTS = []
RECIPIENTS.append(os.getenv("WHATSAPP_TO"))  # my phone number
# RECIPIENTS.append("whatsapp:+46761234567") # another number to test with

# Fetch all subscribers from DB, then filter by RECIPIENTS
all_subs = get_all_subscribers(DB_PATH)
recipients = [sub for sub in all_subs if sub['phone_number'] in RECIPIENTS]
print(f"{recipients=}")

if not recipients:
    print(f"No subscribers found that had matching phone number with any number in {RECIPIENTS=}.")
else:
    for sub in recipients:
        send_to_subscribers(recipients)
