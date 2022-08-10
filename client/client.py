import asyncio
import string
from kivy.app import async_runTouchApp
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

import websockets
from json import dumps, loads
from random import choices

from kivy.uix.label import Label


class MessageBox(Label):
    pass


class MainBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.client_id = "".join(choices(string.digits, k=6))
        self.url = "ws://127.0.0.1:8000/ws/" + self.client_id
        self.data = ''

    def start_websocket(self, instance):
        asyncio.create_task(self.run_websocket(instance))

    def prep_message(self, text):
        return dumps({"id": self.client_id, "message": text})

    async def run_websocket(self, instance):
        async with websockets.connect(self.url) as websocket:
            while True:
                if data := self.data:
                    self.data = ''
                    await websocket.send(self.prep_message(data))
                try:
                    message = loads(await asyncio.wait_for(websocket.recv(), timeout=1 / 60))
                    instance.add_widget(MessageBox(text=message['id']+': '+message['message']))
                except asyncio.exceptions.TimeoutError:
                    continue


if __name__ == "__main__":  # pragma: no cover

    async def run_app(root):
        """Run kivy on the asyncio loop"""
        await async_runTouchApp(root, async_lib="asyncio")
        if root.ws:
            root.ws.cancel()

    asyncio.run(run_app(Builder.load_file('screen.kv')))
