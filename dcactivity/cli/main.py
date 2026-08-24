import argparse
import json
import os
import socket
import sys
import time

HOST = "127.0.0.1"
PORT = 4545


def send_event(cmd: str, cwd: str = None, shell_name: str = None):
    if not cwd:
        cwd = os.getcwd()

    if not shell_name:
        shell_env = os.environ.get("SHELL", "")
        shell_name = os.path.basename(shell_env) if shell_env else "shell"

    payload = {
        "cmd": cmd,
        "cwd": cwd,
        "shell": shell_name,
        "timestamp": int(time.time())
    }

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(0.5)

    try:
        client.connect((HOST, PORT))
        data = json.dumps(payload).encode("utf-8")
        client.sendall(data)
    except Exception:
        # Silencioso para no ensuciar la salida de la terminal si el daemon no esta activo
        pass
    finally:
        try:
            client.close()
        except Exception:
            pass


def main():
    parser = argparse.ArgumentParser(description="DcActivity CLI Collector")

    parser.add_argument(
        "--cmd",
        type=str,
        required=True,
        help="Comando ejecutado en la terminal"
    )
    parser.add_argument(
        "--cwd",
        type=str,
        default=None,
        help="Directorio de trabajo actual"
    )
    parser.add_argument(
        "--shell",
        type=str,
        default=None,
        help="Nombre de la shell (bash, zsh, fish)"
    )

    args = parser.parse_args()
    send_event(args.cmd, args.cwd, args.shell)


if __name__ == "__main__":
    main()
