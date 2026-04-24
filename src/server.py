import json
import re
import time
import threading
import os
import subprocess
import requests
from pathlib import Path
from flask import Flask, jsonify, render_template, request

from config import get_config
from achievement import Achievement, AchievementCache, Session
from vdf_parser import parse_achievements_file, get_steam_path


app = Flask(__name__, template_folder="../templates")
config = get_config()

achievement_cache = AchievementCache()
current_session = Session(id=str(int(time.time())), start_time=int(time.time()))

steam_path = get_steam_path()
current_appid = None
current_game = None


def parse_appmanifest(content: str) -> dict:
    result = {}
    for match in re.finditer(r'"(\w+)"\s+"([^"]*)"', content):
        key, value = match.groups()
        result[key] = value
    if "appid" in result:
        result["appid"] = int(result.get("appid", 0))
    return result


def get_loaded_games() -> dict:
    if not steam_path:
        return {}
    games = {}
    steamapps = steam_path.parent
    for app_manifest in steamapps.glob("appmanifest_*.acf"):
        try:
            content = app_manifest.read_text(encoding="utf-8")
            data = parse_appmanifest(content)
            appid = data.get("appid")
            name = data.get("name", "")
            if appid and name:
                games[name] = {"appid": str(appid), "name": name}
        except:
            pass
    return games


def detect_active_game() -> str:
    game_keywords = {
        "pragmata": "PRAGMATA",
        "playgtsanandreas": "GTA San Andreas",
        "gta san andreas": "GTA San Andreas",
        "gta_san_andreas": "GTA San Andreas",
        "gta": "GTA San Andreas",
        "san andreas": "GTA San Andreas",
        "gta definitive": "GTA San Andreas Definitive",
        "gta trilogy": "GTA Trilogy",
        "eldenring": "Elden Ring",
        "elden": "Elden Ring",
        "hollow knight": "Hollow Knight",
        "stardew": "Stardew Valley",
        "minecraft": "Minecraft",
        "cyberpunk": "Cyberpunk 2077",
        "baldur": "Baldur's Gate 3",
        "helldivers": "HELLDIVERS",
        "terraria": "Terraria",
        "celeste": "Celeste",
        "cs2": "Counter-Strike 2",
        "dota": "Dota 2",
        "pubg": "PUBG",
        "apex": "Apex Legends",
        "resident evil 2": "Resident Evil 2 Remake",
        "resident evil 2 remake": "Resident Evil 2 Remake",
        "re2": "Resident Evil 2 Remake",
        "monster hunter": "Monster Hunter World",
        "monster hunter world": "Monster Hunter World",
        "mhworld": "Monster Hunter World",
        "mafiadef": "Mafia 2 Definitive",
        "mafia definitive": "Mafia 2 Definitive",
        "mafia 2": "Mafia 2 Definitive",
    }
    try:
        result = subprocess.run(["tasklist"], capture_output=True, text=True, timeout=5)
        processes = result.stdout.lower()
        for keyword, game_name in game_keywords.items():
            if keyword in processes:
                return game_name
    except:
        pass
    return ""


def get_appid_for_game(game_name: str) -> str:
    game_appids = {
        "PRAGMATA": "3357650",
        "GTA San Andreas": "1547000",
        "GTA San Andreas Definitive": "1547000",
        "GTA Trilogy": "1817070",
        "GTA V": "271590",
        "Elden Ring": "1245620",
        "Hollow Knight": "367520",
        "Stardew Valley": "413150",
        "Minecraft": "1091500",
        "Cyberpunk 2077": "1091500",
        "Baldur's Gate 3": "1086940",
        "HELLDIVERS": "583400",
        "Terraria": "105600",
        "Celeste": "504230",
        "Counter-Strike 2": "730",
        "Dota 2": "570",
        "Resident Evil 2 Remake": "883710",
        "Monster Hunter World": "582010",
        "Mafia 2 Definitive": "1349010",
    }
    return game_appids.get(game_name, "")


def check_steam_cloud_achievements(appid: str, cache: AchievementCache):
    api_key = config.get("steam_api_key", "")
    steam_id = config.steam_id

    if not api_key or not steam_id:
        return

    url = f"http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid={appid}&key={api_key}&steamid={steam_id}&l=english"
    translations = load_translations(appid)

    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            playerstats = data.get("playerstats", {})
            if playerstats.get("success"):
                achievements = playerstats.get("achievements", [])

                for a in achievements:
                    api_name = a.get("apiname", "")
                    trans = translations.get(api_name, {})

                    name = trans.get("name") or a.get("name", "")
                    desc = trans.get("description") or a.get("description", "")

                    cache.add(
                        Achievement(
                            api_name=api_name,
                            name=name,
                            description=desc,
                            unlocked=a.get("achieved", 0) == 1,
                            unlock_time=a.get("unlocktime", 0),
                        )
                    )
    except Exception as e:
        pass


def load_translations(appid: str) -> dict:
    trans_path = Path("config/translations.json")
    if not trans_path.exists():
        return {}

    try:
        with open(trans_path, encoding="utf-8") as f:
            data = json.load(f)
        return data.get(appid, {})
    except:
        return {}


def load_achievements():
    global achievement_cache, current_appid, current_game

    achievement_cache = AchievementCache()

    detected = detect_active_game()
    if detected:
        current_game = detected
        current_appid = get_appid_for_game(detected)

    api_key = config.get("steam_api_key", "")
    steam_id = config.steam_id

    if current_appid and api_key and steam_id:
        check_steam_cloud_achievements(current_appid, achievement_cache)

    achievement_cache.last_update = int(time.time())
    return achievement_cache.to_dict()


def start_polling():
    def poll_loop():
        while True:
            try:
                load_achievements()
            except Exception as e:
                print(f"Polling error: {e}")
            time.sleep(config.poll_interval)

    thread = threading.Thread(target=poll_loop, daemon=True)
    thread.start()


@app.route("/")
def index():
    mode = request.args.get("mode", "horizontal")
    achievements_json = json.dumps(achievement_cache.to_dict())
    return render_template(
        "overlay.html",
        achievements_json=achievements_json,
        session_start_time=current_session.start_time,
        poll_interval=config.poll_interval,
        theme=config.theme,
        mode=mode,
    )


@app.route("/data")
def data():
    return jsonify(achievement_cache.to_dict())


@app.route("/session")
def session_info():
    return jsonify(current_session.to_dict())


@app.route("/session/reset", methods=["POST"])
def reset_session():
    global current_session
    current_session = Session(id=str(int(time.time())), start_time=int(time.time()))
    return jsonify({"status": "reset", "session": current_session.to_dict()})


@app.route("/dock")
def dock():
    return render_template("dock.html")


@app.route("/popup")
def popup():
    return render_template("popup.html")


@app.route("/game")
def game_info():
    return jsonify(
        {
            "appid": current_appid,
            "name": current_game,
        }
    )


if __name__ == "__main__":
    print("Starting Stream Achievement Counter...")
    print(f"Steam path: {steam_path}")
    print(f"HTTP: http://localhost:{config.http_port}")
    print(f"Dock: http://localhost:{config.http_port}/dock")
    load_achievements()
    start_polling()
    app.run(host="0.0.0.0", port=config.http_port, debug=False)
