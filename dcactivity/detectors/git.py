def detect_git(cmd: str):
    cmd = cmd.lower()

    if "git commit" in cmd:
        return "Haciendo commit"

    if "git push" in cmd:
        return "Subiendo cambios"

    if "git pull" in cmd:
        return "Actualizando repositorio"

    return None