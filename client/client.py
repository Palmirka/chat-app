import asyncio
import string
from kivy.app import async_runTouchApp
from kivy.uix.boxlayout import BoxLayout

import websockets
from json import dumps
from random import choices

client_id = "".join(choices(string.digits, k=6))
url = "ws://127.0.0.1:8000/ws/" + client_id


async def hello():
    async with websockets.connect(url) as websocket:
        data = dumps({"id": client_id,
                      "message": "hi!"})
        print(data)
        await websocket.send(data)
        while True:
            print(await websocket.recv())


if __name__ == "__main__":  # pragma: no cover

    async def run_app(root):
        """Run kivy on the asyncio loop"""
        await async_runTouchApp(root, async_lib="asyncio")
        if root.ws:
            root.ws.cancel()

    asyncio.run(run_app(Screen))


asyncio.run(hello())
