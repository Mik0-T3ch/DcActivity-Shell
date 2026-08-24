import os

EDITORS_MAP = {
    "nvim": ("Neovim", "neovim"),
    "vim": ("Vim", "vim"),
    "vi": ("Vi", "vim"),
    "nano": ("Nano", "nano"),
    "micro": ("Micro", "editor"),
    "helix": ("Helix", "editor"),
    "hx": ("Helix", "editor"),
    "emacs": ("Emacs", "editor"),
    "code": ("VS Code", "editor"),
    "subl": ("Sublime Text", "editor"),
    "gedit": ("Gedit", "editor"),
    "kate": ("Kate", "editor")
}


def detect_editor(cmd: str):
    tokens = cmd.strip().split()
    if not tokens:
        return None

    if tokens[0] == "sudo" and len(tokens) > 1:
        tokens = tokens[1:]

    base_cmd = tokens[0].lower()
    editor_info = EDITORS_MAP.get(base_cmd)

    if not editor_info:
        return None

    editor_name, asset_key = editor_info

    target_file = None
    for arg in tokens[1:]:
        if not arg.startswith("-") and not arg.startswith("+"):
            target_file = os.path.basename(arg)
            break

    if target_file:
        return {
            "state": f"Editando {target_file} ({editor_name})",
            "asset": asset_key
        }

    return {
        "state": f"Editando en {editor_name}",
        "asset": asset_key
    }
