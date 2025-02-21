import socket


def main():
    # サーバソケットの作成
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind(("localhost", 8001))
        server.listen(1)
        print("クライアントからの接続を待ちます。")

        # クライアントソケット(conn)の作成
        # connも中身はsocketオブジェクト
        # クライアントからの通信が来るまでaccept()は実行完了しない
        conn, addr = server.accept()
        with conn:
            print("クライアント接続。")

            with (
                open("server_recv.txt", "wb") as fos,
                open("server_send.txt", "rb") as fis,
            ):
                # クライアントから受け取った内容をserver_recv.txtに出力
                while True:
                    data = conn.recv(1)
                    if data == b"\x00":  # 終了のマークとして0を送付してくる
                        break
                    fos.write(data)

                # server_send.txtの内容をクライアントに送付
                while data := fis.read(1):
                    conn.sendall(data)

            print("通信を終了しました。")


if __name__ == "__main__":
    main()
