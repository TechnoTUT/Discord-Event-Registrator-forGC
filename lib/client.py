import discord
from discord.message import Message
from discord.scheduled_event import ScheduledEvent
import os
from lib.GoogleCalendarAPIWrapper import GoogleCalendar

from returns.result import Success, Failure


class Client(discord.Client):
    EMBED_COLOR_INFO = 0x1E90FF
    EMBED_COLOR_SUCC = 0x3CB371
    EMBED_COLOR_WARN = 0xFFD700
    EMBED_COLOR_CRIT = 0xFF6347

    def __init__(self, *, intents, **options):
        self.ch = None
        self.gc = GoogleCalendar()
        super().__init__(intents=intents, **options)

    async def on_message(self, message: Message):
        if message.author == self.user:
            return

        if message.channel.id != int(os.getenv("OBSERVE_CH_ID")):
            return

        await self.log_send("Message Recieved!")

    async def on_ready(self):
        self.ch = self.get_channel(int(os.getenv("LOG_CH_ID")))
        print(self.ch)
        await self.log_send("Ready!")

    async def on_scheduled_event_create(self, event: ScheduledEvent):
        name = event.name
        start = event.start_time
        end = event.end_time
        await self.log_send_embed(
            title="新しいイベントを検知しました！",
            description=f"イベント名: {name}",
            color=Client.EMBED_COLOR_INFO,
            param_dict={"開始時間": start, "終了時間": end},
        )

        match self.gc.createEvent(title=name, start=start, end=end):
            case Success(val):
                await self.log_send_embed(
                    title="Googleカレンダーに登録しました!",
                    description=None,
                    color=Client.EMBED_COLOR_SUCC,
                )
            case Failure(err):
                await self.log_send_embed(
                    title="Googleカレンダーへの登録に失敗しました...",
                    description=err,
                    color=Client.EMBED_COLOR_CRIT,
                )

    async def on_scheduled_event_update(
        self, before: ScheduledEvent, after: ScheduledEvent
    ):
        await self.log_send("Update Event!")

    async def on_scheduled_event_delete(self, event: ScheduledEvent):
        await self.log_send("Delete Event!")

    async def log_send(self, message):
        await self.ch.send(message)
        print(message)

    async def log_send_embed(
        self, title, description, color, param_dict: dict[str, str] = {}
    ):
        embed = discord.Embed(title=title, color=color, description=description)

        for key, value in param_dict.items():
            embed.add_field(name=key, value=value)

        await self.ch.send(embed=embed)
