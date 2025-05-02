from datetime import datetime
import os.path

from google.oauth2 import service_account


from lib.datastructure.calendarEvent import CalendarEvent

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import dotenv
import os

from returns.result import Result, Failure, Success
from .typedef.gapi_calendar_v3_structs import Event

dotenv.load_dotenv()

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]


class GoogleCalendar:
    def __init__(self, unuse: bool = False):
        self.creds = None
        self.unuse = unuse
        if self.unuse:
            return

        credentials = service_account.Credentials.from_service_account_file(
            "./.local/credentials.json", scopes=SCOPES
        )

        delegated_credentials = credentials.with_subject(os.getenv("ROOT_ACCOUNT"))

        self.service = build("calendar", "v3", credentials=delegated_credentials)

    def createEvent(
        self,
        title: str,
        description: str,
        start: datetime,
        end: datetime,
        location: str,
    ) -> Result[Event, str]:
        body = CalendarEvent.create(
            title=title,
            start=start,
            end=end,
            description=description,
            location=location,
        )

        if self.unuse:
            print(f"Create Event, body: {body}")
            return Success(None)

        try:
            events_result = (
                self.service.events()
                .insert(
                    calendarId=os.getenv("CALENDAR_ID"),
                    body=body,
                )
                .execute()
            )
        except HttpError as e:
            print(e)
            return Failure(e.reason)

        return Success(events_result)

    def updateEvent(
        self,
        gcal_ev_id: str,
        title: str,
        description: str,
        start: datetime,
        end: datetime,
        location: str,
    ) -> Result[Event, str]:
        body = CalendarEvent.create(
            title=title,
            start=start,
            end=end,
            description=description,
            location=location,
        )

        if self.unuse:
            print(f"Create Event, body: {body}")
            return Success(None)

        try:
            events_result = (
                self.service.events()
                .update(
                    calendarId=os.getenv("CALENDAR_ID"),
                    eventId=gcal_ev_id,
                    body=body,
                )
                .execute()
            )
        except HttpError as e:
            return Failure(e.reason)

        return Success(events_result)

    def deleteEvent(self, ev_id: str) -> Result[None, str]:
        try:
            self.service.events().delete(
                calendarId=os.getenv("CALENDAR_ID"), eventId=ev_id, sendUpdates="none"
            ).execute()
        except HttpError as e:
            return Failure(e.reason)

        return Success(None)
