A WhatsApp weather bot that sends daily weather updates using Twilio.

Sends today's weather at 08:30 and tomorrow's forecast at 18:00 using GitHub Actions cron jobs that run weather_bot.py on a Fly.io machine.


## Example WhatsApp message
Weather tomorrow:
- Clouds / Clear
- Sun: 6h
- 21° / 16°
- No rain
- Clouds: 40.6
- Wind: 5 - 3 m/s
- Gust: 6 - 4 m/s

## Environment Variables
The following environment variables must be set for the app to work:

### Twilio
- `TWILIO_ACCOUNT_SID` – Your Twilio Account SID
- `TWILIO_AUTH_TOKEN` – Your Twilio Auth Token
- `WHATSAPP_FROM` – Your Twilio WhatsApp sender number (e.g., `whatsapp:+123456789`)
- `WHATSAPP_TO` – The recipient WhatsApp number (e.g., `whatsapp:+987654321`)

### Weather API
- `WEATHER_API_KEY` – Your OpenWeatherMap API key
- `LAT` – Latitude of the location
- `LON` – Longitude of the location



