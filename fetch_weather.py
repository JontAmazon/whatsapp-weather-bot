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
lat = os.getenv("LAT")
lon = os.getenv("LON")
tomorrow = os.getenv("TOMORROW", "").lower() == "true"
weather_url = "https://api.openweathermap.org/data/2.5/forecast"

print(f"{weather_api_key=}")
print(f"{lat=}")
print(f"{lon=}")
print(f"{tomorrow=}")

def fetch_weather():
    """ Fetch weather data from api.openweathermap.org,
    then just do a bunch of formatting etc.
    
    :return: String. Example:
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
        print(f"\n\n{data=}\n\n")

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

    ### Format the message
    day = "tomorrow" if tomorrow else "today"
    msg = f"🌤 Weather {day}:\n"
    # msg = f"🌤 Weather {target_date}:\n"
    if most_common2:
        msg += f"- {most_common1} / {most_common2}\n"
    else:
        msg += f"- {most_common1} \n"
    msg += f"- {round(max(temps))}° / {round(min(temps))}°\n"
    # msg += f"- Sun: *{sun_hours}h*\n"
    
    msg += f"- Clouds: {round(avg_clouds)}\n\n"
    
    ### RAIN:
    if round(avg_rain) == 0:
        msg += f"- No rain :)\n"
        msg += f"- Max rain: {max(rains)} mm\n"      # tmp debug; TODO remove later
        msg += f"- Avg rain: {round(avg_rain)} mm\n" # tmp debug; TODO remove later
    else:
        # msg += f"- Rain: {max(rains)} / {min(rains)} // {avg_rain} mm\n"
        msg += f"- Max rain: {max(rains)} mm\n"
        msg += f"- Avg rain: {round(avg_rain)} mm\n"

    ### WIND:
    msg += f"- Wind: {round(min(winds))} - {round(max(winds))} m/s\n"
    msg += f"- Gust: {round(min(gusts))} - {round(max(gusts))} m/s\n"

    return msg
