A WhatsApp weather bot that sends daily weather updates using Twilio.

Sends today's weather at 08:30 and tomorrow's forecast at 18:00 using GitHub Actions cron jobs that run weather_bot.py on a Fly.io machine.

- subscribe at URL: xxx

## Example WhatsApp message
Weather tomorrow:
- Clouds / Clear
- 21° / 16°
- No rain
- Clouds: 40.6
- Wind: 3 - 5 m/s
- Gust: 4 - 6 m/s

# -----------------------------------------

## (Some environmental variables must be set, e.g.:)
- (todo-later: list)

## How to run locally:
1. python app.py -> go to http://127.0.0.1:8080/ and subscribe
2. python weather_bot.py -> it sends messages to all numbers 


