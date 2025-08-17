# WhatsApp Weather Bot
Get daily weather forecasts delivered straight to your WhatsApp.

- Automated GitHub Actions trigger weather jobs on a Fly.io server.
- Sends today's forecast at 07:00 and tomorrow's at 18:00.
- Easy subscription via web form: https://weather-whatsapp-bot.fly.dev/.
- Unsubscribe by replying "stop".

## Example WhatsApp message
<img src="images/weather-bot-output.jpg" alt="weather-bot-output" width="60%">

## Features
- Auto-stop_machines: The Fly.io server automatically sleeps when not in use, keeping costs near zero. It wakes up instantly when someone visits the sign-up page or when GitHub Actions trigger the weather bot. Cold starts are fast.
- Weather API Integration: Fetches forecasts from OpenWeatherMap.
- Twilio Integration: Sends WhatsApp messages using Twilio API.
- Database Storage: Subscriber info stored securely in SQLite.
- Easy deployment (Fly.io/Gunicorn)
- Security:
  - Input validation.
  - Rate limiting.
  - Database size limit.
  - Environment Configuration: Uses .env for secrets and API keys.

# ---------- How to run locally ----------

## Requirements:
- get a free Twilio Sandbox account: https://www.twilio.com/docs/whatsapp/sandbox
- get a free weather api key: https://api.openweathermap.org/data/2.5/forecast
- pip install -r requirements.txt
- touch db/subscribers.db

1. python app.py -> go to http://127.0.0.1:8080/ -> subscribe
2. python weather_bot.py -> send messages

## Environment variables (run locally)
- `TWILIO_ACCOUNT_SID`
- `TWILIO_AUTH_TOKEN`
- `WHATSAPP_FROM` – Your Twilio WhatsApp sender number
- `WEATHER_API_KEY` – Your OpenWeatherMap API key
- `DB_PATH`=./db/subscribers.db
- `TOMORROW` – true/false. Get weather forecast for today or tomorrow. Value is set via GitHub Actions.

## Environment variables (Fly.io / GH)
If you deploy to Fly.io and use GH Action, these secrets must be set on both fly.io and GH:
- `FLY_API_TOKEN`
- `FLY_APP_NAME`
- `MACHINE_ID`
