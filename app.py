# app.py - Flask server & routes (basic validation)
import os
import re
from dotenv import load_dotenv
from flask import Flask, request, render_template, redirect, url_for, flash
from db import init_db, add_or_update_subscriber, get_subscriber_by_phone

load_dotenv()

# Config
DB_PATH = os.environ.get("DB_PATH", "/data/subscribers.db")  # Fly volume default
SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "dev-secret")  # override in prod
app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY

# Initialize DB on startup
init_db(DB_PATH)

# Basic validators
PHONE_RE = re.compile(r'^\+?[0-9]{6,15}$')  # allow + and digits
TIME_RE = re.compile(r'^[0-2]\d:[0-5]\d$')  # HH:MM 24h

def parse_bool(val):
    return bool(val) and (val.lower() in ("1","true","yes","on"))

def validate_form(form):
    errors = []
    phone = form.get("phone_number", "").strip()
    location = form.get("location", "").strip()
    lon = form.get("lon", "").strip()
    lat = form.get("lat", "").strip()
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
    # lon/lat optional but validate if provided
    if lon:
        try:
            float(lon)
        except ValueError:
            errors.append("Longitude must be a number (or leave empty).")
    if lat:
        try:
            float(lat)
        except ValueError:
            errors.append("Latitude must be a number (or leave empty).")
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
    phone_nbr = "whatsapp:" + phone_raw


    data = {
        "phone_number": phone_nbr,
        "location": form.get("location", "").strip(),
        "lon": float(form.get("lon")) if form.get("lon") else None,
        "lat": float(form.get("lat")) if form.get("lat") else None,
        "channel": form.get("channel", "whatsapp"),
        "send_time_morning": form.get("send_time_morning") or None,
        "send_time_afternoon": form.get("send_time_afternoon") or None,
        "wind": parse_bool(form.get("wind", "")),
        "gust": parse_bool(form.get("gust", "")),
        "gif": parse_bool(form.get("gif", "")),
        "forecast_days": int(form.get("forecast_days", "1")),
        "only_weird_weather": parse_bool(form.get("only_weird_weather", "")),
    }

    # Insert or update subscriber(s) with same phone number
    add_or_update_subscriber(DB_PATH, data)

    return redirect(url_for("thank_you"))

@app.route("/thankyou", methods=["GET"])
def thank_you():
    return render_template("thank_you.html")

if __name__ == "__main__":
    # debug server for local testing
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)), debug=True)
