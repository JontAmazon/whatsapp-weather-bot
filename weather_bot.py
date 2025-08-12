"""
weather_bot.py

A WhatsApp weather bot that sends daily weather
to a specified phone number updates using Twilio.

- Sends today's or tomorrow's weather forecast (argument).
- Retrieves and formats weather data including
  temperature, sun hours, wind, rain, and cloudiness.
"""

import os
import time
import json
from dotenv import load_dotenv
from twilio.rest import Client
from fetch_weather import fetch_weather

# Load environment variables
load_dotenv()

# Twilio setup
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
whatsapp_from = os.getenv("WHATSAPP_FROM")
# whatsapp_to = os.getenv("WHATSAPP_TO")
twilio_client = Client(account_sid, auth_token)


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
    
    # tmp solution: load subscribers from JSON file
    with open('database/tmp-json/subscribers.json', 'r') as f:
        subscribers = json.load(f)

        counter = 0
        for subscriber in subscribers:

            # if counter >= 1:  # for testing, only send to one subscriber
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
