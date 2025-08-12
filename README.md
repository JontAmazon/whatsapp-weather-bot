A WhatsApp weather bot that sends daily weather updates using Twilio.

Sends today's weather at 08:30 and tomorrow's forecast at 18:00 using GitHub Actions cron jobs that run weather_bot.py on a Fly.io machine.


## Example WhatsApp message
Weather tomorrow:
- Clouds / Clear
- 21° / 16°
- No rain
- Clouds: 40.6
- Wind: 3 - 5 m/s
- Gust: 4 - 6 m/s

# Environment Variables
The following environment variables must be set:

## GitHub Actions secrets:
- `FLY_API_TOKEN`
- `FLY_APP_NAME`
- `MACHINE_ID`

## Fly.io secrets:
- `FLY_API_TOKEN`
- `FLY_APP_NAME`
- `MACHINE_ID`
- `IS_FLY_MACHINE` – true

- `TWILIO_ACCOUNT_SID`
- `TWILIO_AUTH_TOKEN`
- `WHATSAPP_FROM` – Your Twilio WhatsApp sender number
- `WHATSAPP_TO`

- `LAT`
- `LON`
- `WEATHER_API_KEY` – Your OpenWeatherMap API key
- `TOMORROW` – true/false. Get weather forecast for today or tomorrow. Value is set via GitHub Actions.
