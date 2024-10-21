class StringWeight:
    def __init__(self, string: str = None, weight: float = 0):
        self.__string = string
        self.__weight = weight

    @property
    def string(self):
        return self.__string

    @string.setter
    def string(self, value: str):
        if isinstance(value, str):
            self.__string = value
        else:
            raise TypeError(f'not {type(value)}')

    @property
    def weight(self):
        return self.__weight

    @weight.setter
    def weight(self, value: float):
        if isinstance(value, float):
            self.__weight = value
        else:
            raise TypeError(f'not {type(value)}')

    def genweight(self):
        if isinstance(self.__string, str):
            __local_weight = 0
            for symbol in self.__string:
                __local_weight += ord(symbol) / 248
            self.__weight = round(__local_weight, 3)
        else:
            raise TypeError

    def __eq__(self, other):
        return self.__weight == other.weight

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        return self.__weight < other.weight

    def __le__(self, other):
        return self.__weight <= other.weight

    def __gt__(self, other):
        return self.__weight > other.weight

    def __ge__(self, other):
        return self.__weight >= other.weight



