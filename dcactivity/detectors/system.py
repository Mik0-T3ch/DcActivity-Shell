def detect_system(cmd: str):
    tokens = cmd.strip().split()
    if not tokens:
        return None

    is_sudo = tokens[0] == "sudo"
    if is_sudo and len(tokens) > 1:
        tokens = tokens[1:]

    base_cmd = tokens[0].lower()
    args_str = " ".join(tokens[1:]).lower()

    if base_cmd in ("systemctl", "service"):
        if "restart" in args_str or "start" in args_str:
            return {"state": "Iniciando servicio del sistema", "asset": "system"}
        if "status" in args_str:
            return {"state": "Consultando estado de servicio", "asset": "system"}
        return {"state": "Administrando servicios del sistema", "asset": "system"}

    if base_cmd == "journalctl":
        return {"state": "Revisando logs de systemd", "asset": "system"}

    if base_cmd in ("htop", "btop", "top", "gotop", "glances"):
        return {"state": f"Monitoreando recursos ({base_cmd})", "asset": "system"}

    if base_cmd in ("neofetch", "fastfetch", "pfetch", "cpufetch"):
        return {"state": "Mostrando info del sistema", "asset": "system"}

    if base_cmd in ("cmatrix", "hollywood", "pipes.sh"):
        return {"state": "Disfrutando de la terminal", "asset": "terminal"}

    if base_cmd in ("tar", "zip", "unzip", "gzip", "7z"):
        return {"state": "Comprimiendo/descomprimiendo archivos", "asset": "terminal"}

    if base_cmd in ("chmod", "chown"):
        return {"state": "Ajustando permisos del sistema", "asset": "system"}

    if base_cmd in ("df", "du", "lsblk", "fdisk"):
        return {"state": "Consultando almacenamiento", "asset": "system"}

    if is_sudo:
        return {"state": f"Ejecutando como root: {base_cmd}", "asset": "sudo"}

    return None
