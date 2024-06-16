import os

import pika

from pika.exceptions import AMQPConnectionError, AMQPChannelError


def send_message_to_queue(message: str, queue_name: str = 'telegram'):
    """ Отправить сообщение в очередь RabbitMQ """

    username = os.getenv('BROKER_USER')
    password = os.getenv('BROKER_PASS')

    credentials = pika.PlainCredentials(username=username, password=password)
    parameters = pika.ConnectionParameters(host='rabbitmq', port=5672, credentials=credentials)
    try:
        with pika.BlockingConnection(parameters) as connection:
            channel = connection.channel()
            channel.queue_declare(queue=queue_name, durable=True)
            channel.basic_publish(exchange='', routing_key=queue_name, body=message)
            print(f'В очередь {queue_name} отправлено сообщение: {message}')
    except AMQPConnectionError as e:
        print(f"Ошибка подключения к RabbitMQ: {e}")
    except AMQPChannelError as e:
        print(f"Ошибка канала RabbitMQ: {e}")
    except Exception as e:
        print(f"Ошибка при отправке сообщения: {e}")
