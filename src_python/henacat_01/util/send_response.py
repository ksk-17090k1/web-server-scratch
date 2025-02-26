from .Util import Util


class SendResponse:
    @staticmethod
    def send_ok_response_header(output_stream, content_type):
        Util.write_line(output_stream, "HTTP/1.1 200 OK")
        Util.write_line(output_stream, "Date: " + Util.get_date_string_utc())
        Util.write_line(output_stream, "Server: Henacat/0.1")
        Util.write_line(output_stream, "Connection: close")
        Util.write_line(output_stream, "Content-type: " + content_type)
        Util.write_line(output_stream, "")

    @staticmethod
    def send_ok_response(output_stream, input_stream, ext):
        SendResponse.send_ok_response_header(output_stream, Util.get_content_type(ext))
        while True:
            ch = input_stream.read(1)
            if not ch:
                break
            output_stream.write(ch)

    @staticmethod
    def send_move_permanently_response(output_stream, location):
        Util.write_line(output_stream, "HTTP/1.1 301 Moved Permanently")
        Util.write_line(output_stream, "Date: " + Util.get_date_string_utc())
        Util.write_line(output_stream, "Server: Henacat/0.1")
        Util.write_line(output_stream, "Location: " + location)
        Util.write_line(output_stream, "Connection: close")
        Util.write_line(output_stream, "")

    @staticmethod
    def send_found_response(output_stream, location):
        Util.write_line(output_stream, "HTTP/1.1 302 Found")
        Util.write_line(output_stream, "Date: " + Util.get_date_string_utc())
        Util.write_line(output_stream, "Server: Henacat/0.1")
        Util.write_line(output_stream, "Location: " + location)
        Util.write_line(output_stream, "Connection: close")
        Util.write_line(output_stream, "")

    @staticmethod
    def send_not_found_response(output_stream, error_document_root):
        Util.write_line(output_stream, "HTTP/1.1 404 Not Found")
        Util.write_line(output_stream, "Date: " + Util.get_date_string_utc())
        Util.write_line(output_stream, "Server: Henacat/0.1")
        Util.write_line(output_stream, "Connection: close")
        Util.write_line(output_stream, "Content-type: text/html")
        Util.write_line(output_stream, "")
        with open(f"{error_document_root}/404.html", "rb") as fis:
            while True:
                ch = fis.read(1)
                if not ch:
                    break
                output_stream.write(ch)
