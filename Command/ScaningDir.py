from importlib import import_module
from pathlib import Path


class ScanDir:
    def __init__(self):
        self.files_obj = None
        self.path = "../Plugins"
        self.path_plug: str = None

    def sys_path(self):
        sys = import_module("sys")
        sys.path.append(self.path)

    def __iter__(self):
        return self

    def __next__(self):
        if self.path_plug is None:
            self.sys_path()
            self.files_obj = Path(self.path).glob("*.py")

        try:
            self.path_plug = next(self.files_obj).stem
            return str(self.path_plug)
        except StopIteration:
            raise StopIteration()


