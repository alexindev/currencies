import os
import time

import pika
import requests
import ujson

from pika.exceptions import AMQPConnectionError


class Consumer:
    def start_consumer(self):

        queue = 'telegram'
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

            print(f'получили смс в telegram: {message}')
            self.send_user_message(message)

            # подтверждаем получение сообщения
            ch.basic_ack(delivery_tag=method.delivery_tag)

        except ujson.JSONDecodeError:
            print(f'Не смогли декодировать сообщение: {message}')
        except Exception as e:
            print(e)

    @staticmethod
    def send_user_message(message: dict):
        chat_id: int = message.get('chat_id')
        ticker: str = message.get('ticker')
        init_price: float = message.get('init_price')
        last_price: float = message.get('last_price')
        change: float = message.get('change')
        event: str = message.get('event')
        url: str = message.get('url')

        text = (
            f'Событие: {event}\n'
            f'Тикер: {ticker.upper()}\n'
            f'Изменения: {change}%\n'
            f'Начальная цена: {init_price}\n'
            f'Текущая цена: {last_price}\n'
            f'URL: {url}'
        )

        url = f"https://api.telegram.org/bot{os.getenv('TOKEN')}/sendMessage"
        params = {"chat_id": chat_id, "text": text, "parse_mode": "HTML", "disable_web_page_preview": True}
        requests.post(url, json=params)
