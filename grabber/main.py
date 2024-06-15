import asyncio

from process import run_websocket


async def main():
    await run_websocket()

if __name__ == "__main__":
    asyncio.run(main())
