from threading import Thread

from colorama import Fore
from allai.Ai import Ai
from chainTextSpeach.Player import Player
# from chainTextSpeach.Player import player
from chainTextSpeach.SpeachText import SpeachText

from tools import getconfig
from logging import basicConfig, DEBUG, debug
from time import time

s = time()
class Interfaces(object):
    def __init__(self) -> None:
        self.voice = None
        self.spchText = SpeachText()
        self.ai = Ai()
        self.config = getconfig()

    def start(self):

        while True:
            if self.config["Modes"]["TEXT_OR_VOICE"] == 'TEXT':
                text = input(Fore.CYAN + ">>> ")
                self.ai.question(text)
            elif self.config["Modes"]["TEXT_OR_VOICE"] == 'VOICE':
                voice = self.spchText.speachtotext()
                if not isinstance(voice, bool):
                    if voice.strip() != '':
                        print("VOICE: "+voice)
                        response = self.ai.question(voice)
                        if not response:
                            print("AI: "+response)
                            continue
                    else:
                        voice = self.spchText.speachtotext()

            else:
                print(self.config["Modes"]["TEXT_OR_VOICE"])
                raise ValueError("Unexpected value, see config.yaml - ['Modes']['TEXT_OR_VOICE']")


if __name__ == "__main__":
    spch = SpeachText()
    player = Player()
    conf = getconfig()
    for _ in range(0, conf["Theard"]["FromSpeach"]):
        Thread(target=spch.queemq_create).start()
    # if conf["Modes"]["AI_OR_SINTES"] != 'YA':
    #     playertheard = Thread(target=player.queue_consuming).start()

    i = Interfaces()
    basicConfig(
    filename='app.log',
    level=DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

    debug(f'Запущено за:"{time()-s}"')

    i.start()