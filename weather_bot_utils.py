import os
from twilio.rest import Client
from fetch_weather import fetch_weather

DB_PATH = os.environ.get("DB_PATH", "/data/subscribers.db")
TWILIO_FROM = os.getenv("WHATSAPP_FROM")
TWILIO_CLIENT = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))

# Forecast for today or tomorrow? :
tomorrow_str = os.getenv("TOMORROW", None)
if tomorrow_str:
    TOMORROW = tomorrow_str.lower() == "true"
else:
    TOMORROW = True  # default

def send_weather_message(whatsapp_to: str, weather_forecast: str):
    try:
        print(f"[INFO] Sending WhatsApp message from {TWILIO_FROM} to {whatsapp_to}.")
        TWILIO_CLIENT.messages.create(
            body=weather_forecast,
            from_=TWILIO_FROM,
            to=whatsapp_to
        )
        print("[INFO] Message sent successfully.")
    except Exception as e:
        print(f"[ERROR] Failed sending to {whatsapp_to}: {e}")
        # don't raise

def send_to_subscribers(subscribers):
    for sub in subscribers:
        nbr_days = sub.get('forecast_days', 1)  # not implemented yet
        forecast = fetch_weather(sub['location'], sub['lon'], sub['lat'], TOMORROW, nbr_days)
        send_weather_message(sub['phone_number'], forecast)
