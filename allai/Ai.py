from pathlib import Path

from tools import getconfig
from .DataType.PikaType import PikaType

from .Gemini import GeminiAi
from .Local import LocalModel


class Ai:
    def __init__(self) -> None:
        super().__init__()
        self.gemini = None
        self.local = None
        self.config = getconfig()
        self.pika = PikaType()
        self.all_path = [file for file in Path("../timeslep/").glob("*")]

        if self.config["GEMINI"]["MODE"] == 'GEMINI':
            self.gemini = GeminiAi()
        else:
            self.local = LocalModel()

    def expectation(self):
        from sounddevice import play
        from soundfile import read
        from random import choice
        choicewav = choice(self.all_path)
        s, f = read(choicewav)
        play(s, 24000, blocking=True)
        # sleep(len(s) / 24000 + 2)
        # stop()

    # @classmethod
    # def queemq_create(cls):
    #     print('ai')
    #     _host = 'localhost'
    #     connection = BlockingConnection(ConnectionParameters(_host))
    #     cls.channel = connection.channel()
    #     cls.channel.queue_declare(queue='message')
    #     return connection, cls.channel

    @staticmethod
    def logging_function(func):
        def wrapper(*args, **kwargs):
            from time import time
            from loguru import logger
            if getconfig()['DEBUG']['STATUS'] == 'On':
                start = time()
                res = func(*args, **kwargs)
                logger.info(f"AI answered for: {round(time() - start, 3)}s"
                            f" | TOKENS = {res.token}"
                            f" | TEXT = {res.text}")
                return res
            else:
                return func
        return wrapper

    @logging_function
    def question(self, text):
        _mode = self.config["GEMINI"]["MODE"]

        if _mode == 'GEMINI':
            _response = self.gemini.gemini_send(text)
            self.pika.send(_response.text)
            return _response

        elif _mode == 'LOCAL':
            _local = self.local.localmodel(text=text)
            self.pika.send(_local)
