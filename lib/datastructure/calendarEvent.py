from datetime import datetime


class CalendarEvent:
    def __init__(self, title, start, end):
        self.title = title
        self.start = start
        self.end = end

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

    def obj(self):
        return {
            "start": {
                "dateTime": f"{self.start}",
            },
            "end": {
                "dateTime": f"{self.start}",
            },
            "summary": self.title,
        }
