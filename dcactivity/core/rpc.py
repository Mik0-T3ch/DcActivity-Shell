import time

from pypresence import Presence

CLIENT_ID = "1446336643320647720"


class DiscordRPC:
    def __init__(self):
        self.rpc = Presence(CLIENT_ID)

        self.connected = False

    def connect(self):
        try:
            self.rpc.connect()

            self.connected = True

            print("[RPC] Connected")

        except Exception as e:
            print(f"[RPC ERROR] {e}")

    def update(self, state: str, elapsed: int):
        try:
            self.rpc.update(
                details="DcActivity",
                state=state,
                large_image="shell",
                large_text="Linux Activity",
                start=int(time.time()) - elapsed
            )

        except Exception as e:
            print(f"[RPC UPDATE ERROR] {e}")

            self.connected = False