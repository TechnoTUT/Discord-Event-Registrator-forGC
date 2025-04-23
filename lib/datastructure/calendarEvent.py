from pydantic import BaseModel, field_serializer
from datetime import datetime, timedelta
from discord.scheduled_event import ScheduledEvent
from lib.util import Optional_or


class CalendarEvent(BaseModel):
    title: str
    description: str
    location: str
    start: datetime
    end: datetime

    @field_serializer("start", "end")
    def datetime_serializer(self, time: datetime, _info):
        return time.isoformat()

    @staticmethod
    def create(title, start: datetime, end: datetime, description: str, location: str):
        return {
            "start": {
                "dateTime": f"{start.isoformat()}",
            },
            "end": {
                "dateTime": f"{end.isoformat()}",
            },
            "summary": title,
            "description": description,
            "location": location,
        }

    @staticmethod
    def parse(event: ScheduledEvent) -> "CalendarEvent":
        return CalendarEvent(
            title=event.name,
            description=Optional_or(event.description, "不明"),
            location=Optional_or(event.location, "不明"),
            start=event.start_time,
            end=Optional_or(
                event.end_time, default=event.start_time + timedelta(hours=1)
            ),
        )

    def obj(self):
        return {
            "start": {
                "dateTime": f"{self.start}",
            },
            "end": {
                "dateTime": f"{self.start}",
            },
            "summary": self.title,
            "description": self.description,
            "location": self.location,
        }
