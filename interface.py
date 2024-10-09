from Ai import Ai
from speachtotext import SpeachToText
from colorama import Fore
# from chainTextSpeach.Player import player
from chainTextSpeach.SpeachText import SpeachText
import threading
import logging

class Interfaces(object):
    def __init__(self, txt_mode: bool) -> None:
        self.spchText = SpeachToText()
        self.ai = Ai()
        self.text_mode = None or txt_mode

    def start(self):
        while True:
            if self.text_mode:
                text = input(Fore.CYAN + ">>> ")
                self.ai.question(text)
            else:
                voice = self.spchText.speachtotext()
                self.ai.question(voice)


if __name__ == "__main__":
    logging.basicConfig(level=logging.WARNING, filename="py_log.log",filemode="w")
    print(1)
    spch = SpeachText()
    print(1)
    # playertheard = threading.Thread(target=player)
    print(1)
    speach = threading.Thread(target=spch.queemq_create)
    speach2 = threading.Thread(target=spch.queemq_create)
    speach3 = threading.Thread(target=spch.queemq_create)
    print(1)
    # playertheard.start()
    print(1)
    speach.start()
    print(1)
    i = Interfaces(True)

    i.start()


