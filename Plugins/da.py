from Other.tools import BaseFromCommand


class Plugin(BaseFromCommand):
    def __init__(self, text: list[str]):
        self.text = text
        self.word = "Да"

        super().__init__(text, self.word)

    def __call__(self):
        print('Da')

    def __str__(self):
        docs: str = "RJB"
        return docs
