import os
import time

from dcactivity.core.rpc import DiscordRPC
from dcactivity.core.state import State
from dcactivity.core.config import Config

from dcactivity.detectors.distro import get_distro_info
from dcactivity.detectors.git import detect_git
from dcactivity.detectors.editors import detect_editor
from dcactivity.detectors.packages import detect_packages
from dcactivity.detectors.dev import detect_dev
from dcactivity.detectors.system import detect_system
from dcactivity.detectors.network import detect_network


class Engine:
    def __init__(self):
        self.config = Config()
        client_id = self.config.get("client_id")
        self.rpc = DiscordRPC(client_id=client_id)
        self.state = State()
        self.distro = get_distro_info()

        self.detectors = [
            detect_editor,
            detect_git,
            detect_packages,
            detect_dev,
            detect_system,
            detect_network
        ]

        self.rpc.connect()

    def format_path(self, cwd: str) -> str:
        if not cwd:
            return ""
        home = os.path.expanduser("~")
        if cwd == home:
            return "~"
        if cwd.startswith(home):
            return "~" + cwd[len(home):]
        return os.path.basename(cwd) or cwd

    def handle_event(self, event_data):
        if isinstance(event_data, str):
            cmd = event_data
            cwd = ""
            shell = "terminal"
        elif isinstance(event_data, dict):
            cmd = event_data.get("cmd", "")
            cwd = event_data.get("cwd", "")
            shell = event_data.get("shell", "terminal")
        else:
            return

        cmd = cmd.strip()
        if not cmd:
            return

        detected = self.detect(cmd)
        
        # Extraccion de datos de detector
        if isinstance(detected, dict):
            state_text = detected.get("state", "En terminal")
            small_asset = detected.get("asset")
        else:
            state_text = str(detected)
            small_asset = None

        if self.config.get("privacy_mode", False):
            state_text = "Trabajando en terminal"
            small_asset = None

        # Formato de details
        show_dir = self.config.get("show_current_dir", True)
        if show_dir and cwd:
            short_path = self.format_path(cwd)
            details_text = f"📁 {short_path}"
        else:
            details_text = f"{self.distro.get('name', 'Linux')} ({shell})"

        large_image = self.distro.get("asset_key", "shell")
        large_text = f"{self.distro.get('name', 'Linux')} | {shell}"

        if self.state.should_update(state_text, details_text):
            self.state.set(state_text, details_text, command=cmd)

            self.rpc.update(
                details=details_text,
                state=state_text,
                large_image=large_image,
                large_text=large_text,
                small_image=small_asset,
                small_text=f"Shell: {shell}",
                start_time=self.state.started_at
            )

            try:
                print(f"[STATE] {details_text} | {state_text}")
            except UnicodeEncodeError:
                safe_details = details_text.encode("ascii", "replace").decode("ascii")
                safe_state = state_text.encode("ascii", "replace").decode("ascii")
                print(f"[STATE] {safe_details} | {safe_state}")
        else:
            self.state.touch()

    def handle_command(self, cmd: str):
        self.handle_event({"cmd": cmd})

    def detect(self, cmd: str):
        for detector in self.detectors:
            result = detector(cmd)
            if result:
                return result

        return {"state": "Ejecutando comandos", "asset": "terminal"}
