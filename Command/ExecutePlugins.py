from pathlib import Path


class LaunchPlugin:
    @staticmethod
    def import_plug(path: str):
        from importlib import import_module
        plugin = import_module(path)
        return plugin

    def executeplugin(self):
        from ScaningDir import ScanDir
        for plug in ScanDir():
            if plug == "__init__":
                continue
            else:
                plugin = self.import_plug(f'Plugins.{plug}')
                instanceplug = plugin.Plugin(['Да'])
                __wordchk = instanceplug.word_check()
                if __wordchk:
                    instanceplug()

x = LaunchPlugin()
x.executeplugin()
