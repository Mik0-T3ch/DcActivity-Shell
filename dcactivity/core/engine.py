print("[DEBUG] engine.py loaded")

from dcactivity.core.rpc import DiscordRPC


class Engine:
    def __init__(self):
        print("[DEBUG] Engine initialized")

        self.rpc = DiscordRPC()

        self.rpc.connect()

    def handle_command(self, cmd: str):
        print(f"[DEBUG] Handling command: {cmd}")

        self.rpc.update(cmd, 0)