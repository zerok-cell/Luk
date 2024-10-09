import pika 

conn = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = conn.channel()
channel.queue_declare(queue='message')


def callback(ch, method, properties, body):
    print(f" [x] Received {body}")


channel.basic_consume(queue='message',
                      auto_ack=True,
                      on_message_callback=play)

channel.start_consuming()
