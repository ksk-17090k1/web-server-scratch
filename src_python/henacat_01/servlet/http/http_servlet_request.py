from abc import ABC, abstractmethod
from typing import List


class HttpServletRequest(ABC):
    @abstractmethod
    def get_method(self) -> str:
        pass

    @abstractmethod
    def get_parameter(self, name: str) -> str:
        pass

    @abstractmethod
    def get_parameter_values(self, name: str) -> List[str]:
        pass

    @abstractmethod
    def set_character_encoding(self, env: str) -> None:
        pass
