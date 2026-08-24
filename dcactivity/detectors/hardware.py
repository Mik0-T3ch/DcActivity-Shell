def detect_hardware(cmd: str):
    tokens = cmd.strip().split()
    if not tokens:
        return None

    if tokens[0] == "sudo" and len(tokens) > 1:
        tokens = tokens[1:]

    base_cmd = tokens[0].lower()
    args_str = " ".join(tokens[1:]).lower()

    if base_cmd in ("tmux", "zellij", "screen", "byobu"):
        if "attach" in args_str or "a" in tokens[1:]:
            return {"state": f"Reconectando sesion ({base_cmd})", "asset": "terminal"}
        return {"state": f"Sesion multiplexada ({base_cmd})", "asset": "terminal"}

    if base_cmd in ("nvidia-smi", "nvtop"):
        return {"state": "Monitoreando GPU Nvidia", "asset": "system"}

    if base_cmd in ("radeontop", "intel_gpu_top"):
        return {"state": f"Monitoreando GPU ({base_cmd})", "asset": "system"}

    if base_cmd in ("sensors", "psensor"):
        return {"state": "Consultando temperaturas y sensores", "asset": "system"}

    if base_cmd in ("lscpu", "lspci", "lsusb", "inxi", "hardinfo"):
        return {"state": f"Inspeccionando hardware ({base_cmd})", "asset": "system"}

    if base_cmd == "powertop":
        return {"state": "Optimizando consumo energetico", "asset": "system"}

    return None
