from pathlib import Path

from Other.tools import BaseFromCommand
import os


class Plugin(BaseFromCommand):
    def __init__(self, text: list[str]):
        self.text = text
        self.word = "проводник"
        self.pycharm = Path(os.path.join(os.path.expanduser(r'~'), r"AppData\Local\Programs\PyCharm Community\bin"))
        super().__init__(text, self.word)

    def __call__(self):
        from subprocess import run
        from fuzzywuzzy import fuzz
        count_explorer = 0
        print(21312312)
        for word in self.text:
            print(fuzz.ratio('проводник', word))
            if fuzz.ratio('проводник', word) > 70:
                count_explorer += 1
        for _ in range(count_explorer):
            run(['explorer'], shell=True)

    def __str__(self):
        docs: str = "Pligin from open explorer"
        return docs

    def d(self):
        print(1231231321213212)



