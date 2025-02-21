import socket


def main():
    try:
        # サーバソケットの作成
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(("localhost", 8001))
            with (
                open("client_send.txt", "rb") as fis,
                open("client_recv.txt", "wb") as fos,
            ):
                # Send the contents of client_send.txt to the server
                while ch := fis.read(1):
                    s.sendall(ch)
                # Send zero to indicate the end
                s.sendall(b"\x00")
                # Receive the response from the server and write to client_recv.txt
                while ch := s.recv(1):
                    fos.write(ch)
    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()
