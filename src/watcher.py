from pypresence import Presence
import os
import time

# CLASES DE ESTADO

#esta clase define la estructura q se debe tener en las otras
class ShellState:
    def applies(self, data):
        raise NotImplementedError
    def get_presence(self, data):
        raise NotImplementedError


#es un estado por defecto se activa si las otras no
class NormalShellState(ShellState):
    def applies(self, data):
        return True

    def get_presence(self, data):
        #muestra el directorio actual y el ultimo comando ejecutado
        return {
            "details": f"Carpeta: {data['current_dir']}",
            "state": data["last_cmd"],
            "image": "terminal"
        }


#clase para detectar si se tiene nano 
class NanoState(ShellState):
    def applies(self, data):
        #comprueba si esta usando nano
        return "nano" in data["last_cmd"]

    #texto o imagen que se muestra en discord si esta usando nano
    def get_presence(self, data):
        return {
            "details": "Programando con Nano",
            "state": data["last_cmd"],
            "image": "nano"
        }


#se activa si el usuario es root
class RootState(ShellState):
    def get_presence(self, data):
        return {
            "details": "Modo ROOT",
            "state": data["last_cmd"],
            "image": "superusuario"
        }

    def applies(self, data):
        return data["user"] == "root"


#clase que gestiona los estados
class StateManager:
    def __init__(self):
        #lista ordenada segun la prioridad
        self.states = [
            NanoState(),
            RootState(),
            NormalShellState()
        ]

    #muestra los estados y enseña el estado actual
    def get_state(self, data):
        for s in self.states:
            if s.applies(data):
                return s.get_presence(data)


#MAIN RPC

CLIENT_ID = "1446336643320647720"
rpc = Presence(CLIENT_ID)
rpc.connect()

manager = StateManager()

#loop principal
while True:

    data = {
        "current_dir": os.getenv("CURRENT_SHELL_DIR", "Desconocida"),
        "last_cmd": os.getenv("LAST_SHELL_CMD", ""),
        "user": os.getenv("USER", "")
    }

    #determina  el estado segun los datos anteriores
    presence = manager.get_state(data)

    #manda la actualizacion a discord
    rpc.update(
        details=presence["details"],
        state=presence["state"],
        large_image=presence["image"]
    )

    #un tiempo de espera para no saturar el RPC
    time.sleep(3)

