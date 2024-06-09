from pymongo import MongoClient


class MongoDBManager:
    """ Класс для управления MongoDB """

    def __init__(self, host: str = 'localhost', port: int = 27017, database_name: str = 'currencies'):
        """
        Инициализация соединения с MongoDB

        :param host: Адрес хоста MongoDB. По умолчанию: 'localhost'
        :param port: Порт MongoDB. По умолчанию: 27017
        :param database_name: Имя базы данных
        """
        self.client = MongoClient(f'mongodb://{host}:{port}/')
        self.db = self.client[database_name]
        self.collection = self.db['binance']

        # Создаем индекс только при первом запуске
        if not self.collection.index_information().get("timestamp"):
            self.collection.create_index([("timestamp", 1)], expireAfterSeconds=600, name="timestamp")

    def insert_document(self, collection_name: str, document: dict):
        """
        Вставка документа в коллекцию

        :param collection_name: Имя коллекции
        :param document: Документ для вставки
        """
        collection = self.db[collection_name]
        return collection.insert_one(document)

    def find_documents(self, collection_name: str, projection=None, query=None):
        """
        Поиск документов в коллекции

        :param collection_name: Имя коллекции
        :param projection: Поля для выборки (по умолчанию: все поля)
        :param query: Критерии поиска (по умолчанию: все документы)
        """
        if projection is None:
            projection = {}
        if query is None:
            query = {}
        collection = self.db[collection_name]
        return collection.find(query, projection)

    def find_document(self, collection_name: str, query=None):
        """
        Поиск одного документа в коллекции

        :param collection_name: Имя коллекции
        :param query: Критерии поиска (по умолчанию: первый документ)
        """
        if query is None:
            query = {}
        collection = self.db[collection_name]
        return collection.find_one(query)

    def update_document(self, collection_name: str, query: dict, update: dict):
        """
        Обновление документа в коллекции

        :param collection_name: Имя коллекции
        :param query: Критерии поиска документа для обновления
        :param update: Обновления для применения
        """
        collection = self.db[collection_name]
        return collection.update_one(query, update)
