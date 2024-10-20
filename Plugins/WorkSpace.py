from pathlib import Path

from Other.tools import BaseFromCommand
import os


class Plugin(BaseFromCommand):
    def __init__(self, text: list[str]):
        self.text = text
        self.word = "работаем"
        self.pycharm = Path(os.path.join(os.path.expanduser(r'~'), r"AppData\Local\Programs\PyCharm Community\bin"))
        super().__init__(text, self.word)

    def __call__(self):
        print('123123123123')
        from subprocess import run
        run(['explorer'], shell=True)
        run(['start', 'microsoft-edge:'], shell=True)

    def __str__(self):
        docs: str = "RJB"
        return docs



