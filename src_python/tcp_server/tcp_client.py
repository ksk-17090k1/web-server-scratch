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
                # client_send.txt の内容をサーバに送信
                # NOTE: セイウチ演算子と、read()でseekが進むことを利用している。地味にすごい。
                while ch := fis.read(1):
                    s.sendall(ch)

                # サーバに送信終了を通知
                # \x は16進数表記の文字を表す
                s.sendall(b"\x00")

                # サーバからのレスポンスを client_recv.txt に保存
                while ch := s.recv(1):
                    fos.write(ch)

    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()
