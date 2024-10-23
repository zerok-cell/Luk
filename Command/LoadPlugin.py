

from typing import Any

from .ScaningDir import ScanDir
from Decorators.Other import timedecorator


class LoadPlugin(ScanDir):
    def __init__(self):
        self.path_list = '../Other/plugin_list.txt'
        super().__init__('../Plugins')

    @staticmethod
    def create_path(start: str, end: str) -> str:
        from os.path import join
        pth = join(start, end)
        return pth.replace('/', '.')

    @timedecorator
    def writepathplug(self) -> Any | None:
        __path_plugins = self.scandir()
        with open(self.path_list, 'r+') as file:
            from Other.tools import checkdander
            for path in __path_plugins:
                if checkdander(path):
                    continue
                else:
                    file.write(f'{path}\n')
                    from Other.tools import logging_message
                    logging_message('info', f'Plugin {path} write')
            file.close()
        from Other.tools import logging_message
        logging_message('info', 'A registry of plugin paths has been created see')

    def rewrite(self):
        with open(self.path_list, 'r+') as file:
            file.seek(0)
            file.truncate()
            self.writepathplug()
            return




