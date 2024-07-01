import time
import ujson

from collections import defaultdict
from datetime import datetime, timedelta

from broker import send_message_to_queue
from database import mongo_client


class Monitor:

    def run(self) -> None:
        """ Мониторинг """

        while True:
            for user in mongo_client.find_documents(collection_name='profile', db_name='users'):
                chat_id = user.get('chat_id')
                long_percent = user.get('long_percent')
                long_time = user.get('long_time')
                short_percent = user.get('short_percent')
                short_time = user.get('short_time')
                end_time = datetime.now()

                if long_percent and long_time:
                    start_time = datetime.now() - timedelta(minutes=long_time)
                    self._process_price_change(chat_id, start_time, end_time, long_percent, 'Лонг')
                if short_percent and short_time:
                    start_time = datetime.now() - timedelta(minutes=short_time)
                    self._process_price_change(chat_id, start_time, end_time, short_percent, 'Шорт')

            time.sleep(10)

    @staticmethod
    def _process_price_change(chat_id: int, start_time: datetime, end_time: datetime, percent_change: int,
                              event_type: str) -> None:
        """ Обработка событий """

        start_time_end = start_time + timedelta(seconds=5)

        # Конец интервала (текущее время - 5 секунд)
        end_time_end = end_time - timedelta(seconds=5)

        #  Запрос данных за начальный интервал
        query_initial = {'timestamp': {'$gte': start_time, '$lte': start_time_end}}
        initial_data = mongo_client.find_documents(collection_name='binance', query=query_initial)

        #  Запрос данных за конечный интервал
        query_final = {'timestamp': {'$gte': end_time_end, '$lte': end_time}}
        final_data = mongo_client.find_documents(collection_name='binance', query=query_final)

        # Сгруппируйте данные по валютам
        initial_data_by_ticker = defaultdict(list)
        final_data_by_ticker = defaultdict(list)

        # Сгруппируйте данные по валютам
        for document in initial_data:
            ticker = document.get('ticker')
            if ticker:
                initial_data_by_ticker[ticker].append(document)

        for document in final_data:
            ticker = document.get('ticker')
            if ticker:
                final_data_by_ticker[ticker].append(document)

        # Проверка изменений для каждой валюты
        for ticker, ticker_data in initial_data_by_ticker.items():
            if len(ticker_data) >= 2 and ticker in final_data_by_ticker:
                init_price = ticker_data[0]['price']
                last_price = final_data_by_ticker[ticker][-1]['price']

                #  Проверка изменения цены
                price_change = (last_price - init_price) / init_price * 100
                if event_type == 'Лонг' and price_change >= percent_change:
                    message = {
                        'event': event_type,
                        'chat_id': chat_id,
                        'ticker': ticker,
                        'init_price': init_price,
                        'last_price': last_price,
                        'change': round(price_change, 2),
                        'url': 'https://www.binance.com/ru/futures/' + ticker.upper()
                    }
                    send_message_to_queue(message=ujson.dumps(message))
                elif event_type == 'Шорт' and price_change <= -percent_change:
                    message = {
                        'event': event_type,
                        'chat_id': chat_id,
                        'ticker': ticker,
                        'init_price': init_price,
                        'last_price': last_price,
                        'change': round(price_change, 2),
                        'url': 'https://www.binance.com/ru/futures/' + ticker.upper()
                    }
                    send_message_to_queue(message=ujson.dumps(message))
