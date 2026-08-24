import json
import os
from pathlib import Path

DEFAULT_CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "default.json"
USER_CONFIG_PATH = Path.home() / ".config" / "dcactivity" / "config.json"


class Config:
    def __init__(self):
        self.data = self.load()

    def load(self):
        config_data = {
            "client_id": "1446336643320647720",
            "privacy_mode": False,
            "show_current_dir": True,
            "show_distro": True,
            "idle_timeout": 180,
            "idle_text": "Inactivo en terminal",
            "ignored_commands": ["clear", "history", "exit"],
            "update_interval": 2
        }

        # Cargar default del paquete
        if DEFAULT_CONFIG_PATH.exists():
            try:
                with open(DEFAULT_CONFIG_PATH, "r", encoding="utf-8") as f:
                    config_data.update(json.load(f))
            except Exception as e:
                print(f"[CONFIG ERROR] Al leer default.json: {e}")

        # Sobrescribir con config del usuario si existe (~/.config/dcactivity/config.json)
        if USER_CONFIG_PATH.exists():
            try:
                with open(USER_CONFIG_PATH, "r", encoding="utf-8") as f:
                    config_data.update(json.load(f))
            except Exception as e:
                print(f"[CONFIG ERROR] Al leer config de usuario: {e}")

        return config_data

    def get(self, key, default=None):
        return self.data.get(key, default)
