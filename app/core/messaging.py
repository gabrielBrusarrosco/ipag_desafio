import pika 
import json

class RabbitMQPublisher:
    def __init__(self, host: str = 'rabbitmq'):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
        self.channel = self.connection.channel()
        self.queue_name = 'order_status_updates'
        self.channel.queue_declare(queue=self.queue_name, durable=True)
    def publish(self, message: dict):
        self.channel.basic_publish(
            exchange='',
            routing_key=self.queue_name,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2
            )
        ) 
    def close(self):
        self.connection.close() 
