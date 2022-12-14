import argparse
import socket
import sys

parser = argparse.ArgumentParser(description="Perform a discord bot health check.")
parser.add_argument(
    "--port",
    default=40404,
    type=int,
    help="the port of the server to connect to",
)
parser.add_argument(
    "--timeout",
    default=10,
    type=int,
    help="the socket timeout (in seconds) when connecting to the server",
)


def main() -> None:
    """Connect to given server and get health status. Exit 1 on error / unhealthy"""
    args = parser.parse_args()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.settimeout(args.timeout)
            s.connect(("127.0.0.1", args.port))
            data = s.recv(1024)
        except (ConnectionError, socket.timeout) as ex:
            print(f"Exception: {ex.__class__.__name__}: {ex}")
            data = b""

    if data == b"healthy":
        print("Healthy!")
        sys.exit(0)
    else:
        print("Not healthy")
        sys.exit(1)


if __name__ == "__main__":
    main()
