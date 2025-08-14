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
