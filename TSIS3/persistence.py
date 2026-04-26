import json
import os

SETTINGS_FILE = "settings.json"

# Бастапқы баптаулар (егер файл болмаса)
DEFAULT_SETTINGS = {
    "sound_on": True,
    "car_color": "RED",
    "difficulty": "Easy"
}

def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS
    with open(SETTINGS_FILE, "r") as f:
        return json.load(f)

def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)

LEADERBOARD_FILE = "leaderboard.json"

def load_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        return []
    with open(LEADERBOARD_FILE, "r") as f:
        return json.load(f)

def save_score(name, score):
    data = load_leaderboard()
    data.append({"name": name, "score": score})
    # Ұпай бойынша сұрыптау және топ 10-ды қалдыру
    data = sorted(data, key=lambda x: x['score'], reverse=True)[:10]
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(data, f, indent=4)