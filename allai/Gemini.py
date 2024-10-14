from functools import lru_cache
from subprocess import CompletedProcess

from google.generativeai.types import GenerateContentResponse

from tools import getconfig
from loguru import logger
from .DataType.ResponseAi import ResponseAi


class GeminiAi(object):
    def __init__(self):

        self.response = None
        self.config = getconfig()
        self.geminiContext: list[dict[str, list[str]]] = [
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

    # TODO доделать выбор звуков для ошибки политики генерации текста.
    def protest(self):
        from soundfile import read
        from sounddevice import play
        from pathlib import Path
        from random import choice
        _protest = [file for file in Path(r"C:\Works\Luk\allai\song_protest").glob("*")]
        choicewav = choice(_protest)
        s, f = read(choicewav)
        play(s, 24000, blocking=True)

    def _no_quta(self, text: str) -> ResponseAi:
        from time import sleep
        from colorama import Fore
        print("The quota per minute is exhausted, switch to the paid API tariff or wait 1 minute for the quota "
              "to become 15 requests again")
        print(Fore.RED + "Request send after 1 minute")
        sleep(65)
        return self.gemini_send(text=text)

    @staticmethod
    def execute_command(check: list[str]) -> CompletedProcess:
        import subprocess
        try:
            subprocess.run(check[1:], shell=True)
        except Exception as e:
            print("Most likely, there is no such command or it was entered incorrectly")
            logger.critical(f"Incorrect command: {''.join(check)}")

    def gemini_send(self, text: str) -> ResponseAi:
        from google.generativeai.types.generation_types import StopCandidateException
        from google.api_core.exceptions import ResourceExhausted
        _model = self.config_gemin()
        print(text)
        chat_session = _model.start_chat(
            history=self.geminiContext)
        try:
            try:
                self.response = chat_session.send_message(text)
                responseobj = ResponseAi()
                responseobj.all = {'text': self.response.text,
                                   "split_text": self.response.text.split(),
                                   "token": self.response.usage_metadata.candidates_token_count}

            except StopCandidateException as stp:
                print("Запрещеный контнет")
                self.protest()
                logger.warning(f"Policy error on user text: {text}")
                responseobj.reqstatus = False
                return responseobj
            print(responseobj.text)
            check = responseobj.splittxt
            if check[0] == 'CMD':
                self.execute_command(check)
            else:
                print(text)
                self.update_memory_gemini(model_text=responseobj.text, user_text=text)
        except ResourceExhausted as e:
            self._no_quta(text)
        finally:
            return responseobj

    def update_memory_gemini(self, model_text: str, user_text: str):

        user = {
            "role": "user",
            "parts": [
                user_text
            ]
        }
        model = {
            "role": "model",
            "parts": [
                model_text
            ]
        }
        self.geminiContext.append(user)
        self.geminiContext.append(model)
        logger.info(f'UPDATE MEMORY: {self.geminiContext[2:]}')

    @lru_cache(2)
    def config_gemin(self):
        import google.generativeai as genai
        genai.configure(api_key=self.config["GEMINI"]['GEMINI_API_KEY'])
        _model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=self.genconf
        )
        return _model
