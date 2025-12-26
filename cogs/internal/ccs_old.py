import json
import os

FILE = "cogs/counting_channels.json"

def load_channels():
    if not os.path.exists(FILE):
        return {}
    with open(FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_channels(data):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)