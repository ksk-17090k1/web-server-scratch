import logging
import pathlib
import threading
import typing
import urllib.parse

from my_url_decoder import MyURLDecoder
from send_response import SendResponse

"""リクエストの例
GET / HTTP/1.1
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Accept-Encoding: gzip, deflate, br, zstd
Accept-Language: ja,en-US;q=0.9,en;q=0.8
Cache-Control: max-age=0
Connection: keep-alive
Host: localhost:8001
"""


DOCUMENT_ROOT = (
    "/Users/ksk_inagaki/repos/web_server_scratch/src_python/modoki_02/htdocs"
)
ERROR_DOCUMENT = (
    "/Users/ksk_inagaki/repos/web_server_scratch/src_python/modoki_02/error_document"
)
SERVER_NAME = "localhost:8001"

logger = logging.getLogger(__name__)


# threading.Threadはrunメソッドをスレッドで実行する
class ServerThread(threading.Thread):
    def __init__(self, client_socket):
        super().__init__()
        self.socket = client_socket

    def run(self):
        output_stream: typing.IO | None = None
        try:
            # socketのIFとしてfile objectを作成
            # "rb"なのでバイナリモードで読み込む
            input_stream: typing.IO = self.socket.makefile("rb")
            path: str | None = None
            ext: str | None = None
            host: str | None = None

            while True:
                # １行読み込む
                line = input_stream.readline().decode("utf-8").strip()
                # 空文字の場合
                if not line:
                    break
                if line.startswith("GET"):
                    # path-name/index.htmlなど
                    # 入力はURLエンコーディングされているのでdecodeする
                    path = MyURLDecoder.decode(
                        urllib.parse.unquote(line.split(" ")[1]), "utf-8"
                    )
                    logger.debug(f"path: {path}")
                    # htmlなど
                    ext = path.split(".")[-1] if "." in path else None
                    logger.debug(f"ext: {ext}")
                elif line.startswith("Host:"):
                    host = line[len("Host: ") :]
                    logger.debug(f"host: {host}")

            if path is None:
                return

            # パスの末尾が"/"の場合はindex.htmlを追加
            if path.endswith("/"):
                path += "index.html"
                ext = "html"

            # "wb"なのでバイナリモードで書き込む
            output_stream = self.socket.makefile("wb")

            # パスの検証
            path_obj = pathlib.Path(DOCUMENT_ROOT + path).resolve()
            try:
                # strict=Trueでファイルが存在しない場合はOSErrorを送出
                real_path = path_obj.resolve(strict=True)
            # いわゆる404の判定
            except FileNotFoundError:
                SendResponse.send_not_found_response(output_stream, ERROR_DOCUMENT)
                return

            # directory traversal対策
            if not str(real_path).startswith(DOCUMENT_ROOT):
                SendResponse.send_not_found_response(output_stream, ERROR_DOCUMENT)
                return

            # パスがディレクトリの場合はリダイレクトする
            if real_path.is_dir():
                location = f"http://{host if host else SERVER_NAME}{path}/"
                SendResponse.send_move_permanently_response(output_stream, location)
                return

            try:
                with open(real_path, "rb") as file_input_stream:
                    SendResponse.send_ok_response(output_stream, file_input_stream, ext)
            except FileNotFoundError:
                SendResponse.send_not_found_response(output_stream)
        except Exception as ex:
            print(ex)
        finally:
            if output_stream:
                output_stream.close()
            self.socket.close()
