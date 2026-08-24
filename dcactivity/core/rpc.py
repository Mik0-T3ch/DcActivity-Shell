import time

try:
    from pypresence import Presence
except ImportError:
    Presence = None

CLIENT_ID = "1446336643320647720"


class DiscordRPC:
    def __init__(self, client_id: str = None):
        self.client_id = client_id or CLIENT_ID
        self.rpc = None
        self.connected = False
        self.last_connect_try = 0

    def connect(self):
        if Presence is None:
            return False

        now = time.time()
        if self.connected or (now - self.last_connect_try < 5):
            return self.connected

        self.last_connect_try = now
        try:
            self.rpc = Presence(self.client_id)
            self.rpc.connect()
            self.connected = True
            print("[RPC] Conectado a Discord")
            return True
        except Exception:
            self.connected = False
            return False

    def update(self, details: str, state: str, large_image: str = "shell",
               large_text: str = "Linux Shell", small_image: str = None,
               small_text: str = None, start_time: int = None):
        if not self.connected:
            if not self.connect():
                return

        payload = {
            "details": details[:127] if details else "DcActivity",
            "state": state[:127] if state else "En terminal",
            "large_image": large_image or "shell",
            "large_text": large_text[:127] if large_text else "Linux Activity"
        }

        if small_image:
            payload["small_image"] = small_image
            if small_text:
                payload["small_text"] = small_text[:127]

        if start_time:
            payload["start"] = int(start_time)
        else:
            payload["start"] = int(time.time())

        try:
            self.rpc.update(**payload)
        except Exception as e:
            print(f"[RPC ERROR] Error al actualizar: {e}")
            self.connected = False

    def close(self):
        if self.rpc and self.connected:
            try:
                self.rpc.close()
            except Exception:
                pass
            self.connected = False
