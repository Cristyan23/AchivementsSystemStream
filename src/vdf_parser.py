import os
import re
import struct
from pathlib import Path
from typing import Optional

STEAM_PATHS = [
    Path("C:/Program Files (x86)/Steam/steamapps/common"),
    Path("C:/Program Files/Steam/steamapps/common"),
    Path(
        os.environ.get("PROGRAMFILES(X86)", "C:/Program Files (x86)")
        + "/Steam/steamapps/common"
    ),
]


def get_steam_path() -> Optional[Path]:
    for base in STEAM_PATHS:
        if base.exists():
            return base

    import os

    local_appdata = os.environ.get("LOCALAPPDATA")
    if local_appdata:
        config_path = Path(local_appdata) / "Steam" / "config" / "config.vdf"
        if config_path.exists():
            content = config_path.read_text(encoding="utf-8")
            match = re.search(r'"InstallConfigDir"\s+"([^"]+)"', content)
            if match:
                return Path(match.group(1)) / "steamapps" / "common"

    return None


def find_achievements_file(steam_id: str) -> Optional[Path]:
    steam_path = get_steam_path()
    if not steam_path:
        return None

    user_manifests = steam_path.parent / "steamapps" / "user"
    if user_manifests.exists():
        for manifest in user_manifests.glob("*.vdf"):
            content = manifest.read_text(encoding="utf-8", errors="ignore")
            if steam_id in content:
                localappdata = Path(os.environ.get("LOCALAPPDATA", ""))
                AchieveFile = (
                    localappdata
                    / "Steam"
                    / "html"
                    / "achievements"
                    / steam_id[:17]
                    / "achievements.dat"
                )
                if AchieveFile.exists():
                    return AchieveFile

    return None


class VDFParser:
    def __init__(self, data: str):
        self.data = data
        self.pos = 0

    def parse(self) -> dict:
        result = {}
        while self.pos < len(self.data):
            key = self._read_string()
            if not key:
                break
            if self.pos >= len(self.data):
                break
            value = self._read_value()
            result[key] = value
        return result

    def _read_string(self) -> str:
        if self.pos >= len(self.data):
            return ""

        if self.data[self.pos] == '"':
            self.pos += 1
            start = self.pos
            while self.pos < len(self.data) and self.data[self.pos] != '"':
                self.pos += 1
            value = self.data[start : self.pos]
            self.pos += 1
            return value
        else:
            start = self.pos
            while self.pos < len(self.data) and self.data[self.pos] not in '"\t\r\n':
                self.pos += 1
            return self.data[start : self.pos].strip()

    def _read_value(self) -> dict:
        result = {}
        while self.pos < len(self.data):
            self._skip_whitespace()
            if self.pos >= len(self.data):
                break
            if self.data[self.pos] == "}":
                self.pos += 1
                break
            key = self._read_string()
            if not key:
                break
            self._skip_whitespace()
            if self.pos >= len(self.data):
                break
            if self.data[self.pos] == "{":
                self.pos += 1
                result[key] = self._read_value()
            elif self.data[self.pos] == '"':
                result[key] = self._read_string()
            else:
                result[key] = self._read_string()
        return result

    def _skip_whitespace(self):
        while self.pos < len(self.data) and self.data[self.pos] in " \t\r\n":
            self.pos += 1


def parse_achievements_file(filepath: Path) -> dict:
    if not filepath.exists():
        return {}

    try:
        content = filepath.read_text(encoding="utf-16-le", errors="ignore")
        if not content:
            content = filepath.read_bytes().decode("utf-8", errors="ignore")

        parser = VDFParser(content)
        return parser.parse()
    except Exception as e:
        print(f"Error parsing achievements file: {e}")
        return {}


def get_achievements_for_app(app_path: Path, appid: str) -> list[dict]:
    achievements_file = app_path / "achievements.dat"
    if not achievements_file.exists():
        return []

    data = parse_achievements_file(achievements_file)

    achievements = []
    achievements_node = data.get("achievements", {})

    if isinstance(achievements_node, dict):
        for key, value in achievements_node.items():
            if isinstance(value, dict):
                achievements.append(
                    {
                        "api_name": key,
                        "name": value.get("name", key),
                        "description": value.get("description", ""),
                        "unlocked": value.get("unlocked", False),
                        "unlock_time": value.get("unlock_time", 0),
                    }
                )

    return achievements


def parse_vdf_string(content: str) -> dict:
    parser = VDFParser(content)
    return parser.parse()


if __name__ == "__main__":
    import os

    steam_path = get_steam_path()
    print(f"Steam path: {steam_path}")

    if steam_path and steam_path.exists():
        print(f"Contents: {list(steam_path.parent.glob('*'))[:10]}")
