import pika
import json
import time
import logging
from app.core.database import SessionLocal
from app.repositories.notification_log_repository import NotificationLogRepository

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

MAX_RETRIES = 3

def on_message_callback(ch, method, properties, body):
    logging.info("Mensagem recebida...")
    
    try:
        message_data = json.loads(body)

        required_keys = ['order_id', 'old_status', 'new_status', 'timestamp']
        if not all(key in message_data for key in required_keys):
            logging.error(f"Mensagem malformada, descartando: {message_data}")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return

        # Lógica Principal
        db = SessionLocal()
        try:
            NotificationLogRepository.create_log(db, log_data=message_data)
            logging.info(f"Order {message_data['order_id']} status changed from {message_data['old_status']} to {message_data['new_status']}")
            logging.info(f"Notification sent for order {message_data['order_id']}")

            ch.basic_ack(delivery_tag=method.delivery_tag)

        except Exception as db_error:
            logging.error(f"Erro de banco de dados ao processar mensagem: {db_error}")
            raise db_error
        finally:
            db.close()

    except Exception as e:
        logging.error(f"Erro ao processar mensagem: {e}")
        headers = properties.headers if properties.headers else {}
        retries = headers.get('x-retries', 0)
        
        if retries < MAX_RETRIES:
            logging.warning(f"Tentativa {retries + 1} de {MAX_RETRIES}. Reenfileirando...")
            headers['x-retries'] = retries + 1
            new_properties = pika.BasicProperties(headers=headers, delivery_mode=2)
            ch.basic_publish(exchange='', routing_key='order_status_updates', body=body, properties=new_properties)
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        else:
            logging.error(f"Máximo de {MAX_RETRIES} tentativas atingido. Descartando mensagem.")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

def main():
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
            channel = connection.channel()
            
            queue_name = 'order_status_updates'
            channel.queue_declare(queue=queue_name, durable=True)
            
            channel.basic_qos(prefetch_count=1)
            
            channel.basic_consume(queue=queue_name, on_message_callback=on_message_callback)
            
            print('✅ Worker iniciado. Aguardando por mensagens. Para sair, pressione CTRL+C')
            channel.start_consuming()
        except pika.exceptions.AMQPConnectionError as e:
            print(f"Erro de conexão com o RabbitMQ: {e}. Tentando reconectar em 5 segundos...")
            time.sleep(5)
        except Exception as e:
            print(f"Um erro inesperado ocorreu: {e}")
            break

if __name__ == '__main__':
    main()