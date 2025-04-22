import discord
from discord.message import Message
import os


class Client(discord.Client):
    def __init__(self, *, intents, **options):
        self.ch = None
        super().__init__(intents=intents, **options)

    async def on_message(self, message: Message):
        print(message)
        if message.author == self.user:
            return

        if message.channel.id != int(os.getenv("OBSERVE_CH_ID")):
            return

        await self.log_send("Message Recieved!")

    async def on_ready(self):
        self.ch = self.get_channel(int(os.getenv("LOG_CH_ID")))
        print(self.ch)
        await self.log_send("Ready!")

    async def on_schedled_event_create(self, event):
        await self.log_send("Create Event!")

    async def on_schedled_event_update(self, before, after):
        await self.log_send("Update Event!")

    async def on_schedled_event_delete(self, event):
        await self.log_send("Delete Event!")

    async def log_send(self, message):
        await self.ch.send(message)
        print(message)
