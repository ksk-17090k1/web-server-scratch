import logging
import socket

from server_thread import ServerThread


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 8001))
    # 同時に接続を待ち受ける数
    server_socket.listen(5)

    try:
        while True:
            client_socket, addr = server_socket.accept()
            server_thread = ServerThread(client_socket)
            # スレッドの処理自体は非同期なので、start()はすぐ終了しまた次のループに入る
            server_thread.start()
    except KeyboardInterrupt:
        server_socket.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()
