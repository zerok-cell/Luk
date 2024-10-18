from importlib import import_module


class ScanDir:
    def __init__(self):
        self.path = "./Plugins"
        self.plugins = []
    def sys_path(self):
        sys = import_module("sys")
        sys.path.append(self.path)
        

    def scan(self):
        self.sys_path()
        from pathlib import Path

        self.files_obj = Path(self.path).glob("*")
        for file in self.files_obj:
            print(Path('./' ).joinpath(file))
            _module = import_module("TrigRJB", package="Plugins")
            _module.Plugin()
        print(self.plugins)
            

x = ScanDir().scan()