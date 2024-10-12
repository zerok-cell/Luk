
from typing import Any

import pika

from tools import getconfig

from speachtotext import SpeachToText


class SpeachText(SpeachToText):
    def __init__(self, ):
        super().__init__()
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

    def spch(self, ch, method, properties, body: bytes):
        print("[X]", body.decode('utf-8'))
        if body.strip():

            # TODO config from voice
            if self.config['Modes']["AI_OR_SINTES"] == 'AI':
                from torch.package import PackageImporter
                self.tts_model = PackageImporter(self.local_file).load_pickle(
                "tts_models", "model"
                )

                audio = self.tts_model.apply_tts(
                    text=body.decode('utf-8'), speaker=self.speaker, sample_rate=self._sample_rate
                )
                from io import BytesIO
                # Конвертируем ответ нейроки торча в байты
                buffer = BytesIO()
                from torch import save as torch_save
                torch_save(audio, buffer)
                audio_bytes = buffer.getvalue()
                self.send_voice_queue(audio_bytes)
                # Проигрываем
                import sounddevice
                sounddevice.play(audio, 24000)  # TODO дороботать плеер

            elif self.config['Modes']["AI_OR_SINTES"] == 'SI':
                from pyttsx3 import init as pyttsx3_init
                print('dwd')
                engine = pyttsx3_init()
                engine.say(body.decode('utf-8'))
                engine.runAndWait()

            elif self.config['Modes']["AI_OR_SINTES"] == 'YA':
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

