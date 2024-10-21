
from Other.tools import BaseFromCommand


class Plugin(BaseFromCommand):
    def __init__(self, text: list[str]):

        self.controller = None
        self.text = text
        self.word = "закрой"
        super().__init__(text, self.word)

    def close(self):
        from pynput import keyboard
        self.controller = keyboard.Controller()
        __ctrl = keyboard.Key.ctrl
        __f4 = keyboard.Key.f4

        self.controller.press(__ctrl)
        self.controller.press(__f4)
        self.controller.release(__ctrl)
        self.controller.release(__f4)

    def __call__(self):
        print('Close')
        count_explorer = 0
        from fuzzywuzzy import fuzz

        for word in self.text:
            if fuzz.ratio('закрой', word) > 70:
                count_explorer += 1
        for _ in range(count_explorer):
            self.close()

    def __str__(self):
        docs: str = "Pligin from open explorer"
        return docs
