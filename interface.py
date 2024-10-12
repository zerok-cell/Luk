import threading


from colorama import Fore

from allai.Ai import Ai
from chainTextSpeach.Player import Player
# from chainTextSpeach.Player import player
from chainTextSpeach.SpeachText import SpeachText
from chainTextSpeach.SpeachText import SpeachText
from tools import getconfig


class Interfaces(object):
    def __init__(self) -> None:
        self.voice = None
        self.spchText = SpeachText()
        self.ai = Ai()
        self.config = getconfig()["Modes"]

    def start(self):

        while True:
            if self.config['TEXT_OR_VOICE'] == 'TEXT':
                text = input(Fore.CYAN + ">>> ")
                self.ai.question(text, )
            elif self.config['TEXT_OR_VOICE'] == 'VOICE':
                voice = self.spchText.speachtotext()
                if not isinstance(voice, bool):
                    if voice.strip() != '':
                        response = self.ai.question(voice)
                        if not response:
                            continue
                    else:
                        voice = self.spchText.speachtotext()

            else:
                raise ValueError("Unexpected value, see config.yaml - ['Modes']['TEXT_OR_VOICE']")


if __name__ == "__main__":
    spch = SpeachText()
    player = Player()
    conf = getconfig()
    for _ in range(0, conf["Theard"]["FromSpeach"]):
        threading.Thread(target=spch.queemq_create).start()
    if conf['Modes']['AI_OR_SINTES'] != 'YA':
        playertheard = threading.Thread(target=player.queue_consuming).start()

    i = Interfaces()

    i.start()
