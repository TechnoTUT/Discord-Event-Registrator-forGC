from pydantic import BaseModel, RootModel
from lib.datastructure.calendarEvent import CalendarEvent
from discord.scheduled_event import ScheduledEvent
from pathlib import Path
import json
from datetime import datetime
from zoneinfo import ZoneInfo
import threading


class RegisteredEventEntry(BaseModel):
    discordEventID: int
    gcalEventID: str | None
    eventInfo: CalendarEvent
    registered: datetime
    updated: datetime

    def updateInfo(
        self,
        discordEventID: int | None = None,
        gcalEventID: str | None = None,
        eventInfo: CalendarEvent | None = None,
    ):
        updateflag = False

        if discordEventID is not None:
            self.discordEventID = discordEventID
            updateflag = True
        if gcalEventID is not None:
            self.gcalEventID = gcalEventID
            updateflag = True
        if eventInfo is not None:
            self.eventInfo = eventInfo
            updateflag = True

        if updateflag:
            self.updated = datetime.now(tz=ZoneInfo("Asia/Tokyo"))

    @staticmethod
    def parse(discord_event_id: int, event: CalendarEvent) -> "RegisteredEventEntry":
        return RegisteredEventEntry(
            discordEventID=discord_event_id,
            gcalEventID=None,
            eventInfo=event,
            registered=datetime.now(tz=ZoneInfo("Asia/Tokyo")),
            updated=datetime.now(tz=ZoneInfo("Asia/Tokyo")),
        )


class RegisteredEvents:
    def __init__(self, path: str):
        self.__dID_event_dict: dict[str, RegisteredEventEntry] = {}
        self.__gID_dID_dict: dict[str, str] = {}

        self.db_path = path

        self.lock = threading.Lock()

        if Path(self.db_path).exists():
            with Path(self.db_path).open("r") as fp:
                for obj in json.load(fp=fp):
                    self.add(RegisteredEventEntry(**obj))

    def add(self, event: RegisteredEventEntry | ScheduledEvent):
        if isinstance(event, ScheduledEvent):
            event = RegisteredEventEntry.parse(
                discord_event_id=event.id, event=CalendarEvent.parse(event)
            )

        self.__dID_event_dict[event.discordEventID] = event
        if event.gcalEventID is not None:
            self.__gID_dID_dict[event.gcalEventID] = event.discordEventID

        self.dump()

    def pop(self, eventID: str):
        removed_event = self.__dID_event_dict.pop(eventID)

        if removed_event.gcalEventID is not None:
            self.__gID_dID_dict.pop(removed_event.gcalEventID)

        self.dump()

        return removed_event

    def update_gcalEventID(self, discord_event_id: str, gcal_event_id: str):
        self.__gID_dID_dict[gcal_event_id] = discord_event_id
        self.__dID_event_dict[discord_event_id].updateInfo(gcalEventID=gcal_event_id)

    def update_eventInfo(
        self, discord_event_id: str, event: RegisteredEventEntry | ScheduledEvent
    ):
        if isinstance(event, ScheduledEvent):
            event = RegisteredEventEntry.parse(
                discord_event_id=event.id, event=CalendarEvent.parse(event)
            )

        self.__dID_event_dict[discord_event_id].updateInfo(eventInfo=event.eventInfo)

        self.dump()

    def get_event_from_discord_event_id(
        self, discord_event_id: str
    ) -> RegisteredEventEntry:
        return self.__dID_event_dict[discord_event_id]

    def get_event_from_gcal_event_id(self, gcal_event_id: str) -> RegisteredEventEntry:
        return self.__dID_event_dict[self.__gID_dID_dict[gcal_event_id]]

    def is_event_exist(self, discord_event_id: str) -> bool:
        return discord_event_id in self.__dID_event_dict.keys()

    def is_gcal_registered_event(self, discord_event_id: str) -> bool:
        return self.__dID_event_dict[discord_event_id].gcalEventID is not None

    def is_need_update_registered_event(
        self, event: RegisteredEventEntry | ScheduledEvent
    ) -> bool:
        if isinstance(event, ScheduledEvent):
            event = RegisteredEventEntry.parse(
                discord_event_id=event.id, event=CalendarEvent.parse(event)
            )

        return self.__dID_event_dict[event.discordEventID].eventInfo != event.eventInfo

    def is_expired_event(self, event: RegisteredEventEntry | ScheduledEvent) -> bool:
        if isinstance(event, ScheduledEvent):
            event = RegisteredEventEntry.parse(
                discord_event_id=event.id, event=CalendarEvent.parse(event)
            )

        return self.__dID_event_dict[event.discordEventID].eventInfo.is_expire()

    def dump(self):
        with self.lock:
            with Path(self.db_path).open("w") as fp:
                fp.write(
                    RootModel[list](self.__dID_event_dict.values()).model_dump_json(
                        indent=4
                    )
                )

    def __iter__(self):
        return self.__dID_event_dict.__iter__()

    def get_items_iter(self):
        return self.__dID_event_dict.items()
