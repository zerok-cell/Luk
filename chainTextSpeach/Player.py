from time import sleep

import pika
from pydub import AudioSegment
from pydub.playback import play
from sounddevice import play, stop
from numpy import array
from tools import getconfig


class Player(object):
    def __init__(self):
        self.host = 'localhost'
        self.name_queue = 'voice'
        self.config = getconfig()['Modes']['AI_OR_SINTES']

    def player(self, ch, method, properties, sound):
        if self.config == 'YA':
            print(sound)
            ar = array(sound)
            print(ar)
            x = AudioSegment(sound)
            play(x)
        else:
            print('dawdwa')
            sample_rate = 24000
            play(sound, sample_rate)
            sleep(len(sound) / sample_rate + 1)
            stop()
        self.queue_consuming()

    def queue_consuming(self):
        conn = pika.BlockingConnection(pika.ConnectionParameters(self.host))
        channel = conn.channel()
        channel.queue_declare(queue=self.name_queue)
        channel.basic_consume(queue=self.name_queue,
                              auto_ack=True,
                              on_message_callback=self.player)
        channel.start_consuming()
