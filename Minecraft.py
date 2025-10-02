import re
import requests
import time
import os

# --- Configuration ---
# Read the names of the environment variables set on Render
TOKEN = os.getenv("8115023864:AAG2UiT5YWTTXMuRjaIsDSBP1ug4jmkffZo")
CHAT_ID = os.getenv("7088894501")

# Path to the Minecraft log file
# WARNING: This assumes the log file exists at this relative path
# within the Render environment, which may be tricky if the Minecraft
# server is not running alongside this script.
LOG_PATH = "logs/latest.log"

# Regex to find player kill messages in the log
# Example log line: "[20:20:20] [Server thread/INFO]: PlayerA was slain by PlayerB using [item]"
KILL_PATTERN = re.compile(r"(\w+) was slain by (\w+)")


def send_message(text):
    """Sends a message to the specified Telegram chat."""
    if not TOKEN or not CHAT_ID:
        print("ERROR: TELEGRAM_TOKEN or CHAT_ID environment variable not set.")
        return

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    
    # Use Markdown for formatting and disable link previews
    data = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": "true"
    }
    
    try:
        response = requests.post(url, data=data, timeout=5)
        response.raise_for_status() # Raise exception for bad status codes (4xx or 5xx)
    except requests.exceptions.RequestException as e:
        print(f"ERROR: Telegram message failed to send: {e}")


def main():
    """Main function to continuously tail and process the log file."""
    print(f"Starting log monitor for: {LOG_PATH}...")
    
    try:
        # Open the log file for reading
        with open(LOG_PATH, "r") as f:
            # Move the file pointer to the end so we only read new lines
            f.seek(0, 2)
            print("Successfully moved to end of log file. Monitoring new entries...")

            while True:
                # Read a new line
                line = f.readline()
                
                if not line:
                    # No new line found, wait a moment and try again
                    time.sleep(1)
                    continue

                # Search for the kill pattern
                match = KILL_PATTERN.search(line)
                if match:
                    # In Minecraft logs, the player who was slain comes first
                    victim, killer = match.groups()
                    
                    # Craft a clear notification message
                    message = f"💀 **KILL ALERT!**\n*{killer}* eliminated *{victim}*."
                    
                    # Send the notification
                    send_message(message)
                    print(f"Sent notification: {message}")

    except FileNotFoundError:
        print(f"CRITICAL ERROR: Log file not found at {LOG_PATH}. Check your file path and server setup.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
