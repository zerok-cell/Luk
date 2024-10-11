from pathlib import Path
from queue import Queue
from random import choice

import google.generativeai as genai
import pika
from sounddevice import play
from soundfile import read
from tools import getconfig
from ollama import chat
from google.api_core.exceptions import ResourceExhausted
from time import sleep
from colorama import  Fore

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
        self.genconf = {
            "temperature": 1,
            "top_p": self.config["GEMINI"]["TOP_P"],
            "top_k": int(self.config["GEMINI"]["TOP_K"]),
            "max_output_tokens": self.config["GEMINI"]["OUTPUT_TOKEN"],  # TODO: configs token
            "response_mime_type": "text/plain",
        }

        self.geminiContext = [
            {
                "role": "user",
                "parts": [
                    f"{self.config['GEMINI']['PROMT'] if self.config['GEMINI']['PROMT'] != '' else 'Будь собой'}",
                ],
            },
            {
                "role": "model",
                "parts": [
                    "Хорошо я буду им \n",
                ],
            },
        ]
        self.all_path = [file for file in Path("./timeslep/").glob("*")]

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
            _memory_user = {
                "role": "user",
                "parts": [
                    text
                ]
            }
            print(text)
            # self.expectation()
            data_in_pamat_user = {"role": "user", "content": text}
            self.pamat.append(data_in_pamat_user)
            genai.configure(api_key=self.config["GEMINI"]['GEMINI_API_KEY'])
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
            )

            chat_session = model.start_chat(
                history=self.geminiContext)
            try:
                response = chat_session.send_message(text)
                _memory_model = {
                    "role": "model",
                    "parts": [
                        response.text
                    ]
                }
                print(response.text)
                self.geminiContext.append(_memory_user)
                self.geminiContext.append(_memory_model)
                channel.basic_publish(exchange='', routing_key='message', body=response.text)

            except ResourceExhausted as e:
                print("The quota per minute is exhausted, switch to the paid API tariff or wait 1 minute for the quota "
                      "to become 15 requests again")
                print(Fore.RED + "Request send after 1 minute")
                sleep(60)
                self.question(text=text)
            finally:
                return True

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
        conn.close()

        # res_text = "".join(for_pamat)
        # print(res_text)
        # luk_pamat = {"role": "Люк", "content": res_text}
        # self.pamat.append(luk_pamat)
        # print(self.pamat)
