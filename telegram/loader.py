import os
from threading import Thread

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from database import Database
from broker.consumer import Consumer

consumer = Consumer()
db = Database()
storage = MemoryStorage()
bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(storage=storage)

Thread(target=consumer.start_consumer).start()
