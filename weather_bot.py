"""
weather_bot.py

A WhatsApp weather bot that sends weather forecasts
to all subscribed phone numbers using Twilio.

Important:
 - Configure DB_PATH env var to point at the SQLite file (same path used by Flask app).
 - If running in GitHub Actions, ensure the job has access to the DB file (or you can expose
   an API endpoint to fetch subscribers instead). # NOTE: va???
"""
# Future improvements:
"""
- message based on preferences?
- hourly cron jobs, and handle time zones?
"""

import os
import time
import json
from dotenv import load_dotenv
from typing import Dict, Any
from twilio.rest import Client
from fetch_weather import fetch_weather
from db import get_all_subscribers

# Load environment variables
load_dotenv()

# Twilio setup
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
whatsapp_from = os.getenv("WHATSAPP_FROM")
# whatsapp_to = os.getenv("WHATSAPP_TO")
twilio_client = Client(account_sid, auth_token)

DB_PATH = os.environ.get("DB_PATH", "/data/subscribers.db")

def send_weather_message(whatsapp_to: str, weather_forecast: str):
    try:
        print(f"Sending WhatsApp message from {whatsapp_from} to {whatsapp_to}.")
        message = twilio_client.messages.create(
            body=weather_forecast,
            from_=whatsapp_from,
            to=whatsapp_to
        )
        print("[INFO] Message sent successfully.")
    except Exception as e:
        print("[ERROR] send_weather_message failed!")
        print(f"[ERROR] Exception type: {type(e).__name__}")
        print(f"[ERROR] Exception message: {str(e)}")

        # tmp
        print(f"{whatsapp_from=}")
        print(f"{whatsapp_to=}")
        print("len(weather_forecast):")
        print(len(weather_forecast))

        # print("[ERROR] Full traceback:") # keep this?
        # e.__traceback__.print_exc()      # keep this?
        # print("[DEBUG] Locals snapshot:") # keep this???
        # print(json.dumps({k: repr(v) for k, v in locals().items()}, indent=2))


if __name__ == "__main__":
    for _ in range(10):
        print()
    for _ in range(10):
        print("weather_bot starting — reading subscribers from DB:", DB_PATH)
    subscribers = get_all_subscribers(DB_PATH)
    print(f"Found {len(subscribers)} subscribers.")
    print(f"{subscribers=}")

    counter = 0
    for subscriber in subscribers:
        # TODO: consider continuing if subscriber X gets an error.

        # if counter >= 1:  # NOTE: for testing, only send to one subscriber
        #     break

        whatsapp_to = subscriber['phone_number']
        location = subscriber['location']
        lon = subscriber['lon']
        lat = subscriber['lat']
        tomorrow = True
            # TODO later: here's a way how to get "TOMORROW":
            # - cron job every hour
            # - check both "send_time_morning" and "send_time_evening", and sets
            # `TOMORROW` according to which one the current time matches with.
        forecast_days = subscriber.get('forecast_days', 1)
        
        # Fetch weather data
        try:
            weather_forecast = fetch_weather(location, lon, lat, tomorrow, forecast_days)
        except Exception as e:
            print(f"[ERROR] Exception in fetch_weather, for {subscriber=}\n{e}")
            raise

        # Send WhatsApp message
        send_weather_message(whatsapp_to, weather_forecast)

        counter = counter + 1
