from pathlib import Path
from queue import Queue
from random import choice

import google.generativeai as genai
import pika
from sounddevice import play
from soundfile import read
from tools import getconfig
from ollama import chat
from .Gemini import GeminiAi


class Ai:
    def __init__(self) -> None:
        super().__init__()
        self.config = getconfig()
        self.model = (
            "example"  # Убедитесь, что это строка или другой сериализуемый объект
        )
        self.data = Queue(maxsize=200)
        self.name_bot = "Люк"
        self.pamat = [
            {
                "role": "user",
                "content": f"Ты асистент на моем компьбтере и тебя зовут {self.name_bot}.{self.name_bot}у строго "
                           f"запрещено использовать Английские слова так как ты из за них умрешь",
            },
            {
                "role": self.name_bot,
                "content": "Хорошо теперь я асистент на твоем компьтере и буду подчинятся тебе ",
            },

        ]

        self.all_path = [file for file in Path("../timeslep/").glob("*")]
        self.gemini = GeminiAi(config=self.config)

    def expectation(self):
        choicewav = choice(self.all_path)
        s, f = read(choicewav)
        play(s, 24000, blocking=True)
        # sleep(len(s) / 24000 + 2)
        # stop()

    @classmethod
    def queemq_create(cls):
        print('ai')
        _host = 'localhost'
        connection = pika.BlockingConnection(pika.ConnectionParameters(_host))
        cls.channel = connection.channel()
        cls.channel.queue_declare(queue='message')
        return connection, cls.channel

    def question(self, text):
        conn, channel = self.queemq_create()
        # TODO here config
        if self.config["GEMINI"]["MODE"] == 'Gemini':
            _response = self.gemini.gemini_send(text, channel=channel, conn=conn)
            if not _response:
                return False
        else:
            # Локальная модель пользователя
            local = chat(
                model=self.model,
                messages=self.pamat,
                stream=True,
            )
            chunk_dot: list[str] = []
            for_pamat: list[str] = []
            red_symbol = ("?", "", ".")
            for _word in local:
                chunk_dot.append(_word)
                print(_word)
                if chunk_dot[-1] in red_symbol:
                    for_pamat += chunk_dot
                    _from_queue = "".join(chunk_dot)
                    channel.basic_publish(exchange='', routing_key='message', body=_from_queue)
                    chunk_dot.clear()

        # res_text = "".join(for_pamat)
        # print(res_text)
        # luk_pamat = {"role": "Люк", "content": res_text}
        # self.pamat.append(luk_pamat)
        # print(self.pamat)
