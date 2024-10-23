import os.path
from functools import lru_cache
from typing import Any

from ScaningDir import ScanDir
from Decorators.Other import timedecorator


class LoadPlugin(ScanDir):
    def __init__(self):
        super().__init__('../Plugins')

    @staticmethod
    def create_path(start: str, end: str) -> str:
        pth = os.path.join(start, end)
        return pth.replace('/', '.')

    @lru_cache(1)
    @timedecorator
    def writepathplug(self) -> Any | None:
        __path_plugins = self.scandir()
        with open('../Other/plugin_list.txt', 'r+') as file:
            if file.read().strip() != '':
                file.close()
            else:
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


LoadPlugin().writepathplug()
