from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime


@dataclass
class Achievement:
    api_name: str
    name: str
    description: str = ""
    unlocked: bool = False
    unlock_time: int = 0
    icon: str = ""
    icon_gray: str = ""

    @property
    def unlock_datetime(self) -> Optional[datetime]:
        if self.unlock_time > 0:
            return datetime.fromtimestamp(self.unlock_time)
        return None

    def to_dict(self) -> dict:
        return {
            "api_name": self.api_name,
            "name": self.name,
            "description": self.description,
            "unlocked": self.unlocked,
            "unlock_time": self.unlock_time,
            "unlock_datetime": self.unlock_datetime.isoformat()
            if self.unlock_datetime
            else None,
            "icon": self.icon,
            "icon_gray": self.icon_gray,
        }


@dataclass
class AchievementCache:
    achievements: dict[str, Achievement] = field(default_factory=dict)
    last_update: int = 0

    def add(self, achievement: Achievement):
        self.achievements[achievement.api_name] = achievement

    def get(self, api_name: str) -> Optional[Achievement]:
        return self.achievements.get(api_name)

    def get_all(self) -> list[Achievement]:
        return list(self.achievements.values())

    def get_unlocked(self) -> list[Achievement]:
        return [a for a in self.achievements.values() if a.unlocked]

    def get_locked(self) -> list[Achievement]:
        return [a for a in self.achievements.values() if not a.unlocked]

    def get_new_unlocks(self, other: "AchievementCache") -> list[Achievement]:
        new = []
        for ach in self.achievements.values():
            other_ach = other.achievements.get(ach.api_name)
            if other_ach:
                if ach.unlocked and not other_ach.unlocked:
                    new.append(ach)
        return new

    def to_dict(self) -> dict:
        return {
            "achievements": {k: v.to_dict() for k, v in self.achievements.items()},
            "last_update": self.last_update,
            "total": len(self.achievements),
            "unlocked": len(self.get_unlocked()),
            "locked": len(self.get_locked()),
        }


@dataclass
class GameProfile:
    appid: str
    name: str
    achievement_count: int = 0
    primary_color: str = "#1b2838"
    accent_color: str = "#66c0f4"

    def to_dict(self) -> dict:
        return {
            "appid": self.appid,
            "name": self.name,
            "achievement_count": self.achievement_count,
            "primary_color": self.primary_color,
            "accent_color": self.accent_color,
        }


@dataclass
class Session:
    id: str
    start_time: int
    achievements_unlocked: list[str] = field(default_factory=list)

    def add_achievement(self, api_name: str):
        if api_name not in self.achievements_unlocked:
            self.achievements_unlocked.append(api_name)

    def get_count(self) -> int:
        return len(self.achievements_unlocked)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "start_time": self.start_time,
            "achievements_unlocked": self.achievements_unlocked,
            "count": self.get_count(),
        }
