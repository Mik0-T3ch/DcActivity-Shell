from pypresence import Presence
import os
import time


CLIENT_ID = "1446336643320647720"
EVENT_FILE = "/home/caponikov/DcActivity-Shell/event.log"


class EventState:
    """Lee y parsea el último estado del archivo de eventos"""

    def __init__(self, event_file):
        self.event_file = event_file
        self.cmd = ""
        self.directory = ""
        self.user = ""

    def read(self):
        """Carga los últimos CMD, DIR y USER del evento"""
        if not os.path.exists(self.event_file):
            return

        data = {"CMD": "", "DIR": "", "USER": ""}

        with open(self.event_file, "r") as f:
            lines = f.readlines()

        for line in reversed(lines):
            if line.startswith("CMD:") and not data["CMD"]:
                data["CMD"] = line[4:].strip()
            elif line.startswith("DIR:") and not data["DIR"]:
                data["DIR"] = line[4:].strip()
            elif line.startswith("USER:") and not data["USER"]:
                data["USER"] = line[5:].strip()

            if all(data.values()):
                break

        self.cmd = data["CMD"]
        self.directory = data["DIR"]
        self.user = data["USER"]


class DiscordActivity:
    """Determina qué mostrar en Discord según los handlers registrados"""

    def __init__(self):
        self.handlers = []

    def add_handler(self, condition, image, details):
        """Registra un estado posible"""
        self.handlers.append((condition, image, details))

    def resolve(self, event: EventState):
        """Retorna la imagen y detalles correctos según el primer handler válido"""
        for condition, image, details in self.handlers:
            if condition(event):
                return image, details.format(event=event)

        # Estado por defecto
        return "terminal", f"Carpeta: {event.directory}"


class PresenceClient:
    """Cliente RPC para Discord Rich Presence"""

    def __init__(self, client_id):
        self.rpc = Presence(client_id)
        self.rpc.connect()

    def update(self, image, details, state, user):
        self.rpc.update(
            details=details,
            state=state,
            large_image=image,
            small_image="terminal",
            small_text=f"Usuario: {user}"
        )


# ---------------- CONFIGURACIÓN ---------------- #

event = EventState(EVENT_FILE)
activity = DiscordActivity()
client = PresenceClient(CLIENT_ID)

# Handlers ordenados por prioridad
activity.add_handler(
    lambda e: "nano" in e.cmd,
    "nano",
    "Escribiendo con Nano"
)

activity.add_handler(
    lambda e: e.user == "root" or e.cmd.startswith("sudo"),
    "root",
    "Modo Superusuario"
)

activity.add_handler(
    lambda e: True,
    "terminal",
    "Carpeta: {event.directory}"
)

# ---------------- LOOP PRINCIPAL ---------------- #

while True:
    event.read()
    image, details = activity.resolve(event)

    client.update(
        image=image,
        details=details,
        state=event.cmd,
        user=event.user
    )

    time.sleep(2)
