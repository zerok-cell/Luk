import importlib
import os.path
from pathlib import Path


class ObjectPlugin:
    def __init__(self):
        self.plugin = []
        self.imported_plug = []

    def import_plugin(self): # TODO решить ModuleNotFoundError: No module named 'Plugins.Plugins'
        for __one_plugin in self.plugin:
            print(__one_plugin)
            result = importlib.import_module(f"Plugins.{__one_plugin}")
            obj = getattr(result, "Plugin")
            ww = obj(['проводник'])
            ww.word_check()
            self.imported_plug.append(result)
        print(self.imported_plug)

    def read_path_plug(self):
        with open("../Other/plugin_list.txt", 'r') as file:
            __all_lines = file.readlines()
            if len(__all_lines) == 0:
                from Errors.EmptyFileError import EmptyFileError
                raise EmptyFileError(f'File {file.name} is empty, in {file.name} null lines')
            else:
                for i in __all_lines:
                    self.plugin.append(i)


x = ObjectPlugin()
x.read_path_plug()
x.import_plugin()

print(os.path.abspath('./Other/plugin_list.txt'))







