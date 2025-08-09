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
import argparse
import json
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta
from datetime import time as dtime
from twilio.rest import Client
from collections import Counter

from stop_fly_machine import stop_machine

# Load environment variables
load_dotenv()

# Twilio setup
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
whatsapp_from = os.getenv("WHATSAPP_FROM")
whatsapp_to = os.getenv("WHATSAPP_TO")
twilio_client = Client(account_sid, auth_token)

# Weather setup
weather_api_key = os.getenv("WEATHER_API_KEY")
lat = os.getenv("LAT")
lon = os.getenv("LON")
tomorrow = os.getenv("TOMORROW", ) or False
weather_url = "https://api.openweathermap.org/data/2.5/forecast"


def fetch_weather():
    """ Fetch weather data from api.openweathermap.org,
    then just do a bunch of formatting etc.
    
    :return: String. Example:
        Weather tomorrow:
        - Clouds / Clear
        - Sun: 6h
        - 21° / 16°
        - No rain :)
        - Clouds: 40.6
        - Wind: 5 - 3 m/s
        - Gust: 6 - 4 m/s
    """
    params = {
        "lat": lat,
        "lon": lon,
        "appid": weather_api_key,
        "units": "metric"
    }


    # -------------------------------------------------
    # TODO later: separate function/file.
    try:
        response = requests.get(weather_url, params=params)
        response.raise_for_status()  # Raises HTTPError for 4xx/5xx responses
    except requests.exceptions.HTTPError as http_err:
        status = response.status_code
        if 400 <= status < 500:
            print(f"Client error: {status} - {response.text}")
        elif 500 <= status < 600:
            print(f"Server error: {status} - {response.text}")
        else:
            print(f"Unexpected HTTP error: {http_err}")
    except requests.exceptions.RequestException as err:
        print(f"Request failed: {err}")
    else:
        data = response.json()
        # print(f"\n\n{data=}\n\n")
    # -------------------------------------------------


    # today or tomorrow?
    if tomorrow:
        target_date = (datetime.now() + timedelta(days=1)).date()
    else:
        target_date = datetime.now().date()

    sun_hours = 0
    temps = []
    winds = []
    gusts = []
    rains = []
    clouds = []
    weather_type = []

    for item in data["list"]:
        time = datetime.fromtimestamp(item["dt"])
        if time.date() != target_date:
            continue
        if time.time().hour < 7 or time.time().hour > 22:
            # not such an interesting interval --> skip!
            continue
        temps.append(item["main"]["temp"])
        winds.append(item["wind"]["speed"])
        rains.append(item.get("rain", {}).get("3h", 0))
        gusts.append(item["wind"].get("gust", {0}))
        clouds.append(item["clouds"]["all"])
        weather_type_3h = item["weather"][0]["main"]
        print(f"{time.time()}: {weather_type_3h=}")
        weather_type.append(weather_type_3h)
        if weather_type_3h == "Clear":
            sun_hours += 3

    if not temps:
        return "No weather data available."

    avg_wind = sum(winds) / len(winds)
    avg_rain = sum(rains) / len(rains) if rains else 0
    avg_clouds = sum(clouds) / len(clouds)

    counts = Counter(weather_type)
    most_common = counts.most_common(2)
    most_common1 = most_common[0][0]
    if len(most_common) > 1:
        most_common2 = most_common[1][0]
    else:
        most_common2 = None

    day = "tomorrow" if tomorrow else "today"
    msg = f"🌤 Weather {day}:\n"
    # msg = f"🌤 Weather {target_date}:\n"
    if most_common2:
        msg += f"- {most_common1} / {most_common2}\n"
    else:
        msg += f"- {most_common1} \n"
    msg += f"- {round(max(temps))}° / {round(min(temps))}°\n"
    msg += f"- Sun: *{sun_hours}h*\n"
    if round(avg_rain) == 0:
        msg += f"- No rain :)\n"
    else:
        # msg += f"- Rain: {max(rains)} / {min(rains)} // {avg_rain} mm\n"
        msg += f"- Max rain: {max(rains)} mm\n"
        msg += f"- Avg rain: {round(avg_rain)} mm\n"
    msg += f"- Clouds: {round(avg_clouds)}\n\n"

    msg += f"- Wind: {round(max(winds))} - {round(min(winds))} m/s\n"
    msg += f"- Gust: {round(max(gusts))} - {round(min(gusts))} m/s\n"

    return msg

def send_weather_message():
    try:
        body = fetch_weather()
        # print(f"[DEBUG] fetch_weather returned type={type(body)} value={repr(body)}")
        if not body:
            raise ValueError("Weather body is empty or None")

        print(f"Sending WhatsApp message from {whatsapp_from} to {whatsapp_to}.")
        message = twilio_client.messages.create(
            body=body,
            from_=whatsapp_from,
            to=whatsapp_to
        )

        print(f"[DEBUG] Twilio response SID={message.sid}")
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

    # note: uncommented code to stop fly machine,
    # see notes in notes/stop_fly_machine.md
