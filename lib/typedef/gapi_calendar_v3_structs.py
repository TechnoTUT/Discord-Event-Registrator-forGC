# Copy and Sorted by googleapiclient-stubs/_apis/calendar/v3/schemas.pyi

import typing

_list = list


class AclRule:
    etag: str
    id: str
    kind: str
    role: str
    scope: dict[str, typing.Any]


class Acl:
    etag: str
    items: _list[AclRule]
    kind: str
    nextPageToken: str
    nextSyncToken: str


class ConferenceProperties:
    allowedConferenceSolutionTypes: _list[str]


class Calendar:
    conferenceProperties: ConferenceProperties
    description: str
    etag: str
    id: str
    kind: str
    location: str
    summary: str
    timeZone: str


class EventReminder:
    method: str
    minutes: int


class CalendarListEntry:
    accessRole: str
    backgroundColor: str
    colorId: str
    conferenceProperties: ConferenceProperties
    defaultReminders: _list[EventReminder]
    deleted: bool
    description: str
    etag: str
    foregroundColor: str
    hidden: bool
    id: str
    kind: str
    location: str
    notificationSettings: dict[str, typing.Any]
    primary: bool
    selected: bool
    summary: str
    summaryOverride: str
    timeZone: str


class CalendarList:
    etag: str
    items: _list[CalendarListEntry]
    kind: str
    nextPageToken: str
    nextSyncToken: str


class CalendarNotification:
    method: str
    type: str


class Channel:
    address: str
    expiration: str
    id: str
    kind: str
    params: dict[str, typing.Any]
    payload: bool
    resourceId: str
    resourceUri: str
    token: str
    type: str


class ColorDefinition:
    background: str
    foreground: str


class Colors:
    calendar: dict[str, typing.Any]
    event: dict[str, typing.Any]
    kind: str
    updated: str


class ConferenceParametersAddOnParameters:
    parameters: dict[str, typing.Any]


class ConferenceParameters:
    addOnParameters: ConferenceParametersAddOnParameters


class ConferenceRequestStatus:
    statusCode: str


class ConferenceSolutionKey:
    type: str


class ConferenceSolution:
    iconUri: str
    key: ConferenceSolutionKey
    name: str


class CreateConferenceRequest:
    conferenceSolutionKey: ConferenceSolutionKey
    requestId: str
    status: ConferenceRequestStatus


class EntryPoint:
    accessCode: str
    entryPointFeatures: _list[str]
    entryPointType: str
    label: str
    meetingCode: str
    passcode: str
    password: str
    pin: str
    regionCode: str
    uri: str


class ConferenceData:
    conferenceId: str
    conferenceSolution: ConferenceSolution
    createRequest: CreateConferenceRequest
    entryPoints: _list[EntryPoint]
    notes: str
    parameters: ConferenceParameters
    signature: str


class Error:
    domain: str
    reason: str


class EventAttachment:
    fileId: str
    fileUrl: str
    iconLink: str
    mimeType: str
    title: str


class EventAttendee:
    additionalGuests: int
    comment: str
    displayName: str
    email: str
    id: str
    optional: bool
    organizer: bool
    resource: bool
    responseStatus: str
    self: bool


class EventBirthdayProperties:
    contact: str
    customTypeName: str
    type: str


class EventDateTime:
    date: str
    dateTime: str
    timeZone: str


class EventFocusTimeProperties:
    autoDeclineMode: str
    chatStatus: str
    declineMessage: str


class EventOutOfOfficeProperties:
    autoDeclineMode: str
    declineMessage: str


class EventWorkingLocationProperties:
    customLocation: dict[str, typing.Any]
    homeOffice: typing.Any
    officeLocation: dict[str, typing.Any]
    type: str


class Event:
    anyoneCanAddSelf: bool
    attachments: _list[EventAttachment]
    attendees: _list[EventAttendee]
    attendeesOmitted: bool
    birthdayProperties: EventBirthdayProperties
    colorId: str
    conferenceData: ConferenceData
    created: str
    creator: dict[str, typing.Any]
    description: str
    end: EventDateTime
    endTimeUnspecified: bool
    etag: str
    eventType: str
    extendedProperties: dict[str, typing.Any]
    focusTimeProperties: EventFocusTimeProperties
    gadget: dict[str, typing.Any]
    guestsCanInviteOthers: bool
    guestsCanModify: bool
    guestsCanSeeOtherGuests: bool
    hangoutLink: str
    htmlLink: str
    iCalUID: str
    id: str
    kind: str
    location: str
    locked: bool
    organizer: dict[str, typing.Any]
    originalStartTime: EventDateTime
    outOfOfficeProperties: EventOutOfOfficeProperties
    privateCopy: bool
    recurrence: _list[str]
    recurringEventId: str
    reminders: dict[str, typing.Any]
    sequence: int
    source: dict[str, typing.Any]
    start: EventDateTime
    status: str
    summary: str
    transparency: str
    updated: str
    visibility: str
    workingLocationProperties: EventWorkingLocationProperties


class Events:
    accessRole: str
    defaultReminders: _list[EventReminder]
    description: str
    etag: str
    items: _list[Event]
    kind: str
    nextPageToken: str
    nextSyncToken: str
    summary: str
    timeZone: str
    updated: str


class FreeBusyGroup:
    calendars: _list[str]
    errors: _list[Error]


class FreeBusyRequestItem:
    id: str


class FreeBusyRequest:
    calendarExpansionMax: int
    groupExpansionMax: int
    items: _list[FreeBusyRequestItem]
    timeMax: str
    timeMin: str
    timeZone: str


class FreeBusyResponse:
    calendars: dict[str, typing.Any]
    groups: dict[str, typing.Any]
    kind: str
    timeMax: str
    timeMin: str


class Setting:
    etag: str
    id: str
    kind: str
    value: str


class Settings:
    etag: str
    items: _list[Setting]
    kind: str
    nextPageToken: str
    nextSyncToken: str


class TimePeriod:
    end: str
    start: str


class FreeBusyCalendar:
    busy: _list[TimePeriod]
    errors: _list[Error]
