import json
import urllib.request
import urllib.error
from typing import Optional


class WebhookClient:
    def __init__(self, url: str, rarity_threshold: str = "rare"):
        self.url = url
        self.rarity_threshold = rarity_threshold

    def send(self, achievement: dict) -> bool:
        if not self.url:
            return False

        if self.rarity_threshold == "legendary" and achievement.get("rarity", 0) > 1:
            return False
        if self.rarity_threshold == "ultra_rare" and achievement.get("rarity", 0) > 5:
            return False
        if self.rarity_threshold == "rare" and achievement.get("rarity", 0) > 20:
            return False

        message = self._format_message(achievement)

        try:
            data = json.dumps({"content": message}).encode("utf-8")
            req = urllib.request.Request(
                self.url, data=data, headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                return response.status < 400
        except Exception as e:
            print(f"Webhook error: {e}")
            return False

    def _format_message(self, achievement: dict) -> str:
        return f"🏆 Achievement Unlocked: {achievement.get('name', 'Unknown')}"
