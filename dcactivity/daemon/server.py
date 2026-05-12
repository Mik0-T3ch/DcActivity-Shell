import socket

from dcactivity.core.engine import Engine

HOST = "127.0.0.1"
PORT = 4545


def start_server():
    engine = Engine()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind((HOST, PORT))

    server.listen(5)

    print(f"[DAEMON] Listening on {HOST}:{PORT}")

    while True:
        client, addr = server.accept()

        data = client.recv(1024).decode().strip()

        if data:
            print(f"[EVENT] {data}")

            engine.handle_command(data)

        client.close()


if __name__ == "__main__":
    start_server()