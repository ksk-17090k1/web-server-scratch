import importlib
from io import BytesIO
from urllib.parse import parse_qs

from http_servlet_request_impl import HttpServletRequestImpl
from http_servlet_response_impl import HttpServletResponseImpl
from servlet.http.http_servlet_response import HttpServletResponse
from util.constants import Constants
from util.send_response import SendResponse


class ServletService:
    @staticmethod
    def create_servlet(info):
        module_name, class_name = info.servletClassName.rsplit(".", 1)
        module = importlib.import_module(module_name)
        clazz = getattr(module, class_name)
        return clazz()

    @staticmethod
    def string_to_map(query):
        return {
            k: v if isinstance(v, list) else [v] for k, v in parse_qs(query).items()
        }

    @staticmethod
    def read_to_size(input_stream, size):
        return input_stream.read(size).decode("utf-8")

    @staticmethod
    def do_service(method, query, info, request_header, input_stream, output_stream):
        if info.servlet is None:
            info.servlet = ServletService.create_servlet(info)

        output_buffer = BytesIO()
        resp = HttpServletResponseImpl(output_buffer)

        if method == "GET":
            param_map = ServletService.string_to_map(query)
            req = HttpServletRequestImpl("GET", param_map)
        elif method == "POST":
            content_length = int(request_header.get("CONTENT-LENGTH"))
            body = ServletService.read_to_size(input_stream, content_length)
            param_map = ServletService.string_to_map(body)
            req = HttpServletRequestImpl("POST", param_map)
        else:
            raise AssertionError(f"BAD METHOD: {method}")

        info.servlet.service(req, resp)

        if resp.status == HttpServletResponse.SC_OK:
            SendResponse.send_ok_response_header(output_stream, resp.content_type)
            resp.print_writer.flush()
            output_stream.write(output_buffer.getvalue())
        elif resp.status == HttpServletResponse.SC_FOUND:
            if resp.redirect_location.startswith("/"):
                host = request_header.get("HOST")
                redirect_location = f"http://{host if host else Constants.SERVER_NAME}{resp.redirect_location}"
            else:
                redirect_location = resp.redirect_location
            SendResponse.send_found_response(output_stream, redirect_location)
