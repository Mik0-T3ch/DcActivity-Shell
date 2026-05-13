def detect_network(cmd: str):
    cmd = cmd.lower()

    if "ssh " in cmd:
        return "Conectado por SSH"

    if "ping " in cmd:
        return "Haciendo ping"

    return None