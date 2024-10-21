import pathlib
from functools import lru_cache
from importlib import import_module


class ScanDir:
    def __init__(self, target: str = None, type_file: str = None):
        self.__result_scan = None
        self.__path = target
        self.__files_obj = iter(
            [file for file in pathlib.Path(target).glob(f'*')])
        self.__path_plug: str = None

    def sys_path(self):
        sys = import_module("sys")
        sys.path.append(self.__path)

    def __iter__(self):
        return self

    def __next__(self) -> str:
        if self.__path_plug is None:
            self.sys_path()

        try:
            self.__path_plug = next(self.__files_obj)
            return str(self.__path_plug)
        except StopIteration:
            raise StopIteration()

    @lru_cache
    def scandir(self) -> list[str]:
        self.__result_scan: list[pathlib.WindowsPath] = []
        for file in self.__files_obj:
            self.__result_scan.append(file.stem)
        return self.__result_scan
