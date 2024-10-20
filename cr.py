from fuzzywuzzy import process


class StringWeight:
    def __init__(self, string: str, weight: float):
        self.__string = None
        self.__weight = None

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
            self.__weight = __local_weight
        else:
            raise TypeError


# x = ['выключить пк', 'открой', 'прибавь звук']
#
# print(process.extract('Отключи пк и прибавь звук', x, limit=16))
# from math import ceil
#
# x = 'прибавь звук'
# cop = 0
# nc = 0

# cop += i/64
# # cop += ord(i)/2048
# if i % 2 == 0:
#     cop += len(str(i))
# elif i % 2 != 0:

# nc += len(str(i))
# print(round(cop, 2))
