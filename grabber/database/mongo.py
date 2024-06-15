from pymongo import MongoClient


class MongoDBManager:
    """ Класс для управления MongoDB """

    def __init__(self, host: str = 'mongo', port: int = 27017, currencies_db: str = 'currencies',
                 user_db: str = 'users'):
        """
        Инициализация соединения с MongoDB

        :param host: Адрес хоста MongoDB'
        :param port: Порт MongoDB. По умолчанию: 27017
        :param currencies_db: Имя базы данных для бирж
        :param user_db: Имя базы данных для пользователей
        """
        self.client = MongoClient(f'mongodb://{host}:{port}/')
        self.currencies_db = self.client[currencies_db]
        self.binance_collection = self.currencies_db['binance']
        self.bybit_collection = self.currencies_db['bybit']

        # Создаем индексы только при первом запуске
        if not self.binance_collection.index_information().get("timestamp"):
            self.binance_collection.create_index([("timestamp", 1)], expireAfterSeconds=600, name="timestamp")

        if not self.bybit_collection.index_information().get("timestamp"):
            self.bybit_collection.create_index([("timestamp", 1)], expireAfterSeconds=600, name="timestamp")

        self.user_db = self.client[user_db]
        self.user_collection = self.user_db['users']

    def insert_document(self, collection_name: str, document: dict, db_name: str = 'currencies'):
        """
        Вставка документа в коллекцию

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

    def find_documents(self, collection_name: str, projection=None, query=None, db_name: str = 'currencies'):
        """
        Поиск документов в коллекции

        :param collection_name: Имя коллекции
        :param projection: Поля для выборки (по умолчанию: все поля)
        :param query: Критерии поиска (по умолчанию: все документы)
        :param db_name: Имя базы данных
        """
        if projection is None:
            projection = {}
        if query is None:
            query = {}
        if db_name == 'currencies':
            db = self.currencies_db
        else:
            db = self.user_db
        collection = db[collection_name]
        return collection.find(query, projection)

    def find_document(self, collection_name: str, query=None, db_name: str = 'currencies'):
        """
        Поиск одного документа в коллекции

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
        Обновление документа в коллекции

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
