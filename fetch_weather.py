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
        Lund tomorrow:
        - 21° / 16°
        - Clouds: 40.6
        - Rain: 0 mm / 3h
        - Wind: 3 - 5 m/s
        - Gust: 4 - 6 m/s
    """
    
    # ---------------------------------------------------------
    # NOTE: I slimmed down the message a lot. If one wants to, it could look like this:
    """
        Lund tomorrow:
        - Clear / Broken clouds
        - 21° / 16°
        - Clouds: 40.6%
        - Rain: 0 mm/h
        - Wind: 3 - 5 m/s
        - Gust: 4 - 6 m/s
    """
    # ---------------------------------------------------------

    # ----------- 1. Fetch the weather data from weather_url ----------------
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
        # print(f"[DEBUG] Weather API response headers: {response.headers}")
        print(f"[DEBUG] First 150 chars of body: {response.text[:150]}") 

        data = response.json()
        # print(f"\n\n{data=}\n\n")

    # --------------- 2. Build the weather message ----------------
    # Define variables
    # sun_hours = 0; # if weather_type_3h == "Clear": sun_hours += 3
    temps = []
    feels_like = []
    winds = []
    gusts = []
    rains = []
    clouds = []
    weather_type = []
    weather_description = []
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
        
        # 24 hours:
        temps.append(item["main"]["temp"])
        feels_like.append(item["main"]["feels_like"])
        winds.append(item["wind"]["speed"])
        gusts.append(item["wind"].get("gust", {0}))
        
        if dt.time().hour < 7 or dt.time().hour > 22:
            # not such an interesting interval for rain/clouds/weather type --> skip!
            # NOTE: 7-22 gives us an interval from 7:00 to 01:00, since the weather data is 3h intervals.
            continue
        
        # Between 7:00 - 01:00:
        clouds.append(item["clouds"]["all"])
        rains.append(item.get("rain", {}).get("3h", 0))
        weather_type.append(item["weather"][0]["main"])
        weather_description.append(item["weather"][0]["description"])
        time_of_day.append(dt.time())

    if not temps:
        return "No weather data available."
    

    # Translate "weather_type" into emojis
    for hour_of_day, w_type_3h, w_descr_3h in zip(time_of_day, weather_type, weather_description):
        print(f"{hour_of_day}: {w_type_3h=}, {w_descr_3h=}")
        if w_type_3h == "Clouds":
            weather_emoji.append("☁️")
        elif w_type_3h == "Clear":
            weather_emoji.append("☀️")
        elif w_type_3h == "Rain":
            weather_emoji.append("🌧")

    # maybe TODO:
    # Translate "weather_description" into emojis
    # ...

    # Calculate averages
    avg_clouds = sum(clouds) / len(clouds) if clouds else "no data"
    avg_wind = sum(winds) / len(winds) if winds else "no data"
    avg_rain = sum(rains) / len(rains) if rains else 0
    avg_rain_per_hour = avg_rain / 3

    ### ------------- Format the message ----------------
    which_day = "tomorrow" if tomorrow else "today"
    msg = f"🌤 {location} {which_day}:\n"
    
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
    # msg += f"- {round(max(temps))}° / {round(min(temps))}°\n"
    msg += f"- {round(max(feels_like))}° / {round(min(feels_like))}°\n"
    # msg += f"- Sun: *{sun_hours}h*\n"
    
    # Clouds:
    # msg += f"- Clouds: {round(avg_clouds)}%\n"

    # Rain:
    if avg_rain_per_hour < 0.1:
        msg += f"- No rain\n"
    else:
        msg += f"- Rain: {avg_rain_per_hour:.2f} mm/h\n"

    # Wind:
    # I don't know if this is interesting enough...
    # msg += f"- Wind: {round(min(winds))} - {round(max(winds))} m/s\n"
    # msg += f"- Gusts: {round(min(gusts))} - {round(max(gusts))} m/s\n"


    if not msg:
        raise ValueError("Weather forecast is empty or None"
                         f"All weather data fetched for the location: {data=}")

    return msg

