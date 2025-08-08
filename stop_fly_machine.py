""" After weather_bot.py is run, run this script to stop the fly.io machine. """
import os
import requests

def stop_machine():
    machine_id = os.getenv("FLY_MACHINE_ID")
    app_name = os.getenv("FLY_APP_NAME")
    access_token = os.getenv("FLY_API_TOKEN")

    if not all([machine_id, app_name, access_token]):
        raise Exception("Error! Missing env vars for stopping machine")

    url = f"https://api.machines.fly.io/v1/apps/{app_name}/machines/{machine_id}/stop"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to stop machine: {e}")

    print("Sent stop request to fly.io machine.")
    # print("Stop response:", response.status_code, response.text)
    print("Stop request response code:", response.status_code)

