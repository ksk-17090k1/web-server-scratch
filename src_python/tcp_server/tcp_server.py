import socket

# ブラウザで以下を打つとHTTPレスポンスがserver_recv.txtに出力される
# http://localhost:8001/index.html


def main():
    # サーバソケットの作成
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind(("localhost", 8001))
        # 同時に接続を待ち受ける数
        server.listen(1)
        print("クライアントからの接続を待ちます。")

        # クライアントソケット(conn)の作成
        # connも中身はsocketオブジェクト
        # クライアントからの通信が来るまでaccept()は実行完了しない
        conn, addr = server.accept()
        with conn:
            print("クライアント接続。")

            with (
                # "rb"や"wb"はバイナリモードでファイルを開く
                open("server_recv.txt", "wb") as file_output_stream,
                open("server_send.txt", "rb") as file_input_stream,
            ):
                # クライアントから受け取った内容をserver_recv.txtに出力
                while True:
                    data = conn.recv(1)
                    if data == b"\x00":  # 終了のマークとして0を送付してくる
                        break
                    file_output_stream.write(data)

                # server_send.txtの内容をクライアントに送付
                # read(1)で1バイトずつ読み込んでいる
                while data := file_input_stream.read(1):
                    conn.sendall(data)

            print("通信を終了しました。")


if __name__ == "__main__":
    main()
