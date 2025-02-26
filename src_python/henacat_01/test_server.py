import socket


def main():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind(("localhost", 8001))
            server_socket.listen(1)
            print("クライアントからの接続を待ちます。")
            conn, addr = server_socket.accept()
            with conn:
                print("クライアント接続。")
                with open("server_recv.txt", "wb") as file_output_stream:
                    while True:
                        data = conn.recv(1)
                        if not data:
                            break
                        file_output_stream.write(data)
    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()
