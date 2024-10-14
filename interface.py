from threading import Thread

from allai.Ai import Ai
from chainTextSpeach.Player import Player
# from chainTextSpeach.Player import player
from chainTextSpeach.SpeachText import SpeachText

from tools import getconfig

from loguru import logger
from time import time


class Interfaces(object):
    def __init__(self) -> None:
        self.voice = None
        self.spchText = SpeachText()
        self.ai = Ai()
        self.config = getconfig()

    def start(self):

        while True:
            if self.config["Modes"]["TEXT_OR_VOICE"] == 'TEXT':
                from colorama import Fore
                text = input(Fore.CYAN + ">>> ")
                self.ai.question(text)
            elif self.config["Modes"]["TEXT_OR_VOICE"] == 'VOICE':
                voice = self.spchText.speachtotext()
                print(voice)
                print("VOICE: " + voice)
                response = self.ai.question(voice)
                if response:
                    print("AI: " + response)
                else:
                    continue
            else:
                print(self.config["Modes"]["TEXT_OR_VOICE"])
                raise ValueError("Unexpected value, see config.yaml - ['Modes']['TEXT_OR_VOICE']")


logger.add('applog.log')


def time_log(start_time: float):
    logger.info(f"{'-'*10}| PROGRAM START BEHIND: {round(time() - start_time, 3)}s |{'-'*10}")
    logger.info(f"Startup Configuration: {getconfig()}")
    return


def main():
    if getconfig()['DEBUG']['STATUS'] == 'On':
        start = time()
    spch = SpeachText()
    player = Player()
    for _ in range(0, getconfig()["Theard"]["FromSpeach"]):
        Thread(target=spch.queemq_create).start()

    i = Interfaces()
    if getconfig()['DEBUG']['STATUS'] == 'On':
        time_log(start)
    i.start()


if __name__ == "__main__":
    main()
    # basicConfig(
    #     filename='app.log',
    #     level=DEBUG,
    #     format='%(asctime)s - %(levelname)s - %(message)s'
    # )

    # debug(f'Запущено за:"{time() - s}"')
