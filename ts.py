import pika
import queue

pik = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
channel = pik.channel()

class n():
    pass

channel.queue_declare(queue='hello')
x = queue.Queue(2)
x.put('2')
channel.basic_publish(exchange='', routing_key='hello', body=)

print('send')

pik.close()
