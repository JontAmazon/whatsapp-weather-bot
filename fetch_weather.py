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
    # NOTE: this API gives data in 3 hour intervals for the next 5 days.


def fetch_weather(location: str, lon: str, lat: str, tomorrow: bool) -> str:
    data = get_weather_data(lon, lat)
    if data == "error fetching weather data":
        return
    return format_weather(data, location, tomorrow)

def get_weather_data(lon, lat):
    """ Fetch raw weather data from the API. Returns the raw response (dict or JSON). """
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
        return "error fetching weather data"
    except requests.exceptions.RequestException as err:
        print(f"Request failed: {err}")
        return "error fetching weather data"
    
    # print(f"[DEBUG] Weather API response headers: {response.headers}")
    print(f"[DEBUG] First 150 chars of body: {response.text[:150]}") 
    data = response.json()
    # print(f"\n\n{data=}\n\n")
    return data
    
def format_weather(data, location: str, tomorrow: bool) -> str:
    """
    Format raw weather data into a message string.

    :param tomorrow: Boolean. If True, fetch weather for tomorrow, otherwise for today.
    :return: Example string:
        Lund tomorrow:
        - 21° / 16°
        - Light breeze
        - Maybe some rain
    """
    # ---------------------------------------------------------
    # NOTE: possible additions to the message:
    """
        - Clear / Broken clouds
        - Clouds: 40.6%
        - Gust: 4 - 6 m/s
        - sun hours?
    """
    # ---------------------------------------------------------
    temps = []
    feels_like = []
    winds = []
    gusts = []
    rains = []
    clouds = []
    weather_type = []
    weather_description = []
    time_of_day = []  # e.g. 09:00, 12:00, etc.

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
        
        if dt.time().hour < 7 or dt.time().hour > 22:
            # not such an interesting interval for rain/clouds/wind/weather type --> skip!
            # NOTE: 7-22 gives us an interval from 7:00 to 01:00, since the weather data is 3h intervals.
            continue
        
        # Between 7:00 - 01:00:
        clouds.append(item["clouds"]["all"])
        rains.append(item.get("rain", {}).get("3h", 0))
        winds.append(item["wind"]["speed"])
        gusts.append(item["wind"].get("gust", {0}))

        weather_type.append(item["weather"][0]["main"])
        weather_description.append(item["weather"][0]["description"])
        time_of_day.append(dt.time())

    if not temps:
        return "No weather data available."
    
    # [DEBUG] Print "weather_type"
    for hour_of_day, w_type_3h, w_descr_3h in zip(time_of_day, weather_type, weather_description):
        print(f"{hour_of_day}: {w_type_3h=}, {w_descr_3h=}")

    # Calculate averages
    avg_clouds = sum(clouds) / len(clouds) if clouds else "no data"
    avg_wind = sum(winds) / len(winds) if winds else "no data"
    avg_rain = sum(rains) / len(rains) if rains else 0
    avg_rain_per_hour = avg_rain / 3

    ### ------------- Format the message ----------------
    which_day = "tomorrow" if tomorrow else "today"
    msg = f"🌤 {location} {which_day}:\n"
    
    # msg += f"- {round(max(temps))}° / {round(min(temps))}°\n"
    msg += f"- {round(max(feels_like))}° / {round(min(feels_like))}°\n"
    
    if avg_wind != "no data":
        wind_descr = describe_wind(avg_wind)
        msg += f"- {wind_descr}\n"

    rain_descr = describe_rain(avg_rain_per_hour)
    msg += f"- {rain_descr}\n"

    if not msg:
        raise ValueError("Weather forecast is empty or None"
                         f"All weather data fetched for the location: {data=}")

    return msg

def describe_rain(avg_rain_per_h):
    div_factor = 5  # Since we're talking day averages (between 07:00 and 01:00),
                    # we can't use the thresholds how rain is normally defined.
                    # Even a small daily average can mean a lot of rain at some point.
    if avg_rain_per_h > 4.5 / div_factor:
        return "A lot of rain"
    elif avg_rain_per_h > 2.4 / div_factor:
        return "Rainy"
    elif avg_rain_per_h > 1.1 / div_factor:
        return "Some rain"
    elif avg_rain_per_h > 0.3 / div_factor:
        return "Maybe some rain"
    else:
        return "No rain"

def describe_wind(avg_wind):
    if avg_wind > 7.8:
        return "Super windy!"
    elif avg_wind > 6.5:
        return "Strong wind"
    elif avg_wind > 4.7:
        return "Windy"
    elif avg_wind > 3.5:
        return "A bit windy"
    elif avg_wind > 2.8:
        return "Light breeze"
    else:
        return "Calm"

def get_emojis(weather_type) -> str:
    """ Not used. Just an idea.
    
    :return: e.g. [☁️,☁️,🌧,☀️,☁️]
    """
    # Translate "weather_type" into emojis
    return
    emojis = []
    for w_type_3h in weather_type:
        if w_type_3h == "Clouds":
            emojis.append("☁️")
        elif w_type_3h == "Clear":
            emojis.append("☀️")
        elif w_type_3h == "Rain":
            emojis.append("🌧")
        # EV: do same but with weather_description?
    return emojis

def get_main_weather_type(weather_type) -> str:
    """ Not used. Just an idea.
    
    :return: e.g. "Cloudy / Clear"
    """
    return
    counts = Counter(weather_type)
    most_common = counts.most_common(2)
    most_common1 = most_common[0][0]
    if len(most_common) > 1:
        most_common2 = most_common[1][0]
    else:
        most_common2 = None
    if most_common2:
        return f"{most_common1} / {most_common2}"
    else:
        return f"{most_common1}"
        # EV: do same but with weather_description?
