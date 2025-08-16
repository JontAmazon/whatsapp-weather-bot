# app.py - Flask server & routes (basic validation)
import os
import time
import re
from dotenv import load_dotenv
from flask import Flask, request, abort, render_template, redirect, url_for, flash
from db import init_db, add_or_update_subscriber, get_subscriber_by_phone

# Config
load_dotenv()
DB_PATH = os.environ.get("DB_PATH", "/data/subscribers.db")  # Fly volume default
# print(f"{DB_PATH=}")
SECRET_KEY = os.environ.get("FLASK_SECRET_KEY")
app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY

# Initialize DB on startup
init_db(DB_PATH)

# Basic validators
PHONE_RE = re.compile(r'^\+?[0-9]{6,15}$')  # allow + and digits
TIME_RE = re.compile(r'^[0-2]\d:[0-5]\d$')  # HH:MM 24h

# Rate limiting
VISIT_LIMIT = 10      # max requests
PER_SECONDS = 60      # per 60 seconds
visits = {}

def check_rate_limit():
    ip = request.remote_addr
    now = time.time()
    times = visits.get(ip, [])
    # remove old timestamps
    times = [t for t in times if now - t < PER_SECONDS]
    if len(times) >= VISIT_LIMIT:
        abort(429, "Too many requests, try later")
    times.append(now)
    visits[ip] = times

def parse_bool(val):
    return bool(val) and (val.lower() in ("1","true","yes","on"))

def validate_form(form):
    MAX_PHONE_LEN = 15
    MAX_LOCATION_LEN = 20
    MAX_LONLAT_LEN = 10
    errors = []
    phone = form.get("phone_number", "").strip()[:MAX_PHONE_LEN]
    location = form.get("location", "").strip()[:MAX_LOCATION_LEN]
    lon = form.get("lon", "").strip()[:MAX_LONLAT_LEN]
    lat = form.get("lat", "").strip()[:MAX_LONLAT_LEN]
    send_time_morning = form.get("send_time_morning", "").strip()
    send_time_afternoon = form.get("send_time_afternoon", "").strip()
    forecast_days = form.get("forecast_days", "1").strip()

    if not phone:
        errors.append("Phone number is required.")
    else:
        # Accept phone with optional leading "whatsapp:" or plus sign, normalize later
        normalized = phone.replace("whatsapp:", "").strip()
        if not PHONE_RE.match(normalized):
            errors.append("Phone number looks invalid. Use international format, e.g. +4676...")

    if not location:
        errors.append("Location is required.")

    # Longitude and latitude
    if not lon:
        errors.append("Longitude is required.")
    else:
        try:
            lon_val = float(lon)
            if not (-180 <= lon_val <= 180):
                errors.append("Longitude must be between -180 and 180.")
        except ValueError:
            errors.append("Longitude must be a number.")

    if not lat:
        errors.append("Latitude is required.")
    else:
        try:
            lat_val = float(lat)
            if not (-90 <= lat_val <= 90):
                errors.append("Latitude must be between -90 and 90.")
        except ValueError:
            errors.append("Latitude must be a number.")

    if send_time_morning and not TIME_RE.match(send_time_morning):
        errors.append("Morning send time must be HH:MM 24-hour format.")
    if send_time_afternoon and not TIME_RE.match(send_time_afternoon):
        errors.append("Afternoon send time must be HH:MM 24-hour format.")

    try:
        d = int(forecast_days)
        if not (1 <= d <= 7):
            errors.append("forecast_days must be between 1 and 7.")
    except ValueError:
        errors.append("forecast_days must be an integer.")

    return errors

@app.route("/", methods=["GET"])
def form():
    # Render subscription form
    return render_template("form.html")

@app.route("/subscribe", methods=["POST"])
def subscribe():
    check_rate_limit()
    form = request.form
    errors = validate_form(form)
    if errors:
        for e in errors:
            flash(e, "danger")
        # re-render form with previous values
        return render_template("form.html", form=form), 400

    # Normalize inputs
    phone_raw = form.get("phone_number", "").strip()
    # phone = phone_raw.replace("whatsapp:", "").strip()
    phone_nbr = "whatsapp:" + phone_raw  # e.g. "whatsapp:+46761234567"


    data = {
        "phone_number": phone_nbr,
        "location": form.get("location").strip(),
        "lon": float(form.get("lon")),
        "lat": float(form.get("lat")),
        "channel": form.get("channel", "whatsapp"),                     # not implemented yet
        "send_time_morning": form.get("send_time_morning") or None,     # not implemented yet
        "send_time_afternoon": form.get("send_time_afternoon") or None, # not implemented yet
        "wind": parse_bool(form.get("wind", "")),
        "gust": parse_bool(form.get("gust", "")),
        "gif": parse_bool(form.get("gif", "")),                         # not implemented yet
        "forecast_days": int(form.get("forecast_days", "1")),           # not implemented yet
        "only_weird_weather": parse_bool(form.get("only_weird_weather", "")), # not implemented yet
    }

    # Insert or update subscriber(s) with same phone number
    try:
        add_or_update_subscriber(DB_PATH, data)
    except Exception as e:
        print(f"Failed to subscribe: {e}")
        flash(f"Failed to subscribe due to a server error.", "danger")
        return redirect(url_for("form"))

    return redirect(url_for("thank_you"))

@app.route("/thankyou", methods=["GET"])
def thank_you():
    check_rate_limit()
    return render_template("thank_you.html")


def handle_unsubscribe_request(phone_number):
    print(f"Time to bring in Maria...")
    # ... logic here ...

@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    """ When a user sends a message to the bot via WhatsApp, it gets forwarded to this endpoint."""
    # Twilio webhook setup, i.e. the following sandbox configuration:
    # When a message comes in: https://weather-whatsapp-bot.fly.dev/whatsapp
    print("Twilio webhook - a user sent a message")
    from_number = request.form.get("From")
    body = request.form.get("Body", "").strip().lower()
    print(f"{from_number=}:")
    print(body)
    if body == "I want to unsubscribe":
        handle_unsubscribe_request(from_number)
        return "So... you think can you dance?", 200
    return "Message received", 200

if __name__ == "__main__":
    # NOTE: this code is only run when running app.py locally. Keep for local testing.
    # On Fly, I'm running Gunicorn (CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app", etc.])
    print("Starting Flask server...")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)), debug=True)
