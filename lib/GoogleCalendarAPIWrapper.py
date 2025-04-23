from datetime import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

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

        if os.path.exists("./.local/token.json"):
            self.creds = Credentials.from_authorized_user_file(
                "./.local/token.json", SCOPES
            )
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "./.local/credentials.json", SCOPES
                )
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("./.local/token.json", "w") as token:
                token.write(self.creds.to_json())

        self.service = build("calendar", "v3", credentials=self.creds)

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
