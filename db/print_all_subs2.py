""" WIP: ssh to machine, then print all subscribers from the database """
import subprocess
import time

APP_NAME = "weather-whatsapp-bot"
DB_PATH = "/data/subscribers.db"
SQL = "SELECT * FROM subscribers;"

MACHINE_ID = "todo"
MACHINE_ID = "todo"
MACHINE_ID = "todo"
MACHINE_ID = "todo"
MACHINE_ID = "todo"

# Run sqlite3 remotely via SSH and capture output
cmd1 = f"fly machine start {MACHINE_ID}\""
cmd2 = f"fly ssh console --command \"sqlite3 -header -column {DB_PATH} '{SQL}'\""
result1 = subprocess.run(cmd1, shell=True, capture_output=True, text=True)
print(result1.stdout)
time.sleep(5)  # wait for the machine to start
result2 = subprocess.run(cmd2, shell=True, capture_output=True, text=True)
print(result2.stdout)
# idk if this works... the problem is that the machine auto sleeps quite quickly.
# idk if this works... the problem is that the machine auto sleeps quite quickly.

# test:
# sqlite3 -header -column {/data/subscribers.db} 'SELECT * FROM subscribers;'
