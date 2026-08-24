def detect_dev(cmd: str):
    tokens = cmd.strip().split()
    if not tokens:
        return None

    if tokens[0] == "sudo" and len(tokens) > 1:
        tokens = tokens[1:]

    base_cmd = tokens[0].lower()
    args_str = " ".join(tokens[1:]).lower()

    if base_cmd in ("docker", "podman"):
        if "compose" in args_str:
            if "up" in args_str:
                return {"state": f"Levantando servicios ({base_cmd} compose)", "asset": "docker"}
            if "down" in args_str:
                return {"state": f"Deteniendo servicios ({base_cmd} compose)", "asset": "docker"}
            return {"state": f"Usando {base_cmd} compose", "asset": "docker"}
        if "build" in args_str:
            return {"state": f"Construyendo imagen ({base_cmd})", "asset": "docker"}
        if "run" in args_str:
            return {"state": f"Ejecutando contenedor ({base_cmd})", "asset": "docker"}
        if "ps" in args_str:
            return {"state": f"Listando contenedores ({base_cmd})", "asset": "docker"}
        if "logs" in args_str:
            return {"state": f"Revisando logs de contenedor", "asset": "docker"}
        return {"state": f"Gestionando contenedores ({base_cmd})", "asset": "docker"}

    if base_cmd == "docker-compose":
        return {"state": "Usando Docker Compose", "asset": "docker"}

    if base_cmd in ("kubectl", "k9s"):
        if "get" in args_str:
            return {"state": "Consultando recursos de Kubernetes", "asset": "k8s"}
        if "apply" in args_str or "create" in args_str:
            return {"state": "Desplegando en Kubernetes", "asset": "k8s"}
        if "logs" in args_str:
            return {"state": "Revisando logs de Kubernetes", "asset": "k8s"}
        return {"state": "Administrando cluster K8s", "asset": "k8s"}

    if base_cmd == "helm":
        return {"state": "Gestionando charts de Helm", "asset": "k8s"}

    if base_cmd == "terraform":
        if "plan" in args_str:
            return {"state": "Generando plan de Terraform", "asset": "terminal"}
        if "apply" in args_str:
            return {"state": "Aplicando infraestructura Terraform", "asset": "terminal"}
        return {"state": "Usando Terraform", "asset": "terminal"}

    if base_cmd in ("ansible", "ansible-playbook"):
        return {"state": "Ejecutando playbook de Ansible", "asset": "terminal"}

    if base_cmd in ("gcc", "g++", "clang", "clang++"):
        return {"state": f"Compilando con {base_cmd}", "asset": "c"}

    if base_cmd in ("make", "cmake", "ninja"):
        return {"state": f"Construyendo con {base_cmd}", "asset": "c"}

    if base_cmd == "go":
        if "run" in args_str:
            return {"state": "Ejecutando app en Go", "asset": "go"}
        if "build" in args_str:
            return {"state": "Compilando binario en Go", "asset": "go"}
        if "test" in args_str:
            return {"state": "Ejecutando tests de Go", "asset": "go"}
        return {"state": "Programando en Go", "asset": "go"}

    if base_cmd in ("python", "python3", "ipython", "ptpython"):
        if len(tokens) > 1 and not tokens[1].startswith("-"):
            script_name = tokens[1].split("/")[-1]
            return {"state": f"Ejecutando {script_name}", "asset": "python"}
        return {"state": "Interprete interactivo Python", "asset": "python"}

    if base_cmd == "pytest":
        return {"state": "Corriendo suite de tests (pytest)", "asset": "python"}

    if base_cmd in ("node", "deno", "bun"):
        if len(tokens) > 1 and not tokens[1].startswith("-"):
            file_name = tokens[1].split("/")[-1]
            return {"state": f"Ejecutando {file_name}", "asset": "node"}
        return {"state": f"Interprete interactivo {base_cmd}", "asset": "node"}

    if base_cmd in ("psql", "mysql", "mongosh", "redis-cli", "sqlite3"):
        return {"state": f"Conectado a BD ({base_cmd})", "asset": "terminal"}

    return None
