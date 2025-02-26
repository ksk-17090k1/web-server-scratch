import datetime
import io

import pytz


class Util:
    @staticmethod
    def read_line(input_stream):
        ret = ""
        while True:
            ch = input_stream.read(1)
            if not ch:
                return None if ret == "" else ret
            if ch == b"\r":
                continue
            elif ch == b"\n":
                break
            else:
                ret += ch.decode()
        return ret

    @staticmethod
    def write_line(output_stream, string):
        output_stream.write(string.encode())
        output_stream.write(b"\r\n")

    @staticmethod
    def get_date_string_utc():
        now = datetime.datetime.now(pytz.utc)
        return now.strftime("%a, %d %b %Y %H:%M:%S GMT")

    content_type_map = {
        "html": "text/html",
        "htm": "text/html",
        "txt": "text/plain",
        "css": "text/css",
        "png": "image/png",
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "gif": "image/gif",
    }

    @staticmethod
    def get_content_type(ext):
        return Util.content_type_map.get(ext.lower(), "application/octet-stream")
