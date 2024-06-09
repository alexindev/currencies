from threading import Thread

from broker import Consumer
from database import MongoDBManager


mongo = MongoDBManager()
consumer = Consumer()

Thread(target=consumer.start_consumer).start()
