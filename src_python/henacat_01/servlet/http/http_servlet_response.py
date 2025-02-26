from abc import ABC, abstractmethod
from typing import TextIO


class HttpServletResponse(ABC):
    SC_OK = 200
    SC_FOUND = 302

    @abstractmethod
    def set_content_type(self, content_type: str):
        pass

    @abstractmethod
    def set_character_encoding(self, charset: str):
        pass

    @abstractmethod
    def get_writer(self) -> TextIO:
        pass

    @abstractmethod
    def send_redirect(self, location: str):
        pass

    @abstractmethod
    def set_status(self, sc: int):
        pass
