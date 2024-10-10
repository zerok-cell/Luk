import threading
from functools import lru_cache

import yaml
from colorama import Fore

from Ai import Ai
# from chainTextSpeach.Player import player
from chainTextSpeach.SpeachText import SpeachText
from speachtotext import SpeachToText


class Interfaces(object):
    def __init__(self) -> None:
        self.spchText = SpeachToText()
        self.ai = Ai()

        self.conf = self.getconfig()

    def start(self):
        print(self.conf)
        while True:
            if self.conf['Modes']['TEXT_OR_VOICE'] == 'TEXT':
                text = input(Fore.CYAN + ">>> ")
                self.ai.question(text, )
            elif self.conf['Modes']['TEXT_OR_VOICE'] == 'VOICE':
                voice = self.spchText.speachtotext()
                self.ai.question(voice, )
            else: 
                raise ValueError("Unexpected value, see config.yaml - ['Modes']['TEXT_OR_VOICE']")

    @lru_cache
    def getconfig(self):
        with open("config.yaml", "r", encoding='utf-8') as file:
            config = yaml.safe_load(file)
            return config


if __name__ == "__main__":
    spch = SpeachText()
    # playertheard = threading.Thread(target=player)
    speach = threading.Thread(target=spch.queemq_create)
    # playertheard.start()
    speach.start()
    i = Interfaces()

    i.start()
