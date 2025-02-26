from urllib.parse import unquote_plus


class HttpServletRequestImpl:
    def __init__(self, method, parameter_map):
        self.method = method
        self.characterEncoding = "ISO-8859-1"
        self.parameterMap = parameter_map

    def get_method(self):
        return self.method

    def get_parameter(self, name):
        values = self.get_parameter_values(name)
        return values[0] if values else None

    # TODO: docoderつかうべきかも
    def get_parameter_values(self, name):
        values = self.parameterMap.get(name)
        if values is None:
            return None
        return [
            unquote_plus(value, encoding=self.characterEncoding) for value in values
        ]

    def set_character_encoding(self, env):
        if not env:
            raise ValueError(f"Unsupported encoding: {env}")
        self.characterEncoding = env
