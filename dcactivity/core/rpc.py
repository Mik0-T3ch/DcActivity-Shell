import time

from pypresence import Presence

CLIENT_ID = "1446336643320647720"


class DiscordRPC:
    def __init__(self):
        print("[DEBUG] RPC init")

        self.rpc = Presence(CLIENT_ID)

    def connect(self):
        print("[DEBUG] Connecting RPC")

        try:
            self.rpc.connect()

            print("[SUCCESS] Connected to Discord")

        except Exception as e:
            print(f"[RPC ERROR] {e}")

    def update(self, state: str, elapsed: int):
        print(f"[DEBUG] Updating: {state}")

        try:
            self.rpc.update(
                details="DcActivity",
                state=state,
                large_image="shell",
                large_text="Linux Activity",
                start=int(time.time())
            )

            print("[SUCCESS] RPC updated")

        except Exception as e:
            print(f"[UPDATE ERROR] {e}")