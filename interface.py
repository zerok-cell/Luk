from Ai import Ai
from speachtotext import SpeachToText
from texttospeach import TextToSpeach


class Interfaces(object):
    def __init__(self) -> None:
        self.spchText = SpeachToText()
        self.txtSpeach = TextToSpeach()
        self.ai = Ai()

    def start(self):
        while True:
            text = self.spchText.speachtotext()
            self.ai.question(text)


i = Interfaces()
i.start()
