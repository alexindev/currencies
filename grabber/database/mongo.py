from pymongo import MongoClient


class MongoDBManager:
    """ Менеджер MongoDB """

    _instance = None

    def __new__(cls, *args, **kwargs):
        """" Singleton """
        if cls._instance is None:
            cls._instance = super(MongoDBManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, host: str = 'mongo', currencies_db: str = 'currencies', user_db: str = 'users'):
        """
        Инициализация соединения с MongoDB

        :param host: Адрес хоста MongoDB'
        :param currencies_db: Имя базы данных для бирж
        :param user_db: Имя базы данных для пользователей
        """
        self.client = MongoClient(f'mongodb://{host}:27017/')

        self.currencies_db = self.client[currencies_db]
        self.binance_collection = self.currencies_db['binance']
        self.bybit_collection = self.currencies_db['bybit']

        self.user_db = self.client[user_db]
        self.user_collection = self.user_db['profile']

        # Создаем индексы только при первом запуске
        if not self.binance_collection.index_information().get("timestamp"):
            self.binance_collection.create_index([("timestamp", 1)], expireAfterSeconds=600, name="timestamp")

        if not self.bybit_collection.index_information().get("timestamp"):
            self.bybit_collection.create_index([("timestamp", 1)], expireAfterSeconds=600, name="timestamp")

    def insert_document(self, document: dict, collection_name: str, db_name: str = 'currencies'):
        """
        Вставка документа

        :param collection_name: Имя коллекции
        :param document: Документ для вставки
        :param db_name: Имя базы данных
        """
        if db_name == 'currencies':
            db = self.currencies_db
        else:
            db = self.user_db
        collection = db[collection_name]
        return collection.insert_one(document)

    def find_documents(self, collection_name: str, db_name: str = 'currencies', query=None):
        """
        Поиск документов

        :param collection_name: Имя коллекции
        :param db_name: Имя базы данных
        :param query: Критерии поиска (по умолчанию: все документы)
        """
        if query is None:
            query = {}
        if db_name == 'currencies':
            db = self.currencies_db
        else:
            db = self.user_db
        collection = db[collection_name]
        return collection.find(query)

    def find_document(self, collection_name: str, query=None, db_name: str = 'currencies'):
        """
        Поиск одного документа

        :param collection_name: Имя коллекции
        :param query: Критерии поиска (по умолчанию: первый документ)
        :param db_name: Имя базы данных
        """
        if query is None:
            query = {}
        if db_name == 'currencies':
            db = self.currencies_db
        else:
            db = self.user_db
        collection = db[collection_name]
        return collection.find_one(query)

    def update_document(self, collection_name: str, query: dict, update: dict, db_name: str = 'currencies'):
        """
        Обновление документа

        :param collection_name: Имя коллекции
        :param query: Критерии поиска документа для обновления
        :param update: Обновления для применения
        :param db_name: Имя базы данных
        """
        if db_name == 'currencies':
            db = self.currencies_db
        else:
            db = self.user_db
        collection = db[collection_name]
        return collection.update_one(query, update)

    def delete_document(self, query: dict, collection_name: str, db_name: str = 'currencies'):
        """
        Удаление документа

        :param query: Критерии для удаления
        :param db_name: Имя базы данных
        :param collection_name: Имя коллекции
        """
        if db_name == 'currencies':
            db = self.currencies_db
        else:
            db = self.user_db
        collection = db[collection_name]
        return collection.delete_one(query)

    def set_user_settings(self, chat_id: int, document: dict):
        """ Добавить настройки пользователя """
        self.user_collection.update_one(
            {'chat_id': chat_id},
            {'$set': document},
            upsert=True
        )


mongo_client = MongoDBManager()
