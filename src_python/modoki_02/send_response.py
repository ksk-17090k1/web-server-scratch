import os
import typing

from util import Util


class SendResponse:
    @staticmethod
    def send_ok_response(
        output_stream: typing.IO, file_input_stream: typing.IO, extension: str
    ):
        Util.write_line(output_stream, "HTTP/1.1 200 OK")
        Util.write_line(output_stream, "Date: " + Util.get_date_string_utc())
        Util.write_line(output_stream, "Server: Modoki/0.2")
        Util.write_line(output_stream, "Connection: close")
        Util.write_line(
            output_stream, "Content-type: " + Util.get_content_type(extension)
        )
        Util.write_line(output_stream, "")

        while chunk := file_input_stream.read(1024):
            output_stream.write(chunk)

    @staticmethod
    def send_move_permanently_response(output_stream: typing.IO, location):
        Util.write_line(output_stream, "HTTP/1.1 301 Moved Permanently")
        Util.write_line(output_stream, "Date: " + Util.get_date_string_utc())
        Util.write_line(output_stream, "Server: Modoki/0.2")
        Util.write_line(output_stream, "Location: " + location)
        Util.write_line(output_stream, "Connection: close")
        Util.write_line(output_stream, "")

    @staticmethod
    def send_not_found_response(output_stream: typing.IO, error_document_root: str):
        Util.write_line(output_stream, "HTTP/1.1 404 Not Found")
        Util.write_line(output_stream, "Date: " + Util.get_date_string_utc())
        Util.write_line(output_stream, "Server: Modoki/0.2")
        Util.write_line(output_stream, "Connection: close")
        Util.write_line(output_stream, "Content-type: text/html")
        Util.write_line(output_stream, "")

        file_path = os.path.join(error_document_root, "404.html")
        try:
            with open(file_path, "rb") as input_stream:
                while chunk := input_stream.read(1024):
                    output_stream.write(chunk)
        except FileNotFoundError:
            Util.write_line(
                output_stream, "<html><body><h1>404 Not Found</h1></body></html>"
            )
