import asyncio
from typing import Any

import pika

from Other.tools import getconfig

from .SpeechToText import SpeachToText
from loguru import logger


class SpeachText(SpeachToText):
    def __init__(self, ):
        super().__init__()
        self.audio = None
        self.tts_model = None
        self.channel = None
        self._sample_rate = 24000
        self.local_file = "./voiceModel/v4_ru.pt"

        self.speaker = "kseniya"
        self.config = getconfig()

    def __str__(self) -> str:
        return """Class from speach text.
    Arguments:
        chunk:str
    """

    def queemq_create(self):
        while True:
            conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
            channel = conn.channel()
            channel.queue_declare(queue='message')

            channel.basic_consume(queue='message',
                                  auto_ack=True,
                                  on_message_callback=self.spch,
                                  )
            print('111в')
            channel.start_consuming()

    def send_voice_queue(self, sendobj: Any):
        _host = 'localhost'
        connection = pika.BlockingConnection(pika.ConnectionParameters(_host))
        self.channel = connection.channel()
        self.channel.queue_declare(queue='voice')
        self.channel.basic_publish(exchange='', routing_key='voice', body=sendobj)
        connection.close()

    def sintesvoice(self, body: str):  # TODO решить ошибку когда синтез работает через раз
        from pyttsx3 import init as pyttsx3_init
        if isinstance(body, str):
            engine = pyttsx3_init()
            engine.say(body)
            engine.runAndWait()
        else:
            try:
                raise TypeError(f"Неверный тип ожидалсь 'str' передано '{type(body)}'")
            except TypeError as tp:
                logger.critical(f'Invalid data type TRACE: {tp}')

    # @staticmethod
    # def silerosendplayer(audio):
    #     from io import BytesIO
    #     # Конвертируем ответ нейроки торча в байты
    #     buffer = BytesIO()
    #     from torch import save as torch_save
    #     torch_save(audio, buffer)
    #     audio_bytes = buffer.getvalue()
    #     # send_voice_queue(audio_bytes)

    def aisilero(self, body: bytes):
        from torch.package import PackageImporter
        try:
            self.tts_model = PackageImporter(self.local_file).load_pickle(
                "tts_models", "model"
            )
        except ImportError as imper:
            logger.critical(
                f"Failed to import model f'{self.local_file}', the path may be incorrect or the model may be incorrect."
                f"Check the path and try again.{imper}")
            print('Model import error see logs')
            return
        try:
            if isinstance(body, bytes):
                self.audio = self.tts_model.apply_tts(
                    text=body.decode('utf-8'), speaker=self.speaker, sample_rate=self._sample_rate
                )
            else:
                raise TypeError(f'the data type was expected "str" , was transmitted "{type(body)}"')
        except TypeError as tp:
            logger.critical(f"Invalid data type TRACE: {tp}")
        from sounddevice import play  # Проигрываем
        try:
            if not isinstance(self.audio, None):
                play(self.audio, 24000)
            raise TypeError(f'the data type was expected "str", was transmitted "{type(body)}.Soundevice not supported '
                            f'transmitted type')
        except TypeError as trp:
            logger.critical(trp)

    def spch(self, ch, method, properties, body: bytes):
        __decode_data = body.decode('utf-8')
        if body.strip():

            # TODO config from voice
            if self.config['Modes']["AI_OR_SINTES"] == 'AI':
                self.aisilero(body)

            elif self.config['Modes']["AI_OR_SINTES"] == 'SI':
                print('SIN')
                from queue import Queue
                data = Queue(5)
                data.put(__decode_data)
                self.sintesvoice(data.get())
                self.queemq_create()
            elif self.config['Modes']["AI_OR_SINTES"] == 'YA':

                print('22das')
                from speechkit import model_repository, configure_credentials, creds
                configure_credentials(
                    yandex_credentials=creds.YandexCredentials(
                        api_key=self.config['Yandex']['KEY']
                    )
                )
                print('dawda')
                model = model_repository.synthesis_model()
                model.voice = 'anton'
                model.role = 'good'
                result = model.synthesize(body.decode('utf-8'), )
                from pydub.playback import play
                play(result)

                return
            else:
                pass
