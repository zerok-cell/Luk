import importlib
import os.path
from pathlib import Path


class ObjectPlugin:
    """Provides a Plugin data type for its loading, importing and unloading. Provides an iterator for traversing
    imported plugins"""

    def __init__(self):
        self.pkl_file_path = None
        self.plugin = []
        self.imported_plug = []

    def import_plugin(self) -> None:
        """Function to import a plugin from the self.plugin attribute"""
        for __one_plugin in self.plugin:
            result = importlib.import_module(f"Plugins.{__one_plugin[:-1]}")
            obj = getattr(result, "Plugin")(['проводник'])
            obj.word_check()
            self.imported_plug.append(result)

    def read_path_plug(self) -> None:
        """Reads the recorded paths (cached) from the Other/plugins_list.txt file and then adds them to the list
        self.plugin"""
        with open("../Other/plugin_list.txt", 'r') as file:
            __all_lines = file.readlines()
            if len(__all_lines) == 0:
                from Errors.EmptyFileError import EmptyFileError
                raise EmptyFileError(f'File {file.name} is empty, in {file.name} null lines')
            else:
                for _ in __all_lines:
                    self.plugin.append(_)

    def unload(self):
        """Unloads plugins from the self.import_plugin attribute"""
        if len(self.import_plugin()) != 0:
            for _ in self.import_plugin():
                del _

    def __iter__(self):
        return iter(self.imported_plug)

    def __next__(self):
        return next(self.imported_plug)

    def __len__(self):
        return len(self.imported_plug)


x = ObjectPlugin()
x.read_path_plug()
x.import_plugin()
