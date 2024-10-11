import threading
from functools import lru_cache

import yaml
from colorama import Fore

from Ai import Ai
# from chainTextSpeach.Player import player
from chainTextSpeach.SpeachText import SpeachText
from speachtotext import SpeachToText
from tools import getconfig

class Interfaces(object):
    def __init__(self) -> None:
        self.spchText = SpeachToText()
        self.ai = Ai()
        self.config = getconfig()["Modes"]


    def start(self):

        while True:
            if self.config['TEXT_OR_VOICE'] == 'TEXT':
                text = input(Fore.CYAN + ">>> ")
                self.ai.question(text, )
            elif self.config['TEXT_OR_VOICE'] == 'VOICE':
                voice = self.spchText.speachtotext()
                self.ai.question(voice, )
            else: 
                raise ValueError("Unexpected value, see config.yaml - ['Modes']['TEXT_OR_VOICE']")




if __name__ == "__main__":
    spch = SpeachText()
    # playertheard = threading.Thread(target=player)
    speach = threading.Thread(target=spch.queemq_create)
    # playertheard.start()
    speach.start()
    i = Interfaces()

    i.start()
