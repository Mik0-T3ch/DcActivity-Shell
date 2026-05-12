import json
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "default.json"


class Config:
    def __init__(self):
        self.data = self.load()

    def load(self):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                return json.load(f)

        except Exception as e:
            print(f"[CONFIG ERROR] {e}")

            return {
                "privacy_mode": False,
                "show_full_command": False,
                "max_command_length": 25,
                "update_interval": 2
            }

    def get(self, key, default=None):
        return self.data.get(key, default)