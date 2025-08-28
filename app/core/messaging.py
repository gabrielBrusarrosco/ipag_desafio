import pika 
import json
from .config import settings

class RabbitMQPublisher:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.RABBITMQ_HOST))
        self.channel = self.connection.channel()
        dlq_name = 'order_status_updates_dlq'
        self.channel.queue_declare(queue=dlq_name, durable=True)
        self.queue_name = 'order_status_updates'
        queue_args = {
            "x-dead-letter-exchange": "",
            "x-dead-letter-routing-key": dlq_name
        }
        self.channel.queue_declare(queue=self.queue_name, durable=True, arguments=queue_args)
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
