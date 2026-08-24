import json
import socket
import sys

from dcactivity.core.engine import Engine

HOST = "127.0.0.1"
PORT = 4545


def start_server():
    engine = Engine()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server.bind((HOST, PORT))
        server.listen(10)
    except Exception as e:
        print(f"[DAEMON FATAL] No se pudo iniciar el servidor en {HOST}:{PORT}: {e}")
        sys.exit(1)

    print(f"[DAEMON] Escuchando en {HOST}:{PORT}...")

    while True:
        try:
            client, addr = server.accept()
            client.settimeout(1.0)
            data_raw = client.recv(4096).decode("utf-8", errors="ignore").strip()

            if data_raw:
                try:
                    payload = json.loads(data_raw)
                    engine.handle_event(payload)
                except json.JSONDecodeError:
                    engine.handle_command(data_raw)

            client.close()
        except Exception as e:
            pass


if __name__ == "__main__":
    start_server()
