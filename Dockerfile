FROM python:3.11

# Create app directory
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

# Ensure DB mount path exists (Fly will mount a volume to /data)
RUN mkdir -p /data

ENV FLASK_ENV=production
ENV PORT=8080
EXPOSE 8080

CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app", "--workers", "2", "--threads", "4"]

# CMD:
# skip defining a CMD here?
# because we have different commands for the app and the job?
# hopefully it's sufficient that we define CMD in fly.toml.
#
#
# NOTE:
# we have different commands for:
# - the app (web form)
# - the whatsapp messaging job
#
# the commands are defined in fly.toml
# 
# hm...
# hm...
# and how does the whatsapp messaging job know 
# to run "python weather_bot.py" and not "gunicorn bla bla"?


# NOTE to self:
# maybe I should have the gunicorn command here, anyway. (???).
# to be continued...

