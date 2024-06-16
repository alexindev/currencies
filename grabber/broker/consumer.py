import os
import time

import ujson
import pika

from pika.exceptions import AMQPConnectionError

from database import mongo_client


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

    def callback(self, ch, method, properties, body):
        message = None
        try:
            message = ujson.loads(body)

            print(f'получили смс в grabber: {message}')
            func = message.get('func')

            match func:
                case 'start':
                    self.add_user_settings(message)
                case 'stop':
                    self.delete_user(message)
                case _:
                    print('Функция не опознана')

            # подтверждаем получение сообщения
            ch.basic_ack(delivery_tag=method.delivery_tag)

        except ujson.JSONDecodeError:
            print(f'Не смогли декодировать сообщение: {message}')
        except Exception as e:
            print(e)

    @staticmethod
    def add_user_settings(message: dict):
        """ Пользователь добавил настройки """
        chat_id = message.get('chat_id')
        long_percent = message.get('long_percent')
        long_time = message.get('long_time')
        short_percent = message.get('short_percent')
        short_time = message.get('short_time')

        document = {
            'chat_id': chat_id,
            'long_percent': long_percent,
            'long_time': long_time,
            'short_percent': short_percent,
            'short_time': short_time
        }
        mongo_client.set_user_settings(chat_id=chat_id, document=document)

    @staticmethod
    def delete_user(message: dict):
        """ Удалить настройки пользователя """
        query = {'chat_id': message.get('chat_id')}
        mongo_client.delete_document(query=query, collection_name='profile', db_name='users')
