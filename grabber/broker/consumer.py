import json
import os
import time

import pika
from pika.exceptions import AMQPConnectionError


class Consumer:
    def start_consumer(self):

        queue = 'grabber'
        username = os.getenv('BROKER_USER')
        password = os.getenv('BROKER_PASS')

        # данные для подключения
        credentials = pika.PlainCredentials(username=username, password=password)
        while True:
            try:
                connection = pika.BlockingConnection(
                    pika.ConnectionParameters(host='rabbitmq', port=5672, credentials=credentials)
                )

                channel = connection.channel()
                channel.queue_declare(queue=queue, durable=True)
                channel.basic_consume(queue=queue, on_message_callback=self.callback)

                try:
                    print(f'Подключились к брокеру, очередь: {queue}')
                    channel.start_consuming()
                except KeyboardInterrupt:
                    channel.stop_consuming()
                finally:
                    channel.close()
                    connection.close()

            except AMQPConnectionError as e:
                print(f"Ошибка подключения к RabbitMQ: {e}")
                time.sleep(5)
            except Exception as e:
                print(f'Ошибка брокера: {e}')
                time.sleep(5)

    @staticmethod
    def callback(ch, method, properties, body):
        message = None
        try:
            message = json.loads(body)

            print(f'получили смс в grabber: {message}')

            # подтверждаем получение сообщения
            ch.basic_ack(delivery_tag=method.delivery_tag)

        except json.JSONDecodeError:
            print(f'Не смогли декодировать сообщение: {message}')
        except Exception as e:
            print(e)
