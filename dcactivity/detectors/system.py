def detect_system(cmd: str):
    cmd = cmd.lower()

    if "sudo" in cmd:
        return "Ejecutando como root"

    if "apt " in cmd:
        return "Gestionando paquetes"

    return None