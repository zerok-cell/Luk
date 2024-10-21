from pathlib import Path


class LaunchPlugin:

    def __init__(self):
        self.file = None

    @staticmethod
    def import_plug(path: str):
        from importlib import import_module
        plugin = import_module(path)
        print(1)
        return plugin

    def executeplugin(self, text: list[str]):
        from .ScaningDir import ScanDir
        self.file = ScanDir('./Plugins', 'py').scandir()
        for plug in self.file:
            if plug == "__init__":
                continue
            else:
                print(f'Plugins.{plug}')
                plugin = self.import_plug(f'Plugins.{plug}')
                instanceplug = plugin.Plugin(text)
                __wordchk = instanceplug.word_check()
                if __wordchk:
                    instanceplug()


# x = LaunchPlugin()
# x.executeplugin('работаем')


