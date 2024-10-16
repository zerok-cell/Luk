import asyncio
from functools import lru_cache, wraps
from tools import logging_message
from subprocess import CompletedProcess


from tools import getconfig

from .DataType.ResponseAi import ResponseAi
from .Decorators.GeminiSenDecorators import GeminiSendDecorators


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

    # @GeminiSendDecorators  # TODO доделать декоратор на основе класса
    async def request(self, text: str) -> ResponseAi:
        print('After await')
        responseobj = ResponseAi()

        self.response = await asyncio.create_task(self.chat_session.send_message_async(text))
        print('Berofre await')
        responseobj.all = {'text': self.response.text,
                           "split_text": self.response.text.split(),
                           "token": self.response.usage_metadata.candidates_token_count}
        print(responseobj.text)
        return responseobj

    async def gemini_send(self, text: str) -> ResponseAi:  # TODO перейти на асинхроные запросы
        print('gemini send')
        _model = self.config_gemin()
        self.chat_session = _model.start_chat(
            history=self.geminiContext)
        self.responseobj = await self.request(text)
        print('d')
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
