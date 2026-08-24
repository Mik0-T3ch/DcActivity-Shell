def detect_network(cmd: str):
    tokens = cmd.strip().split()
    if not tokens:
        return None

    if tokens[0] == "sudo" and len(tokens) > 1:
        tokens = tokens[1:]

    base_cmd = tokens[0].lower()
    args_str = " ".join(tokens[1:]).lower()

    if base_cmd == "ssh":
        host = tokens[1] if len(tokens) > 1 and not tokens[1].startswith("-") else ""
        if host:
            return {"state": f"Conectado por SSH a {host}", "asset": "network"}
        return {"state": "Sesion remota SSH", "asset": "network"}

    if base_cmd == "scp" or base_cmd == "rsync":
        return {"state": f"Transfiriendo archivos ({base_cmd})", "asset": "network"}

    if base_cmd in ("ping", "ping6"):
        target = tokens[1] if len(tokens) > 1 and not tokens[1].startswith("-") else ""
        if target:
            return {"state": f"Haciendo ping a {target}", "asset": "network"}
        return {"state": "Haciendo ping", "asset": "network"}

    if base_cmd in ("curl", "wget", "http", "xh"):
        return {"state": f"Peticion de red con {base_cmd}", "asset": "network"}

    if base_cmd in ("nmap", "wireshark", "tshark", "tcpdump"):
        return {"state": f"Auditoria de red ({base_cmd})", "asset": "network"}

    if base_cmd in ("netstat", "ss", "lsof", "ip", "ifconfig"):
        return {"state": "Inspeccionando red y sockets", "asset": "network"}

    if base_cmd in ("ufw", "iptables", "nft"):
        return {"state": "Configurando firewall", "asset": "network"}

    return None
