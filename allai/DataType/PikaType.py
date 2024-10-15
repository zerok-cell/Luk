class PikaType(object):
    def __init__(self):
        self._host = 'localhost'
        self.connection = None
        self.channel = None
        self.configure()

    def configure(self):
        from pika import BlockingConnection, ConnectionParameters
        self.connection = BlockingConnection(ConnectionParameters(self._host))
        self.channel = self.connection.channel()

        self.channel.queue_declare(queue='message')
        return

    def send(self, value):
        self.channel.basic_publish(exchange='', routing_key='message', body=value)


    def close(self):
        if not self.connection is None:
            self.connection.close()
