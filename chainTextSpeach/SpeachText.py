import io
from json import load

import pika
import pyttsx3
import sounddevice
import torch
from torch.package import PackageImporter


class SpeachText(object):
    def __init__(self, ):
        self.channel = None
        self._sample_rate = 24000
        self.local_file = "./voiceModel/v4_ru.pt"
        self.tts_model = PackageImporter(self.local_file).load_pickle(
            "tts_models", "model"
        )
        self.speaker = "kseniya"

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
            print('111')
            channel.start_consuming()

    def spch(self, ch, method, properties, body: bytes, config: dict):
        print("[X]", body.decode('utf-8'))
        if body.strip():
            # TODO config from voice
            if config["AI_OR_SINTES"] == 'AI':

                print(11111, body)
                exit() if isinstance(body, str) else None

                audio = self.tts_model.apply_tts(
                    text=body.decode('utf-8'), speaker=self.speaker, sample_rate=self._sample_rate
                )
                buffer = io.BytesIO()
                torch.save(audio, buffer)
                audio_bytes = buffer.getvalue()

                sounddevice.play(audio, 24000)  # TODO дороботать плеер
                _host = 'localhost'
                connection = pika.BlockingConnection(pika.ConnectionParameters(_host))
                self.channel = connection.channel()
                self.channel.queue_declare(queue='voice')
                self.channel.basic_publish(exchange='', routing_key='voice', body=audio_bytes)
                self.queemq_create()
                connection.close()
            else:
                engine = pyttsx3.init()
                engine.say(body.decode('utf-8'))
                engine.runAndWait()
