def detect_security(cmd: str):
    tokens = cmd.strip().split()
    if not tokens:
        return None

    if tokens[0] == "sudo" and len(tokens) > 1:
        tokens = tokens[1:]

    base_cmd = tokens[0].lower()
    args_str = " ".join(tokens[1:]).lower()

    if base_cmd in ("nmap", "rustscan", "masscan"):
        return {"state": f"Escaneando red y puertos ({base_cmd})", "asset": "network"}

    if base_cmd in ("wireshark", "tshark", "tcpdump"):
        return {"state": f"Analizando trafico de red ({base_cmd})", "asset": "network"}

    if base_cmd in ("burpsuite", "zaproxy", "mitmproxy"):
        return {"state": f"Interceptando trafico ({base_cmd})", "asset": "network"}

    if base_cmd == "sqlmap":
        return {"state": "Auditoria de inyeccion SQL (sqlmap)", "asset": "terminal"}

    if base_cmd in ("gobuster", "ffuf", "dirb", "feroxbuster", "wfuzz"):
        return {"state": f"Fuzzing de rutas web ({base_cmd})", "asset": "terminal"}

    if base_cmd in ("nikto", "wpscan", "nuclei"):
        return {"state": f"Escaneo de vulnerabilidades ({base_cmd})", "asset": "terminal"}

    if base_cmd in ("john", "hashcat"):
        return {"state": f"Auditoria de hashes ({base_cmd})", "asset": "terminal"}

    if base_cmd in ("hydra", "medusa"):
        return {"state": f"Auditoria de autenticacion ({base_cmd})", "asset": "terminal"}

    if base_cmd in ("msfconsole", "msfvenom"):
        return {"state": "Operando Metasploit Framework", "asset": "terminal"}

    if base_cmd in ("aircrack-ng", "airodump-ng", "aireplay-ng", "wifite", "kismet"):
        return {"state": f"Auditoria inalambrica ({base_cmd})", "asset": "network"}

    if base_cmd in ("ghidra", "radare2", "r2", "cutter", "gdb", "ida", "ida64"):
        return {"state": f"Ingenieria inversa ({base_cmd})", "asset": "terminal"}

    return None
