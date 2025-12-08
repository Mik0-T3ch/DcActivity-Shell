from pypresence import Presence
import os
import time

# ID de la app de Discord Rich Presence
CLIENT_ID = "1446336643320647720"

class EventState:
    # Lee y muetra el ultimo estado de actividad

    def read(self):
        # Carga los últimos CMD, DIR y USER del evento

        #si no existe la ruta no hay nada que leer
        if not os.path.exists(self.event_file):
            return

        # variable para almacenar temporalmente los ultimos datos
        data = {"CMD": "", "DIR": "", "USER": ""}

        # se leen todas las lineasd del archivo 
        with open(self.event_file, "r") as f:
            lines = f.readlines()

        # se lee el archivo al revez para obtener los ultimos datos de cada estado
        for line in reversed(lines):
            if line.startswith("CMD:") and not data["CMD"]:
                data["CMD"] = line[4:].strip()
            elif line.startswith("DIR:") and not data["DIR"]:
                data["DIR"] = line[4:].strip()
            elif line.startswith("USER:") and not data["USER"]:
                data["USER"] = line[5:].strip()

            # se corta cuando ya encontro los 3 valores
            if all(data.values()):
                break

        # actualiza la info
        self.cmd = data["CMD"]
        self.directory = data["DIR"]
        self.user = data["USER"]

    def __init__(self, event_file):
        self.cmd = ""
        self.event_file = event_file  # archivo que contiene los estados (CMD:,DIR:,USER:)
        self.directory = ""
        # los valores que se leen el archivo (al principio estan vacios)
        self.user = ""


# ruta absoluta delm archivo donde se registran los eventos de la shell
EVENT_FILE = os.path.join(
    os.path.expanduser("~"),
    "DcActivity-Shell",
    "event.log"
)

class DiscordActivity:
    # Determina que mostrar en Discord según los handlers registrados

    def resolve(self, event: EventState):
        # Retorna la imagen y detalles correctos según el primer handler válido
        for condition, image, details in self.handlers:
            if condition(event):
                return image, details.format(event=event)

        return "terminal", f"Carpeta: {event.directory}"

    def add_handler(self, condition, image, details):
        # Registra un estado posible
        self.handlers.append((condition, image, details))

    def __init__(self):
        self.handlers = []


class PresenceClient:
    # Cliente RPC para Discord Rich Presence

    # crea al cliente y lo conecta
    def __init__(self, client_id):
        self.rpc = Presence(client_id)
        self.rpc.connect()

    #a actualiza el Rich Present
    def update(self, image, details, state, user):
        self.rpc.update(
            details=details,
            state=state,
            large_image=image,
            small_image="terminal",
            small_text=f"Usuario: {user}"
        )


# CONFIGURACIÓN

activity = DiscordActivity()
event = EventState(EVENT_FILE)
client = PresenceClient(CLIENT_ID)

activity.add_handler(
    lambda e: "nano" in e.cmd,
    "nano",
    "Escribiendo con Nano"
)
# Handlers ordenados por prioridad

activity.add_handler(
    lambda e: e.user == "root" or e.cmd.startswith("sudo"),
    "root",
    "Modo Superusuario"
)

# handler principal por si los anteriores fallan
activity.add_handler(
    lambda e: True,
    "terminal",
    "Carpeta: {event.directory}"
)


# LOOP PRINCIPAL

while True:
    image, details = activity.resolve(event)  # para determinar que mostrar
    event.read()  # actualiza el estado desde el archivo .log

    client.update(
        image=image,
        details=details,
        state=event.cmd,
        user=event.user
    )

    time.sleep(0.1)

