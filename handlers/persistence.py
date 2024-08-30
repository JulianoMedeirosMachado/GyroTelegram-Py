import json

FILE_PATH = 'watched_channels.json'

def save_watched_channels(watched_channels):
    with open(FILE_PATH, 'w') as f:
        json.dump(watched_channels, f)

def load_watched_channels():
    try:
        with open(FILE_PATH, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
