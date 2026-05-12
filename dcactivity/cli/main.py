print("[DEBUG] main.py loaded")

import argparse

from dcactivity.core.engine import Engine


def main():
    print("[DEBUG] main() executed")

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--cmd",
        type=str,
        required=True
    )

    args = parser.parse_args()

    print(f"[DEBUG] CMD: {args.cmd}")

    engine = Engine()

    engine.handle_command(args.cmd)


if __name__ == "__main__":
    main()