import socket


def main() -> None:
    """Connect to given localhost:port and get bot health"""
    HOST = "127.0.0.1"
    PORT = 4040

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        data = s.recv(1024)

    if data == b"healthy":
        print("Healthy!")
    else:
        print(":(")


if __name__ == "__main__":
    main()
