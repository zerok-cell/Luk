from google.api_core.exceptions import ResourceExhausted
from colorama import Fore
from time import sleep
from functools import lru_cache
import google.generativeai as genai
import subprocess
from google.generativeai.types.generation_types import StopCandidateException
from sounddevice import play
from pathlib import Path
from random import choice
from soundfile import read


class GeminiAi(object):
    def __init__(self, config):
        self.config = config
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

        self.genconf = {
            "temperature": 1,
            "top_p": self.config["GEMINI"]["TOP_P"],
            "top_k": int(self.config["GEMINI"]["TOP_K"]),
            "max_output_tokens": self.config["GEMINI"]["OUTPUT_TOKEN"],  # TODO: configs token
            "response_mime_type": "text/plain",
        }
        self._protest = [file for file in Path("./song_protest/").glob("*")]

        for i in Path("./song_protest/").glob("*"):
            print(i)

    # TODO доделать выбор звуков для ошибки политики генерации текста.
    def protest(self):

        choicewav = choice(self._protest)
        s, f = read(choicewav)
        play(s, 24000, blocking=True)

    def gemini_send(self, text: str, channel, conn):
        _model = self.config_gemin()
        _memory_user = {
            "role": "user",
            "parts": [
                text
            ]
        }
        chat_session = _model.start_chat(
            history=self.geminiContext)
        try:
            try:
                response = chat_session.send_message(text)
            except StopCandidateException as stp:
                print("Запрещеный контнет")
                self.protest()
                return False
            _memory_model = {
                "role": "model",
                "parts": [
                    response.text
                ]
            }
            print(response.text)
            check = response.text.split()
            print(check)
            if check[0] == 'CMD':
                print(check[1:])
                subprocess.run(check[1:], shell=True)
            else:
                channel.basic_publish(exchange='', routing_key='message', body=response.text)
                self.update_memory_gemini(_memory_user, _memory_model)

        except ResourceExhausted as e:
            print("The quota per minute is exhausted, switch to the paid API tariff or wait 1 minute for the quota "
                  "to become 15 requests again")
            print(Fore.RED + "Request send after 1 minute")
            sleep(60)
            self.gemini_send(text=text, channel=channel, conn=conn)
        finally:
            conn.close()

    def update_memory_gemini(self, user: dict[str, list | str],
                             model: dict[str, list | str]):
        self.geminiContext.append(user)
        self.geminiContext.append(model)

    @lru_cache(2)
    def config_gemin(self):
        genai.configure(api_key=self.config["GEMINI"]['GEMINI_API_KEY'])
        _model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=self.genconf
        )
        return _model
