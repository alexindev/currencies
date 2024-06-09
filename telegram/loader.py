import os
from threading import Thread

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

from database.sqlite import SqliteDatabase
from broker.consumer import Consumer

load_dotenv()


consumer = Consumer()
db = SqliteDatabase()
storage = MemoryStorage()
bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(storage=storage)

Thread(target=consumer.start_consumer).start()
