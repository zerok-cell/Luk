# from sounddevice import play, stop
# from time import sleep
# import pika


# def player(voice_extract, sample_rate: int, ch, method, properties, body):
#     sample_rate = 24000
#     play(body, sample_rate)
#     sleep(len(body) / sample_rate + 1)
#     stop()


# conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
# channel = conn.channel()
# channel.queue_declare(queue='voice')
# channel.basic_consume(queue='voice',
#                       auto_ack=True,
#                       on_message_callback=player)
# print('21312')
# channel.start_consuming()
