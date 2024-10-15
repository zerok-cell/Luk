class ResponseAi:
    def __init__(self):
        self.__token: int = None
        self.__text: str = None
        self.__split_text: list[str] = None
        self.__request_status: bool = None

    def __bool__(self):
        if self.reqstatus is False or None:
            return False
        else:
            return True

    @property
    def all(self):
        return {
            'text': self.__text,
            'token': self.__token,
            'split_text': self.__split_text
        }

    @all.setter
    def all(self, value: dict[str, list[str] | int | str]):
        if len(value) == 3:
            self.__token = value.get('token')
            self.__text = value.get('text')
            self.__split_text = value.get('split_text')
        else:
            raise ValueError('Не все данные введены')

    @property
    def void_text(self):
        if self.__text.strip() == '':
            return True
        return False

    @property
    def token(self):
        return self.__token

    @property
    def text(self):
        return self.__text

    @property
    def splittxt(self):
        return self.__split_text

    @property
    def reqstatus(self):
        return self.__request_status

    @token.setter
    def token(self, value: int):
        if isinstance(value, int):
            self.__token = value
        else:
            raise TypeError(f'Ожидалось: "int", дано: "{type(value)}"')

    @reqstatus.setter
    def reqstatus(self, value):
        if isinstance(value, bool):
            self.__request_status = value

    @text.setter
    def text(self, value: str):
        if isinstance(value, str):
            self.__text = value
        else:
            raise TypeError(f'Ожидалось: "str", дано: "{type(value)}"')

    @splittxt.setter
    def splittxt(self, value: list[str]):
        if isinstance(value, list):
            self.__split_text = value
        else:
            raise TypeError(f'Ожидалось: "list", дано: "{type(value)}"')

