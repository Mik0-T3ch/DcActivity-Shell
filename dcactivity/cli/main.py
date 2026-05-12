import argparse
import socket

HOST = "127.0.0.1"
PORT = 4545


def send_event(cmd: str):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((HOST, PORT))

        client.send(cmd.encode())

    except Exception as e:
        print(f"[CLIENT ERROR] {e}")

    finally:
        client.close()


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--cmd",
        type=str,
        required=True
    )

    args = parser.parse_args()

    send_event(args.cmd)


if __name__ == "__main__":
    main()