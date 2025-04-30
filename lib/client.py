import os
import datetime
from pathlib import Path

import discord
from discord.message import Message
from discord.scheduled_event import ScheduledEvent

from returns.result import Success, Failure, Result

from lib.GoogleCalendarAPIWrapper import GoogleCalendar
from lib.util import debugging, Optional_or, event_diff
from lib.datastructure.entry import RegisteredEvents, RegisteredEventEntry
from lib.datastructure.calendarEvent import CalendarEvent


class Client(discord.Client):
    EMBED_COLOR_INFO = 0x1E90FF
    EMBED_COLOR_SUCC = 0x3CB371
    EMBED_COLOR_WARN = 0xFFD700
    EMBED_COLOR_CRIT = 0xFF6347

    def __init__(self, *, intents, unuse_gcapi: bool = True, **options):
        self.ch = None
        self.unuse_gcapi = unuse_gcapi
        self.gc = GoogleCalendar()

        self.event_db_path = os.getenv("EVENT_DB_PATH")

        if self.event_db_path is None:
            raise ValueError("環境変数 EVENT_DB_PATH を読み取れませんでした")

        # イベント登録DB読み出し
        self.event_db = RegisteredEvents(self.event_db_path)

        super().__init__(intents=intents, **options)

    async def register_event_db(self, event: ScheduledEvent):
        """イベントをDBに登録します。

        Args:
            event (ScheduledEvent): 登録する ScheduledEvent オブジェクト。
        """
        name = event.name
        start = event.start_time
        end = Optional_or(event.end_time, default=start + datetime.timedelta(hours=1))
        location = Optional_or(event.location, "不明")
        description = Optional_or(event.description, "不明")

        await self.log_send_embed(
            title=f"新しいイベント {name} を検知しました！",
            description=f"イベント概要: {description}",
            color=Client.EMBED_COLOR_INFO,
            param_dict={
                "id": event.id,
                "開始時間": start.strftime("%Y-%m-%d %H:%M"),
                "終了時間": end.strftime("%Y-%m-%d %H:%M"),
                "開催地": location,
            },
        )

        self.event_db.add(event)

    async def register_event_gcal(self, event: ScheduledEvent) -> Result[str, str]:
        """イベントをGoogle Calendarに登録します。

        Args:
            event (ScheduledEvent): 登録する ScheduledEvent オブジェクト。

        Returns:
            Result[id, err]:
        """
        match self.gc.createEvent(
            title=event.name,
            description=event.description,
            location=event.location,
            start=event.start_time,
            end=event.end_time,
        ):
            case Success(val):
                await self.log_send_embed(
                    title="Googleカレンダーに登録しました!",
                    description=val["htmlLink"],
                    color=Client.EMBED_COLOR_SUCC,
                    param_dict={"Summary": val["summary"], "EventID": val["id"]},
                )
                self.event_db.update_gcalEventID(
                    discord_event_id=event.id, gcal_event_id=val["id"]
                )

                return Success(val["id"])

            case Failure(err):
                await self.log_send_embed(
                    title="Googleカレンダーへの登録に失敗しました...",
                    description=err,
                    color=Client.EMBED_COLOR_CRIT,
                )
                return Failure(err)

        return Failure("")

    async def update_event_db(self, before: ScheduledEvent, after: ScheduledEvent):
        await self.log_send_embed(
            title=f"イベント {after.id} の更新を検知しました！",
            description="",
            param_dict=event_diff(
                CalendarEvent.parse(before), CalendarEvent.parse(after)
            ),
            color=Client.EMBED_COLOR_INFO,
        )

        self.event_db.update_eventInfo(discord_event_id=after.id, event=after)

    async def update_event_gcal(self, update_event: ScheduledEvent) -> Result[str, str]:
        gcal_ev_id = self.event_db.get_event_from_discord_event_id(
            update_event.id
        ).gcalEventID

        if gcal_ev_id is None:
            raise ValueError("")

        match self.gc.updateEvent(
            gcal_ev_id=gcal_ev_id,
            title=update_event.name,
            description=update_event.description,
            location=update_event.location,
            start=update_event.start_time,
            end=update_event.end_time,
        ):
            case Success(val):
                await self.log_send_embed(
                    title="Googleカレンダーを更新しました!",
                    description=val["htmlLink"],
                    color=Client.EMBED_COLOR_SUCC,
                    param_dict={"Summary": val["summary"], "EventID": val["id"]},
                )

                return Success(val["id"])

            case Failure(err):
                await self.log_send_embed(
                    title="Googleカレンダーの更新に失敗しました...",
                    description=err,
                    color=Client.EMBED_COLOR_CRIT,
                )
                return Failure(err)

        return Failure("")

    async def remove_event_db(self, event: ScheduledEvent):
        await self.log_send_embed(
            title="イベントの削除を検知しました!",
            description=f"イベント名: {event.name}",
            color=Client.EMBED_COLOR_SUCC,
            param_dict={
                "ID": event.id,
                "開始時刻": event.start_time.strftime("%Y-%m-%d %H:%M"),
                "終了時刻": event.end_time.strftime("%Y-%m-%d %H:%M"),
            },
        )
        return self.event_db.pop(event.id)

    async def remove_event_db_from_id(self, id: str):
        event = self.event_db.pop(id)
        await self.log_send_embed(
            title="イベントの削除を検知しました!",
            description=f"イベント名: {event.eventInfo.title}",
            color=Client.EMBED_COLOR_SUCC,
            param_dict={
                "ID": event.discordEventID,
                "開始時刻": event.eventInfo.start.strftime("%Y-%m-%d %H:%M"),
                "終了時刻": event.eventInfo.end.strftime("%Y-%m-%d %H:%M"),
            },
        )
        return event

    async def remove_event_gcal(
        self, removed_event: RegisteredEventEntry
    ) -> Result[None, str]:
        match ret := self.gc.deleteEvent(ev_id=removed_event.gcalEventID):
            case Success(_):
                await self.log_send_embed(
                    title="Googleカレンダーからイベントを削除しました!",
                    description=f"削除したイベント: {removed_event.eventInfo.title}",
                    color=Client.EMBED_COLOR_SUCC,
                    param_dict={"EventID": removed_event.gcalEventID},
                )
            case Failure(err):
                await self.log_send_embed(
                    title="Googleカレンダーの更新に失敗しました...",
                    description=err,
                    color=Client.EMBED_COLOR_CRIT,
                )

        return ret

    async def on_message(self, message: Message):
        if message.author == self.user:
            return

        if message.channel.id != int(os.getenv("OBSERVE_CH_ID")):
            return

        await self.log_send("Message Recieved!")

    async def on_ready(self):
        self.ch = self.get_channel(int(os.getenv("LOG_CH_ID")))
        print(self.ch)
        # await self.log_send("Ready!")
        print("Ready!")

        # 未登録のイベントがないかチェック
        # TODO: get_guilds関数を使って丁寧な実装をする
        d_event_id_list = set()
        for event in self.guilds[0].scheduled_events:
            print(event)
            d_event_id_list.add(event.id)

            # DBに登録されていないなら、DBにに登録
            if not self.event_db.is_event_exist(discord_event_id=event.id):
                print("DBに登録されていません!")
                await self.register_event_db(event)
            # Google Calendarに登録されていないなら登録して、DBにも通知
            if not self.event_db.is_gcal_registered_event(discord_event_id=event.id):
                print("カレンダーに登録されていません!")
                await self.register_event_gcal(event=event)
            # イベント内容が変更されていたら、更新
            if self.event_db.is_need_update_registered_event(event=event):
                print("イベントの変更を検知しました!")
                await self.update_event_db(
                    self.event_db.get_event_from_discord_event_id(event.id).eventInfo,
                    event,
                )
                await self.update_event_gcal(event)

            # イベントが終了していたら、DBから削除
            if self.event_db.is_expired_event(event=event):
                print("期限切れのイベントをDBから削除しました!")
                await self.remove_event_db(event)

        # Discordから削除されたイベントがないかチェック
        for dID, event in list(self.event_db.get_items_iter()):
            # DBにはあるがdiscordのイベントには存在しないとき
            if dID not in d_event_id_list:
                print("Discord側に見つからないDBのイベントを削除しました!")
                # DBから削除
                removed_event = await self.remove_event_db_from_id(dID)
                # 期限切れでないならGoogle Calendarからも削除
                if not removed_event.eventInfo.is_expire():
                    print("Google Calendarからも削除しました!")
                    await self.remove_event_gcal(removed_event)

        self.event_db.dump()

    async def on_scheduled_event_create(self, event: ScheduledEvent):
        await self.register_event_db(event)
        await self.register_event_gcal(event)

    async def on_scheduled_event_update(
        self, before: ScheduledEvent, after: ScheduledEvent
    ):
        if (before.id == after.id) and (before.status != after.status):
            print(f"イベント: {before.name} が {after.status.name} になりました")
            if after.status.name == "completed":
                await self.remove_event_db(after)

        await self.update_event_db(before, after)
        await self.update_event_gcal(update_event=after)

    async def on_scheduled_event_delete(self, event: ScheduledEvent):
        removed_event = await self.remove_event_db(event)
        if not removed_event.eventInfo.is_expire():
            await self.remove_event_gcal(removed_event)

    async def log_send(self, message):
        await self.ch.send(message)
        print(message)

    async def log_send_embed(
        self, title, description, color, param_dict: dict[str, str] | None = None
    ):
        param_dict = {} if param_dict is None else param_dict

        embed = discord.Embed(title=title, color=color, description=description)

        for key, value in param_dict.items():
            embed.add_field(name=key, value=value, inline=False)

        await self.ch.send(embed=embed)
