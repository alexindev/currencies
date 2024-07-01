from threading import Thread

from broker import Consumer
from process.monitor import Monitor

consumer = Consumer()
monitor = Monitor()

Thread(target=consumer.start_consumer).start()
Thread(target=monitor.run).start()
