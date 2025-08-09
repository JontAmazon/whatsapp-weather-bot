"""
weather_bot.py

A WhatsApp weather bot that sends daily weather
to a specified phone number updates using Twilio.

- Sends today's or tomorrow's weather forecast (argument).
- Retrieves and formats weather data including
  temperature, sun hours, wind, rain, and cloudiness.
"""

import os
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
whatsapp_to = os.getenv("WHATSAPP_TO")
twilio_client = Client(account_sid, auth_token)


def send_weather_message():
    try:
        weather_message = fetch_weather() # nicely formatted weather message
        if not weather_message:
            raise ValueError("Weather body is empty or None")

        print(f"Sending WhatsApp message from {whatsapp_from} to {whatsapp_to}.")
        message = twilio_client.messages.create(
            body=weather_message,
            from_=whatsapp_from,
            to=whatsapp_to
        )
        # print(f"[DEBUG] Twilio response SID={message.sid}")
        print("[INFO] Message sent successfully.")

    except Exception as e:
        print("[ERROR] send_weather_message failed!")
        print(f"[ERROR] Exception type: {type(e).__name__}")
        print(f"[ERROR] Exception message: {str(e)}")
        # print("[ERROR] Full traceback:")
        # traceback.print_exc()
        print("[DEBUG] Locals snapshot:")
        print(json.dumps({k: repr(v) for k, v in locals().items()}, indent=2))

if __name__ == "__main__":
    
    send_weather_message()
