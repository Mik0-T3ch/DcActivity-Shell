def detect_editor(cmd: str):
    cmd = cmd.lower()

    if cmd.startswith("nvim"):
        return "Editando código"

    if cmd.startswith("vim"):
        return "Editando código"

    if cmd.startswith("nano"):
        return "Editando en Nano"

    return None