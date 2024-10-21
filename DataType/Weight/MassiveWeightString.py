from typing import Iterator

from StringWeight import StringWeight


class MassiveWeight(object):
    def __init__(self, *args: str):
        self.data_input = args
        self.__listweight: list[StringWeight] = []
        self.index: int = 0

    def genlist(self) -> list[StringWeight]:
        for string in self.data_input:
            if isinstance(string[0], str) and (isinstance(string[1], float)):
                __string_weight = StringWeight(string[0], string[1])
                self.__listweight.append(__string_weight)
        return self.__listweight

    def crushing_list(self, for_recursion: list | None = None) -> list:
        if len(for_recursion) <= 1:
            return for_recursion
        len_list = len(for_recursion) // 2
        return self.merge(self.crushing_list(for_recursion[:len_list]),
                          self.crushing_list(for_recursion[len_list:]))

    def merge(self, left, right):
        indexl = indexr = 0
        result = []
        while indexl < len(left) and indexr < len(right):
            if left[indexl] > right[indexr]:
                result.append(left[indexl])
                indexl += 1
            else:
                result.append(right[indexr])
                indexr += 1
        result.extend(left[indexl:])
        result.extend(right[indexr:])
        self.__listweight = result
        return result

    def sorter(self):
        return self.crushing_list(self.__listweight)

    def __getitem__(self, item: int) -> StringWeight:
        if isinstance(item, int):
            return self.__listweight[item]
        else:
            raise TypeError

    def __iter__(self) -> Iterator[StringWeight]:
        return iter(self.__listweight)

    @property
    def list(self) -> list[StringWeight]:
        return self.__listweight



