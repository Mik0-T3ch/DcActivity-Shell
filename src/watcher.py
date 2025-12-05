from pypresence import Presence
import os
import time

# ----------- CLASES DE ESTADO -----------

class ShellState:
    def applies(self, data):
        raise NotImplementedError
    
    def get_presence(self, data):
        raise NotImplementedError


class NanoState(ShellState):
    def applies(self, data):
        return "nano" in data["last_cmd"]

    def get_presence(self, data):
        return {
            "details": "Programando con Nano",
            "state": data["last_cmd"],
            "image": "nano"
        }


class RootState(ShellState):
    def applies(self, data):
        return data["user"] == "root"

    def get_presence(self, data):
        return {
            "details": "Modo ROOT",
            "state": data["last_cmd"],
            "image": "superusuario"
        }


class NormalShellState(ShellState):
    def applies(self, data):
        return True

    def get_presence(self, data):
        return {
            "details": f"Carpeta: {data['current_dir']}",
            "state": data["last_cmd"],
            "image": "terminal"
        }


class StateManager:
    def __init__(self):
        self.states = [
            NanoState(),
            RootState(),
            NormalShellState()
        ]

    def get_state(self, data):
        for s in self.states:
            if s.applies(data):
                return s.get_presence(data)


# ----------- MAIN RPC -----------

CLIENT_ID = "1446336643320647720"
rpc = Presence(CLIENT_ID)
rpc.connect()

manager = StateManager()

while True:

    data = {
        "current_dir": os.getenv("CURRENT_SHELL_DIR", "Desconocida"),
        "last_cmd": os.getenv("LAST_SHELL_CMD", ""),
        "user": os.getenv("USER", "")
    }

    presence = manager.get_state(data)

    rpc.update(
        details=presence["details"],
        state=presence["state"],
        large_image=presence["image"]
    )

    time.sleep(3)
