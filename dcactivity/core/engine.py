from dcactivity.core.rpc import DiscordRPC
from dcactivity.core.state import State
from dcactivity.core.config import Config

from dcactivity.detectors.git import detect_git
from dcactivity.detectors.editors import detect_editor
from dcactivity.detectors.system import detect_system
from dcactivity.detectors.network import detect_network


class Engine:
    def __init__(self):
        self.rpc = DiscordRPC()

        self.state = State()

        self.config = Config()

        self.detectors = [
            detect_git,
            detect_editor,
            detect_system,
            detect_network
        ]

        self.rpc.connect()

    def handle_command(self, cmd: str):
        state = self.detect(cmd)

        if self.config.get("privacy_mode"):
            state = "Trabajando en terminal"

        if self.state.should_update(state):
            self.state.set(state)

            self.rpc.update(
                state,
                self.state.elapsed()
            )

            print(f"[STATE] {state}")

    def detect(self, cmd: str):
        for detector in self.detectors:
            result = detector(cmd)

            if result:
                return result

        return f"Usando terminal"