import os
from pathlib import Path


def get_git_context(cwd: str):
    if not cwd:
        return None

    try:
        current_dir = Path(cwd).resolve()
        for parent in [current_dir] + list(current_dir.parents):
            git_dir = parent / ".git"
            if git_dir.exists():
                repo_name = parent.name
                branch_name = None

                # Intentar leer .git/HEAD de forma rapida y nativa
                if git_dir.is_dir():
                    head_file = git_dir / "HEAD"
                    if head_file.exists():
                        head_content = head_file.read_text(encoding="utf-8", errors="ignore").strip()
                        if head_content.startswith("ref: refs/heads/"):
                            branch_name = head_content.replace("ref: refs/heads/", "")
                        elif len(head_content) >= 7:
                            branch_name = head_content[:7]  # Detached commit sha

                return {
                    "repo": repo_name,
                    "branch": branch_name or "main"
                }
    except Exception:
        pass

    return None


def detect_git(cmd: str):
    tokens = cmd.strip().split()
    if not tokens:
        return None

    if tokens[0] == "sudo" and len(tokens) > 1:
        tokens = tokens[1:]

    base_cmd = tokens[0].lower()
    if base_cmd != "git":
        return None

    args = tokens[1:]
    if not args:
        return {"state": "Usando Git", "asset": "git"}

    sub = args[0].lower()

    if sub == "commit":
        return {"state": "Haciendo commit", "asset": "git"}
    if sub == "push":
        return {"state": "Subiendo cambios (git push)", "asset": "git"}
    if sub == "pull":
        return {"state": "Descargando cambios (git pull)", "asset": "git"}
    if sub == "fetch":
        return {"state": "Consultando cambios remotos", "asset": "git"}
    if sub in ("checkout", "switch"):
        branch_target = args[1] if len(args) > 1 else ""
        if branch_target and not branch_target.startswith("-"):
            return {"state": f"Cambiando a rama {branch_target}", "asset": "git"}
        return {"state": "Cambiando de rama", "asset": "git"}
    if sub == "merge":
        return {"state": "Fusionando ramas (git merge)", "asset": "git"}
    if sub == "rebase":
        return {"state": "Rebasando commits (git rebase)", "asset": "git"}
    if sub == "clone":
        repo = args[1].split("/")[-1].replace(".git", "") if len(args) > 1 else ""
        if repo:
            return {"state": f"Clonando {repo}", "asset": "git"}
        return {"state": "Clonando repositorio", "asset": "git"}
    if sub == "status":
        return {"state": "Revisando estado del repo", "asset": "git"}
    if sub == "diff":
        return {"state": "Viendo diferencias en codigo", "asset": "git"}
    if sub == "log":
        return {"state": "Revisando historial de commits", "asset": "git"}
    if sub == "stash":
        return {"state": "Guardando cambios en stash", "asset": "git"}
    if sub == "branch":
        return {"state": "Gestionando ramas en Git", "asset": "git"}

    return {"state": f"Operacion Git ({sub})", "asset": "git"}
