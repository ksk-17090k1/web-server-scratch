import socket
import sys

sys.path.append(".")

from server_thread import ServerThread
from servletimpl.web_application import WebApplication


def main():
    app = WebApplication.create_instance("testbbs")
    app.add_servlet("/ShowBBS", "ShowBBS")
    app.add_servlet("/PostBBS", "PostBBS")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind(("localhost", 8001))
        server.listen()
        while True:
            client_socket, _ = server.accept()
            server_thread = ServerThread(client_socket)
            server_thread.run()


if __name__ == "__main__":
    main()
