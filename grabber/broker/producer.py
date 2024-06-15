import pika

from pika.exceptions import AMQPConnectionError, AMQPChannelError


def send_message_to_queue(queue_name: str, message):
    """ Отправить сообщение в очередь RabbitMQ """
    credentials = pika.PlainCredentials('guest', 'guest')
    parameters = pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials)
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
