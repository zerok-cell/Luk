from functools import lru_cache
from tools import logging_message
from subprocess import CompletedProcess
from google.api_core.exceptions import FailedPrecondition

from tools import getconfig

from .DataType.ResponseAi import ResponseAi


class GeminiAi(object):
    status = None

    def __init__(self):

        self.responseobj = None
        self.chat_session = None
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
    @staticmethod
    def protest():
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

    @classmethod
    def execute_command(cls, check: list[str]) -> CompletedProcess:
        import subprocess
        if check[0] == 'CMD':
            try:
                cls.status = subprocess.run(check[1:], shell=True)
            except Exception as e:
                print("Most likely, there is no such command or it was entered incorrectly")
                logging_message('critical', f"Incorrect command: {''.join(check)} - {e}")
            return cls.status
        return

    def try_from_request(self, func):
        def wrapper(*args, **kwargs):
            from google.generativeai.types.generation_types import StopCandidateException
            from google.api_core.exceptions import ResourceExhausted
            try:
                try:
                    try:
                        self.res = func(*args, **kwargs)
                    except ResourceExhausted as e:
                        logging_message('waning', e)
                        self._no_quta(args[0])

                except FailedPrecondition as position:
                    logging_message('warning', f"Not correct your possition {position}")
                    self.responseobj.reqstatus = False
                    return self.res

            except StopCandidateException as trp:
                self.protest()
                logging_message('warning', f"Policy error on user text: {text} - {stp}")
                self.res.reqstatus = False
                return self.res
            return self.res
        return wrapper

    @try_from_request
    def request(self, text: str) -> ResponseAi:
        responseobj = ResponseAi()
        self.response = self.chat_session.send_message(text)
        responseobj.all = {'text': self.response.text,
                           "split_text": self.response.text.split(),
                           "token": self.response.usage_metadata.candidates_token_count}
        return responseobj

    def gemini_send(self, text: str) -> ResponseAi:

        _model = self.config_gemin()
        self.chat_session = _model.start_chat(
            history=self.geminiContext)
        self.responseobj = self.request(text)
        check = self.responseobj.splittxt
        self.execute_command(check)
        self.update_memory_gemini(model_text=self.responseobj.text, user_text=text)
        return self.responseobj

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
        logging_message('info', f'UPDATE MEMORY: {self.geminiContext[2:]}')

    @lru_cache(2)
    def config_gemin(self):
        import google.generativeai as genai
        genai.configure(api_key=self.config["GEMINI"]['GEMINI_API_KEY'])
        _model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=self.genconf
        )
        return _model
