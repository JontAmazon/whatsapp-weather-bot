# WhatsApp Weather Bot
Bot that sends daily weather messages using Twilio. Sends today's weather at 07:00 and tomorrow's forecast at 18:00 using GitHub Actions cron jobs that run weather_bot.py on a Fly.io machine.

- subscribe for free via web form: https://weather-whatsapp-bot.fly.dev/

## Example WhatsApp message
Lund tomorrow:
- 21° / 16°
- Clouds: 40.6
- No rain

## Limitations
- Twilio Sandbox --- all lot of limitations
    - but I will change this, I hope !!!
- currently limited to WhatsApp, no SMS (could easily be changed).
- currently, all users are assumed to be near Central European Time. Texts are sent around 07:30 and 18:30 CET.

## Features
- *auto_stop_machines:* The Fly.io machine sleeps whenever it can, so I have ~0 costs. 🙂 
The VM only wakes up when the someone browses the sign-up form website, or when GH Actions trigger the weather bot.


# ---------- How to run locally ----------

## Requirements:
- get a Twilio Sandbox account for free: https://www.twilio.com/docs/whatsapp/sandbox


## Install -- eller vad säger man? Se Apple Dash
1. install something?
2. pip install -r requirements.txt



# How to run locally:
1. python app.py -> go to http://127.0.0.1:8080/ and subscribe
2. python weather_bot.py -> it sends messages to all numbers 


## Environmental variables
- (todo-later: list)






# ---------- Future wishlist ----------

## Descriptive messages:
Compare forecast to the average that time of the year, and just say something like:
- "kinda hot tomorrow"
- "kinda rainy tomorrow"
- "very windy tomorrow, 15° / 6°, but feels like 12° / -2°.
- link to hourly forecast
- (in settings, the user can choose time and/or the original format.)
