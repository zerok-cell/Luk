import io

import sounddevice
import torch
from torch.package import PackageImporter
from torch import TensorType

from time import sleep
from queue import Queue
import pika
from soundfile import read


class SpeachText(object):
    def __init__(self):
        self.channel = None
        self._sample_rate = 24000
        self.local_file = "./voiceModel/v4_ru.pt"
        self.tts_model = PackageImporter(self.local_file).load_pickle(
            "tts_models", "model"
        )
        self.speaker = "aidar"

    def __str__(self) -> str:
        return """Class from speach text.
    Arguments:
        chunk:str
    """

    def queemq_create(self):
        while True:
            print('spchtxt')
            conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
            channel = conn.channel()
            channel.queue_declare(queue='message')

            channel.basic_consume(queue='message',
                                  auto_ack=True,
                                  on_message_callback=self.spch)
            print('111')
            channel.start_consuming()

    def spch(self, ch, method, properties, body: bytes):
        print("[X]", body.decode('utf-8'))
        if body.strip():
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
