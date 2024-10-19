from Other.tools import BaseFromCommand


class Plugin(BaseFromCommand):
    def __init__(self, text: list[str]):
        self.text = text
        self.word = "Раджаб"

        super().__init__(text, self.word)

    def __call__(self):
        print('Rajab')

    def __str__(self):
        docs: str = "RJB"
        return docs
