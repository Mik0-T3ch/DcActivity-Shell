import re


def detect_packages(cmd: str):
    tokens = cmd.strip().split()
    if not tokens:
        return None

    if tokens[0] == "sudo" and len(tokens) > 1:
        tokens = tokens[1:]

    base_cmd = tokens[0].lower()
    args_str = " ".join(tokens[1:]).lower()

    if base_cmd in ("pacman", "yay", "paru"):
        if "-syu" in args_str or "-syyu" in args_str:
            return {"state": f"Actualizando sistema ({base_cmd})", "asset": "package"}
        if "-s" in args_str or "-ss" in args_str:
            return {"state": f"Buscando/instalando con {base_cmd}", "asset": "package"}
        if "-r" in args_str or "-rs" in args_str or "-rns" in args_str:
            return {"state": f"Eliminando paquetes ({base_cmd})", "asset": "package"}
        return {"state": f"Gestionando paquetes ({base_cmd})", "asset": "package"}

    if base_cmd in ("apt", "apt-get"):
        if "update" in args_str or "upgrade" in args_str or "dist-upgrade" in args_str:
            return {"state": f"Actualizando repositorios ({base_cmd})", "asset": "package"}
        if "install" in args_str:
            return {"state": f"Instalando paquetes ({base_cmd})", "asset": "package"}
        if "remove" in args_str or "purge" in args_str:
            return {"state": f"Desinstalando paquetes ({base_cmd})", "asset": "package"}
        return {"state": f"Usando {base_cmd}", "asset": "package"}

    if base_cmd == "dpkg":
        if "-i" in args_str or "--install" in args_str:
            return {"state": "Instalando paquete .deb", "asset": "package"}
        return {"state": "Gestionando paquetes dpkg", "asset": "package"}

    if base_cmd in ("dnf", "yum"):
        if "update" in args_str or "upgrade" in args_str:
            return {"state": f"Actualizando sistema ({base_cmd})", "asset": "package"}
        if "install" in args_str:
            return {"state": f"Instalando paquetes ({base_cmd})", "asset": "package"}
        return {"state": f"Usando {base_cmd}", "asset": "package"}

    if base_cmd == "rpm":
        return {"state": "Gestionando paquetes RPM", "asset": "package"}

    if base_cmd == "zypper":
        if "dup" in args_str or "up" in args_str:
            return {"state": "Actualizando openSUSE (zypper)", "asset": "package"}
        if "in" in args_str or "install" in args_str:
            return {"state": "Instalando paquetes (zypper)", "asset": "package"}
        return {"state": "Usando zypper", "asset": "package"}

    if base_cmd == "apk":
        if "add" in args_str:
            return {"state": "Instalando paquetes (apk)", "asset": "package"}
        if "upgrade" in args_str or "update" in args_str:
            return {"state": "Actualizando Alpine (apk)", "asset": "package"}
        return {"state": "Usando apk", "asset": "package"}

    if base_cmd == "emerge":
        return {"state": "Compilando e instalando con emerge", "asset": "package"}

    if base_cmd in ("nix", "nix-shell", "nix-env", "nixos-rebuild"):
        return {"state": f"Operando Nix ({base_cmd})", "asset": "package"}

    if base_cmd == "flatpak":
        if "install" in args_str:
            return {"state": "Instalando Flatpak", "asset": "package"}
        return {"state": "Gestionando Flatpaks", "asset": "package"}

    if base_cmd == "snap":
        if "install" in args_str:
            return {"state": "Instalando Snap", "asset": "package"}
        return {"state": "Gestionando Snaps", "asset": "package"}

    if base_cmd == "brew":
        return {"state": "Gestionando con Homebrew", "asset": "package"}

    if base_cmd in ("pip", "pip3"):
        if "install" in args_str:
            return {"state": "Instalando librerias Python", "asset": "python"}
        return {"state": "Usando pip", "asset": "python"}

    if base_cmd in ("npm", "pnpm", "yarn", "bun"):
        if "install" in args_str or "add" in args_str or "i" in tokens[1:]:
            return {"state": f"Instalando dependencias ({base_cmd})", "asset": "node"}
        if "run" in args_str or "dev" in args_str or "build" in args_str or "start" in args_str:
            return {"state": f"Ejecutando script de {base_cmd}", "asset": "node"}
        return {"state": f"Usando {base_cmd}", "asset": "node"}

    if base_cmd == "cargo":
        if "build" in args_str:
            return {"state": "Compilando proyecto en Rust", "asset": "rust"}
        if "run" in args_str:
            return {"state": "Ejecutando proyecto en Rust", "asset": "rust"}
        if "install" in args_str:
            return {"state": "Instalando binario con Cargo", "asset": "rust"}
        return {"state": "Usando Cargo (Rust)", "asset": "rust"}

    return None
