import os.path
from pathlib import Path


class LaunchPlugin:

    def __init__(self):
        self.new_level = None
        self.plg = None
        self.file = None

    @staticmethod
    def import_plug(path: str):
        from importlib import import_module
        plugin = import_module(path)
        return plugin

    def checkdander(self, word):
        end = word[:2]
        start = word[-2:]
        if end and start == "__":
            return True
        return False

    def packagelevel(self, path_pakage: str, text, folder):
        from ScaningDir import ScanDir
        pathplug = Path(path_pakage)
        print(pathplug)
        print(pathplug.stem.split('/')[-1])
        if self.checkdander(pathplug.stem.split('/')[-1]):
            pass
        else:
            __file = ScanDir(path_pakage).scandir()
            for fl in __file:
                if self.checkdander(fl):
                    continue
                else:
                    print(f'Plugins.{folder}.{fl}')
                    plugin = self.import_plug(f'Plugins.{folder}.{fl}')
                    print(text)
                    instanceplug = plugin.Plugin(text)
                    __wordchk = instanceplug.word_check()
                    print(__wordchk)
                    if __wordchk:
                        instanceplug()

    def executeplugin(self, text: list[str]):
        from ScaningDir import ScanDir
        self.plg = "..\\Plugins"
        self.file = ScanDir(self.plg, 'py').scandir()

        for plug in self.file:

            self.new_level = os.path.join(self.plg, plug)
            if os.path.isdir(self.new_level):
                if plug == "__pycache__":
                    continue
                else:
                    self.packagelevel(self.new_level, text, folder=plug)

            elif os.path.isdir(self.new_level):
                if plug == "__init__":
                    continue
                plugin = self.import_plug(f'Plugins.{plug}')
                instanceplug = plugin.Plugin(text)
                __wordchk = instanceplug.word_check()
                if __wordchk:
                    instanceplug()


x = LaunchPlugin()
x.executeplugin(['проводник'])
