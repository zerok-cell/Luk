import importlib


class ObjectPlugin:
    def __init__(self):
        self.plugin = []
        self.imported_plug = []

    def import_plugin(self):
        for one_plugin in self.plugin:
            module_name: str = str(one_plugin).replace("\\", "/").replace("\n", "").split("/")[-1]
            result = importlib.import_module(module_name)
            print(result)
            result.Plugin('проводник').word_check()
            self.imported_plug.append(result)
        print(self.imported_plug)

    def read_path_plug(self):
        with open('../Other/plugin_list.txt', 'r') as file:
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








