from pathlib import Path



import pika

from tools import getconfig

from .Gemini import GeminiAi


class Ai:
    def __init__(self) -> None:
        super().__init__()
        self.config = getconfig()
        self.model = (
            "example"  # Убедитесь, что это строка или другой сериализуемый объект
        )
        
        self.name_bot = "Коди"
        self.pamat = [
            {
                "role": "user",
                "content": f"{self.config['GEMINI']['LLAMA_PROMT']}",
            },
            {
                "role": self.name_bot,
                "content": "Замётано!!",
            },

        ]

        self.all_path = [file for file in Path("../timeslep/").glob("*")]
        self.gemini = GeminiAi(config=self.config)
        print(self.all_path)

    def expectation(self):
        from sounddevice import play
        from soundfile import read
        from random import choice
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
        from time import time
        from functools import lru_cache
        start = time()
        @lru_cache(1)
        def what_mode():
            return self.config["GEMINI"]["MODE"]
        conn, channel = self.queemq_create()
        _mode = what_mode()
        from logging import debug
        
        
        # TODO here config
        if _mode == 'GEMINI':
            _response = self.gemini.gemini_send(text, channel=channel, conn=conn)
            if not _response:
                return False
        elif _mode == 'LOCAL':
            from ollama import chat
            _user_text = {
                "role": "user",
                "content": text,
            },
            # Локальная модель пользователя
            local = chat(
                model=self.model,
                messages=self.pamat,

            )
            self.pamat.append(_user_text)
            _llama_text = {
                "role": "user",
                "content": local['message']['content'],
            },
            # chunk_dot: list[str] = []
            # for_pamat: list[str] = []
        #     red_symbol = ("?", "", ".")
        # # for _word in local:
        #     chunk_dot.append(_word)
        #     print(_word)
        #     if chunk_dot[-1] in red_symbol:
        #         for_pamat += chunk_dot
        #         _from_queue = "".join(chunk_dot)
            channel.basic_publish(exchange='', routing_key='message', body=local['message']['content'])
                # chunk_dot.clear()

            self.pamat.append(_llama_text)
        debug(f"'Время Для прохода Ai.py - {start - time()}'")

        # res_text = "".join(for_pamat)
        # print(res_text)
        # luk_pamat = {"role": "Люк", "content": res_text}
        # self.pamat.append(luk_pamat)
        # print(self.pamat)
