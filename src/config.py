import json
import os
from pathlib import Path
from typing import Optional

CONFIG_FILE = Path("config/config.json")

DEFAULT_CONFIG = {
    "steam_id": "",
    "http_port": 5000,
    "ws_port": 8765,
    "poll_interval": 5,
    "cache_dir": "cache",
    "webhook_url": "",
    "webhook_rarity_threshold": "rare",
    "game_data_path": "",
    "theme": {"primary_color": "#1b2838", "accent_color": "#66c0f4"},
}


class Config:
    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = config_path or CONFIG_FILE
        self.data = DEFAULT_CONFIG.copy()
        self.load()

    def load(self):
        if self.config_path.exists():
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    user_config = json.load(f)
                self.data.update(user_config)
            except Exception as e:
                print(f"Warning: Could not load config: {e}")
        else:
            print(f"Config file not found at {self.config_path}, using defaults")

    def save(self):
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2)

    def get(self, key: str, default=None):
        return self.data.get(key, default)

    def set(self, key: str, value):
        self.data[key] = value

    @property
    def steam_id(self) -> str:
        return self.data.get("steam_id", "")

    @steam_id.setter
    def steam_id(self, value: str):
        self.data["steam_id"] = value

    @property
    def http_port(self) -> int:
        return self.data.get("http_port", 5000)

    @property
    def ws_port(self) -> int:
        return self.data.get("ws_port", 8765)

    @property
    def poll_interval(self) -> int:
        return self.data.get("poll_interval", 5)

    @property
    def webhook_url(self) -> str:
        return self.data.get("webhook_url", "")

    @property
    def theme(self) -> dict:
        return self.data.get("theme", DEFAULT_CONFIG["theme"])


def get_config() -> Config:
    return Config()
