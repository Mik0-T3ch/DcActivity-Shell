import argparse
import json
import os
import signal
import socket
import subprocess
import sys
import time
from pathlib import Path

HOST = "127.0.0.1"
PORT = 4545


def is_daemon_running():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.3)
    try:
        sock.connect((HOST, PORT))
        sock.close()
        return True
    except Exception:
        return False


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
        pass
    finally:
        try:
            client.close()
        except Exception:
            pass


def cmd_start():
    if is_daemon_running():
        print("[DcActivity] El daemon ya se encuentra en ejecucion.")
        return

    print("[DcActivity] Iniciando daemon en segundo plano...")
    if sys.platform == "win32":
        creationflags = subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS
        subprocess.Popen(
            [sys.executable, "-m", "dcactivity.daemon.server"],
            creationflags=creationflags,
            close_fds=True
        )
    else:
        subprocess.Popen(
            [sys.executable, "-m", "dcactivity.daemon.server"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            start_new_session=True
        )
    time.sleep(0.5)
    if is_daemon_running():
        print("[DcActivity] Daemon iniciado correctamente.")
    else:
        print("[DcActivity] Daemon lanzado.")


def cmd_stop():
    if not is_daemon_running():
        print("[DcActivity] El daemon no esta en ejecucion.")
        return

    print("[DcActivity] Deteniendo daemon...")
    if sys.platform != "win32":
        try:
            subprocess.run(["pkill", "-f", "dcactivity.daemon.server"], check=False)
            print("[DcActivity] Daemon detenido.")
        except Exception as e:
            print(f"[DcActivity ERROR] No se pudo detener el proceso: {e}")
    else:
        print("[DcActivity] Deten el proceso en el Administrador de Tareas en Windows.")


def cmd_status():
    running = is_daemon_running()
    status_str = "ACTIVO (Online)" if running else "INACTIVO (Offline)"
    print(f"Estado del daemon: {status_str}")
    print(f"Puerto local: {HOST}:{PORT}")

    from dcactivity.detectors.distro import get_distro_info
    distro = get_distro_info()
    print(f"Sistema detectado: {distro.get('name')} (Asset: {distro.get('asset_key')})")


def cmd_test(command_str: str):
    from dcactivity.core.engine import Engine
    print(f"\n--- Probando deteccion para: '{command_str}' ---")
    engine = Engine()
    detected = engine.detect(command_str)
    
    if isinstance(detected, dict):
        state = detected.get("state")
        asset = detected.get("asset")
    else:
        state = str(detected)
        asset = None

    cwd = os.getcwd()
    from dcactivity.detectors.git import get_git_context
    git_ctx = get_git_context(cwd)

    details_val = f"{git_ctx['repo']} ({git_ctx['branch']})" if git_ctx else os.path.basename(cwd)
    try:
        print(f"Detalles (Linea 1): {details_val}")
        print(f"Estado   (Linea 2): {state}")
    except UnicodeEncodeError:
        print(f"Detalles (Linea 1): {details_val.encode('ascii', 'replace').decode('ascii')}")
        print(f"Estado   (Linea 2): {state.encode('ascii', 'replace').decode('ascii')}")

    print(f"Large Asset       : {engine.distro.get('asset_key')}")
    print(f"Small Asset       : {asset or 'Ninguno'}")
    print("--------------------------------------------------\n")


def cmd_config(show=True):
    from dcactivity.core.config import Config, USER_CONFIG_PATH
    cfg = Config()
    print(f"Archivo de config: {USER_CONFIG_PATH}")
    print(json.dumps(cfg.data, indent=2))


def main():
    parser = argparse.ArgumentParser(
        prog="dcactivity",
        description="DcActivity: Discord Rich Presence para la terminal"
    )

    subparsers = parser.add_subparsers(dest="subcommand", help="Comandos disponibles")

    subparsers.add_parser("start", help="Inicia el daemon en segundo plano")
    subparsers.add_parser("stop", help="Detiene el daemon")
    subparsers.add_parser("status", help="Muestra el estado del daemon")
    
    test_parser = subparsers.add_parser("test", help="Prueba el resultado de un comando")
    test_parser.add_argument("cmd_to_test", type=str, help="Comando a probar")

    subparsers.add_parser("config", help="Muestra la configuracion activa")

    parser.add_argument("--cmd", type=str, default=None, help="Comando ejecutado (para hooks)")
    parser.add_argument("--cwd", type=str, default=None, help="Directorio de trabajo")
    parser.add_argument("--shell", type=str, default=None, help="Shell usada (bash/zsh/fish)")

    args = parser.parse_args()

    if args.cmd is not None:
        send_event(args.cmd, args.cwd, args.shell)
        return

    if args.subcommand == "start":
        cmd_start()
    elif args.subcommand == "stop":
        cmd_stop()
    elif args.subcommand == "status":
        cmd_status()
    elif args.subcommand == "test":
        cmd_test(args.cmd_to_test)
    elif args.subcommand == "config":
        cmd_config()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
