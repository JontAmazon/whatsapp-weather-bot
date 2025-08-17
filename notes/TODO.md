# Prio 1:
- done?



# ---------- CURRENT LIMITATIONS ----------
- Twilio:
  - currently limited to WhatsApp, no SMS (but that could easily be changed).
- currently, all users are assumed to be near Central European Time. Texts are sent around 07:30 and 18:30 CET.


# Ideas:
- include a link to yr/hourly?



# ------------- GOLD-PLATING MAYBE ----------------
- add back checkboxes for preferences? see form.html
  - implement sending wind/gust, only when preferences say so.
  - implement "forecast_days"?

# ------------- GOLD-PLATING / NAH----------------
- thank you page: would be nice to distinguish between "thank you, you've subscribed", and "your preferences have been saved". How to do it (maybe):
  - "subscribe" -> app.py "subscribe" method. I think form.html can access the thing it returns? If so, we can adjust the code as follows: let "add_or_update_subscriber" return whether or not it added or subscribed... then use that.
- implement "WhatsApp confirmation" after sign-up?
  - with sandbox, I dont need it.
- replace the sleep 20 with: until flyctl machine list | grep "${{ secrets.MACHINE_ID }}" | grep -q "started"; do; sleep 1; done   ... I tried this, not sure it worked.


# ------------- MUCH LATER / EVEV ----------------
- handle unsubscribe? (very easy, I've already implemented a web hook...)
  - since the number of subs will be small, I don't think it's necessary, I can just rely on Twilio's "stop" filter?

- cron job every hour / matching logic for longitudes
  - for now, let's assume everyone I know is in Europe.

- Descriptive messages?
  Compare forecast to the average that time of the year, and just say something like:
  - "kinda hot tomorrow"
  - "kinda rainy tomorrow"
  - "very windy tomorrow, 15° / 6°, but feels like 12° / -2°.
  - link to hourly forecast
  - (in settings, the user can choose time and/or the original format.)




# ------------- Fun ideas ----------------
- gifs via AI, e.g. veo 2?


