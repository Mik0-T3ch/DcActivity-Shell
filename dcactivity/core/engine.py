import os
import threading
import time

from dcactivity.core.rpc import DiscordRPC
from dcactivity.core.state import State
from dcactivity.core.config import Config

from dcactivity.detectors.distro import get_distro_info
from dcactivity.detectors.git import detect_git, get_git_context
from dcactivity.detectors.editors import detect_editor
from dcactivity.detectors.packages import detect_packages
from dcactivity.detectors.dev import detect_dev
from dcactivity.detectors.security import detect_security
from dcactivity.detectors.hardware import detect_hardware
from dcactivity.detectors.system import detect_system
from dcactivity.detectors.network import detect_network


class Engine:
    def __init__(self):
        self.config = Config()
        client_id = self.config.get("client_id")
        self.rpc = DiscordRPC(client_id=client_id)
        self.state = State()
        self.distro = get_distro_info()
        self.current_cwd = ""
        self.current_shell = "terminal"
        self.is_idle = False

        self.detectors = [
            detect_editor,
            detect_git,
            detect_packages,
            detect_dev,
            detect_security,
            detect_hardware,
            detect_system,
            detect_network
        ]

        self.rpc.connect()

        self._idle_thread = threading.Thread(target=self._idle_checker, daemon=True)
        self._idle_thread.start()

    def format_path(self, cwd: str) -> str:
        if not cwd:
            return ""
        home = os.path.expanduser("~")
        if cwd == home:
            return "~"
        if cwd.startswith(home):
            return "~" + cwd[len(home):]
        return os.path.basename(cwd) or cwd

    def _idle_checker(self):
        while True:
            time.sleep(5)
            idle_timeout = self.config.get("idle_timeout", 180)
            if idle_timeout <= 0:
                continue

            if not self.is_idle and self.state.idle_seconds() >= idle_timeout:
                self.is_idle = True
                idle_text = self.config.get("idle_text", "Inactivo en terminal")
                details_text = f"📁 {self.format_path(self.current_cwd)}" if self.current_cwd else self.distro.get("name", "Linux")
                large_image = self.distro.get("asset_key", "shell")
                large_text = f"{self.distro.get('name', 'Linux')} (Idle)"

                self.rpc.update(
                    details=details_text,
                    state=idle_text,
                    large_image=large_image,
                    large_text=large_text,
                    small_image=None,
                    small_text="Idle",
                    start_time=self.state.started_at
                )

    def handle_event(self, event_data):
        if isinstance(event_data, str):
            cmd = event_data
            cwd = self.current_cwd
            shell = self.current_shell
        elif isinstance(event_data, dict):
            cmd = event_data.get("cmd", "")
            cwd = event_data.get("cwd", self.current_cwd)
            shell = event_data.get("shell", self.current_shell)
        else:
            return

        cmd = cmd.strip()
        if not cmd:
            return

        self.current_cwd = cwd
        self.current_shell = shell
        self.is_idle = False

        ignored = self.config.get("ignored_commands", [])
        base_cmd = cmd.split()[0].lower() if cmd.split() else ""
        if base_cmd in ignored or cmd.lower() in ignored:
            self.state.touch()
            return

        detected = self.detect(cmd)
        
        if isinstance(detected, dict):
            state_text = detected.get("state", "En terminal")
            small_asset = detected.get("asset")
        else:
            state_text = str(detected)
            small_asset = None

        if self.config.get("privacy_mode", False):
            state_text = "Trabajando en terminal"
            small_asset = None

        show_dir = self.config.get("show_current_dir", True)
        if show_dir and cwd:
            git_ctx = get_git_context(cwd)
            if git_ctx:
                details_text = f"📂 {git_ctx['repo']} ({git_ctx['branch']})"
            else:
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
