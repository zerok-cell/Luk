import time
from functools import lru_cache
from random import randint

from StringWeight import StringWeight


class MassiveWeight(object):
    def __init__(self, *args: str):
        self.data_input = args
        self.listweight: list[StringWeight] = []

    def genlist(self):
        for string in self.data_input:
            if isinstance(string[0], str) and (isinstance(string[1], float)):
                __string_weight = StringWeight(string[0], string[1])
                self.listweight.append(__string_weight)
        return self.listweight

    def crushing_list(self, for_recursion: list = None) -> list:
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
        self.listweight = result
        return result

    def sorter(self):
        self.crushing_list(self.listweight)

    def __str__(self):
        return f"{self.listweight}"


x = MassiveWeight(('привет', 9.0), ("Пока", 2.0))
x.genlist()
x.sorter()


