from datetime import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from datastructure.calendarEvent import CalendarEvent

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import dotenv
import os
from zoneinfo import ZoneInfo

from returns.result import Result, Failure, Success

dotenv.load_dotenv()

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]


class GoogleCalendar:
    def __init__(self):
        self.creds = None
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
        self, title: str, start: datetime, end: datetime
    ) -> Result[None, str]:
        try:
            events_result = (
                self.service.events()
                .insert(
                    calendarId=os.getenv("CALENDAR_ID"),
                    body=CalendarEvent.create(
                        title=title,
                        start=start,
                        end=end,
                    ),
                )
                .execute()
            )
        except HttpError as e:
            return Failure(e.reason)

        return Success(None)
