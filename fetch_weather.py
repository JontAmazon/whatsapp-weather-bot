""" Function to return nicely formatted weather data from OpenWeatherMap API."""

import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta
from datetime import time as dtime
from collections import Counter

# Load environment variables
load_dotenv()
weather_api_key = os.getenv("WEATHER_API_KEY")
weather_url = "https://api.openweathermap.org/data/2.5/forecast"


def fetch_weather(location, lon, lat, tomorrow: bool, forecast_days: int) -> str:
    """ Fetch weather data from api.openweathermap.org and format it nicely.
    
    :param tomorrow: Boolean. If True, fetch weather for tomorrow, otherwise for today.
    :param forecast_days: Not yet implemented...

    :return: Example string:
        Weather tomorrow:
        - Clouds / Clear
        - 21° / 16°
        - No rain :)
        - Clouds: 40.6
        - Wind: 3 - 5 m/s
        - Gust: 4 - 6 m/s
    """

    params = {
        "lat": lat,
        "lon": lon,
        "appid": weather_api_key,
        "units": "metric"
    }

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
        print(f"[DEBUG] Response headers: {response.headers}") # tmp
        print(f"[DEBUG] First 500 chars of body: {response.text[:500]}") # tmp 

        data = response.json()
        # print(f"\n\n{data=}\n\n")

    # Define variables
    # sun_hours = 0; # if weather_type_3h == "Clear": sun_hours += 3
    temps = []
    winds = []
    gusts = []
    rains = []
    clouds = []
    weather_type = []
    weather_emoji = []
    time_of_day = []  # e.g. 09:00, 12:00, etc.

    # Filter the data for the target date
    if tomorrow:
        target_date = (datetime.now() + timedelta(days=1)).date()
    else:
        target_date = datetime.now().date()

    for item in data["list"]:
        dt = datetime.fromtimestamp(item["dt"])
        if dt.date() != target_date:
            continue
        if dt.time().hour < 7 or dt.time().hour > 22:
            # not such an interesting interval --> skip!
            continue
        temps.append(item["main"]["temp"])
        winds.append(item["wind"]["speed"])
        rains.append(item.get("rain", {}).get("3h", 0))
        gusts.append(item["wind"].get("gust", {0}))
        clouds.append(item["clouds"]["all"])
        weather_type.append(item["weather"][0]["main"])
        time_of_day.append(dt.time())

    if not temps:
        return "No weather data available."
    

    # Translate into emojis
    for weather_type_3h, hour_of_day in zip(weather_type, time_of_day):
        print(f"{hour_of_day}: {weather_type_3h=}")
        if weather_type_3h == "Clouds":
            weather_emoji.append("☁️")
        elif weather_type_3h == "Clear":
            weather_emoji.append("☀️")
        elif weather_type_3h == "Rain":
            weather_emoji.append("🌧")

    avg_clouds = sum(clouds) / len(clouds)
    avg_rain = sum(rains) / len(rains) if rains else 0
    avg_wind = sum(winds) / len(winds)

    ### ------------- Format the message ----------------
    which_day = "tomorrow" if tomorrow else "today"
    msg = f"🌤 {location} {which_day}:\n"
    # msg = f"{location} {which_day}:\n"  # use this one when emojis work?
    
    """ # message += weather emojis
    for emoji in weather_emoji:
        msg += emoji + " "
    msg += "\n"
    """
    
    """ # message += weather type in words
    counts = Counter(weather_type)
    most_common = counts.most_common(2)
    most_common1 = most_common[0][0]
    if len(most_common) > 1:
        most_common2 = most_common[1][0]
    else:
        most_common2 = None
    if most_common2:
        msg += f"- {most_common1} / {most_common2}\n"
    else:
        msg += f"- {most_common1} \n"
    """
    
    # Temperature:
    msg += f"- {round(max(temps))}° / {round(min(temps))}°\n"
    msg += f"- Clouds: {round(avg_clouds)}\n\n"
    # msg += f"- Sun: *{sun_hours}h*\n"

    # Rain:
    if round(avg_rain) == 0:
        msg += f"- No rain :)\n"
        msg += f"- Max rain: {max(rains)} mm\n"      # tmp debug; TODO remove later
        msg += f"- Avg rain: {round(avg_rain)} mm\n" # tmp debug; TODO remove later
    else:
        # msg += f"- Rain: {max(rains)} / {min(rains)} // {avg_rain} mm\n"
        msg += f"- Max rain: {max(rains)} mm\n"
        msg += f"- Avg rain: {round(avg_rain)} mm\n"

    # Wind:
    msg += f"- Wind: {round(min(winds))} - {round(max(winds))} m/s\n"
    msg += f"- Gust: {round(min(gusts))} - {round(max(gusts))} m/s\n"


    if not msg:
        raise ValueError("Weather forecast is empty or None"
                         f"All weather data fetched for the location: {data=}")

    return msg

