import datetime
import io


class Util:
    @staticmethod
    def write_line(output_stream: io.BufferedWriter, line: str) -> None:
        # 改行コードがCRLFであることに注意
        # output_streamがバイナリモードなので、バイナリにencodingしてから書き込む
        output_stream.write((line + "\r\n").encode())

    @staticmethod
    def get_date_string_utc() -> str:
        return datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")

    @staticmethod
    def get_content_type(ext) -> str:
        content_types = {
            "html": "text/html",
            "txt": "text/plain",
            "jpg": "image/jpeg",
            "png": "image/png",
            "css": "text/css",
            "js": "application/javascript",
        }
        return content_types.get(ext, "application/octet-stream")
