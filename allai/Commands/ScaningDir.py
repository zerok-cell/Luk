
class ScanDir:
    def __init__(self):
        self.path = "../../../Plugins/"
        self.plugins = []
    
    def scan(self):
        from pathlib import Path
        from importlib import import_module
        self.files_obj = Path(self.path).glob("*")
        for file in self.files_obj:
            print(file)
            self.plugins.append(file)
        print(self.plugins)
            

x = ScanDir().scan()