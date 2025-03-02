import traceback
from pathlib import Path

from servletimpl.servlet_service import ServletService
from servletimpl.web_application import WebApplication
from util.constants import Constants
from util.my_url_decoder import MyURLDecoder
from util.send_response import SendResponse

DOCUMENT_ROOT = "C:\\Apache24\\htdocs"
ERROR_DOCUMENT = "C:\\webserver\\error_document"


class ServerThread:
    def __init__(self, socket):
        self.socket = socket

    def run(self):
        output = None
        try:
            input = self.socket.makefile("rb")
            request_line = None
            method = None
            request_header = {}

            while True:
                line = Util.read_line(input)
                if line is None or line == "":
                    break
                if line.startswith("GET"):
                    method = "GET"
                    request_line = line
                elif line.startswith("POST"):
                    method = "POST"
                    request_line = line
                else:
                    Util.add_request_header(request_header, line)

            if request_line is None:
                return

            req_uri = request_line.split(" ")[1]
            path_and_query = req_uri.split("?")
            path = MyURLDecoder.decode(path_and_query[0], "UTF-8")
            query = path_and_query[1] if len(path_and_query) > 1 else None
            output = self.socket.makefile("wb")

            app_dir = path[1:].split("/")[0]
            web_app = WebApplication.search_web_application(app_dir)
            if web_app:
                servlet_info = web_app.search_servlet(path[len(app_dir) + 1 :])
                if servlet_info:
                    ServletService.do_service(
                        method, query, servlet_info, request_header, input, output
                    )
                    return

            ext = req_uri.split(".")[-1]
            if path.endswith("/"):
                path += "index.html"
                ext = "html"

            path_obj = Path(DOCUMENT_ROOT + path).resolve()
            if not path_obj.exists():
                SendResponse.send_not_found_response(output, ERROR_DOCUMENT)
                return
            if not str(path_obj).startswith(DOCUMENT_ROOT):
                SendResponse.send_not_found_response(output, ERROR_DOCUMENT)
                return
            if path_obj.is_dir():
                host = request_header.get("HOST")
                location = f"http://{host if host else Constants.SERVER_NAME}{path}/"
                SendResponse.send_move_permanently_response(output, location)
                return

            with path_obj.open("rb") as fis:
                SendResponse.send_ok_response(output, fis, ext)

        except Exception:
            traceback.print_exc()
        finally:
            try:
                if output:
                    output.close()
                self.socket.close()
            except Exception:
                traceback.print_exc()
