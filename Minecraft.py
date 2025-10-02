import re
import requests
import time
import os

# Telegram bot token & chat ID from Render environment variables
TOKEN = os.getenv("8115023864:AAG2UiT5YWTTXMuRjaIsDSBP1ug4jmkffZo")
CHAT_ID = os.getenv("7088894501")

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})

# Path to Minecraft logs (⚠️ works only if you have access to logs)
log_path = "logs/latest.log"

kill_pattern = re.compile(r"(\w+) killed (\w+)")

with open(log_path, "r") as f:
    f.seek(0, 2)  # move to end
    while True:
        line = f.readline()
        if not line:
            time.sleep(1)
            continue

        match = kill_pattern.search(line)
        if match:
            killer, victim = match.groups()
            send_message(f"{killer} kill him he killed {victim}")
