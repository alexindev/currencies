import ujson
import websockets

from datetime import datetime

from database import mongo_client


async def on_message(message):
    data = ujson.loads(message)
    res_data = data.get('data', [])
    for i in res_data:
        if isinstance(i, dict):
            ticker = i.get('s')
            price = i.get('c')
            mongo_client.insert_document(
                collection_name='binance',
                document={
                    'ticker': ticker,
                    'price': float(price),
                    'timestamp': datetime.now()
                })


async def run_websocket():
    async with websockets.connect("wss://fstream.binance.com/stream") as websocket:
        await websocket.send(
            ujson.dumps({"method": "SUBSCRIBE", "params": ['!miniTicker@arr'], "id": 1}))
        print("Websocket соединение установлено")
        while True:
            try:
                message = await websocket.recv()
                await on_message(message)
            except websockets.exceptions.ConnectionClosed:
                print("Соединение закрыто. Прерываем цикл")
                break
