import pika
from threading import Thread

class SenderBroker(Thread):
    def __init__(self, queue_name):
        super().__init__()
        self.queue_name = queue_name

    def connect(self):
        
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='192.168.135.182'))
        self.channel = self.connection.channel()
        
    def run(self,msg):
        self.connect()
        self.channel.basic_publish(
            exchange='', routing_key=self.queue_name, body=msg)

    def send_message(self, msg):
        self.run(msg)


    def stop(self):
        self.join(5)
        self.connection.close()
