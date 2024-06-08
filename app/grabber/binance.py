import asyncio
import websockets
import json

from datetime import datetime

from app.telegram.loader import mongo


async def on_message(message):
    data = json.loads(message)
    res_data = data.get('data', [])

    for i in res_data:
        if isinstance(i, dict):
            ticker = i.get('s')
            price = i.get('c')

            mongo.insert_document(
                collection_name='binance',
                document={
                    'ticker': ticker,
                    'price': price,
                    'timestamp': datetime.utcnow()
                })


async def run_websocket():
    async with websockets.connect("wss://fstream.binance.com/stream") as websocket:
        await websocket.send(
            json.dumps({"method": "SUBSCRIBE", "params": ['!miniTicker@arr'], "id": 1}))
        print("Соединение установлено")
        while True:
            try:
                message = await websocket.recv()
                await on_message(message)
            except websockets.exceptions.ConnectionClosed:
                print("Соединение закрыто. Прерываем цикл")
                break


async def main():
    await run_websocket()


if __name__ == "__main__":
    asyncio.run(main())
