# Copy and Sorted by googleapiclient-stubs/_apis/calendar/v3/schemas.pyi

import typing

_list = list


@typing.type_check_only
class AclRule:
    etag: str
    id: str
    kind: str
    role: str
    scope: dict[str, typing.Any]


@typing.type_check_only
class Acl:
    etag: str
    items: _list[AclRule]
    kind: str
    nextPageToken: str
    nextSyncToken: str


@typing.type_check_only
class ConferenceProperties:
    allowedConferenceSolutionTypes: _list[str]


@typing.type_check_only
class Calendar:
    conferenceProperties: ConferenceProperties
    description: str
    etag: str
    id: str
    kind: str
    location: str
    summary: str
    timeZone: str


@typing.type_check_only
class EventReminder:
    method: str
    minutes: int


@typing.type_check_only
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


@typing.type_check_only
class CalendarList:
    etag: str
    items: _list[CalendarListEntry]
    kind: str
    nextPageToken: str
    nextSyncToken: str


@typing.type_check_only
class CalendarNotification:
    method: str
    type: str


@typing.type_check_only
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


@typing.type_check_only
class ColorDefinition:
    background: str
    foreground: str


@typing.type_check_only
class Colors:
    calendar: dict[str, typing.Any]
    event: dict[str, typing.Any]
    kind: str
    updated: str


@typing.type_check_only
class ConferenceParametersAddOnParameters:
    parameters: dict[str, typing.Any]


@typing.type_check_only
class ConferenceParameters:
    addOnParameters: ConferenceParametersAddOnParameters


@typing.type_check_only
class ConferenceRequestStatus:
    statusCode: str


@typing.type_check_only
class ConferenceSolutionKey:
    type: str


@typing.type_check_only
class ConferenceSolution:
    iconUri: str
    key: ConferenceSolutionKey
    name: str


@typing.type_check_only
class CreateConferenceRequest:
    conferenceSolutionKey: ConferenceSolutionKey
    requestId: str
    status: ConferenceRequestStatus


@typing.type_check_only
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


@typing.type_check_only
class ConferenceData:
    conferenceId: str
    conferenceSolution: ConferenceSolution
    createRequest: CreateConferenceRequest
    entryPoints: _list[EntryPoint]
    notes: str
    parameters: ConferenceParameters
    signature: str


@typing.type_check_only
class Error:
    domain: str
    reason: str


@typing.type_check_only
class EventAttachment:
    fileId: str
    fileUrl: str
    iconLink: str
    mimeType: str
    title: str


@typing.type_check_only
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


@typing.type_check_only
class EventBirthdayProperties:
    contact: str
    customTypeName: str
    type: str


@typing.type_check_only
class EventDateTime:
    date: str
    dateTime: str
    timeZone: str


@typing.type_check_only
class EventFocusTimeProperties:
    autoDeclineMode: str
    chatStatus: str
    declineMessage: str


@typing.type_check_only
class EventOutOfOfficeProperties:
    autoDeclineMode: str
    declineMessage: str


@typing.type_check_only
class EventWorkingLocationProperties:
    customLocation: dict[str, typing.Any]
    homeOffice: typing.Any
    officeLocation: dict[str, typing.Any]
    type: str


@typing.type_check_only
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


@typing.type_check_only
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


@typing.type_check_only
class FreeBusyGroup:
    calendars: _list[str]
    errors: _list[Error]


@typing.type_check_only
class FreeBusyRequestItem:
    id: str


@typing.type_check_only
class FreeBusyRequest:
    calendarExpansionMax: int
    groupExpansionMax: int
    items: _list[FreeBusyRequestItem]
    timeMax: str
    timeMin: str
    timeZone: str


@typing.type_check_only
class FreeBusyResponse:
    calendars: dict[str, typing.Any]
    groups: dict[str, typing.Any]
    kind: str
    timeMax: str
    timeMin: str


@typing.type_check_only
class Setting:
    etag: str
    id: str
    kind: str
    value: str


@typing.type_check_only
class Settings:
    etag: str
    items: _list[Setting]
    kind: str
    nextPageToken: str
    nextSyncToken: str


@typing.type_check_only
class TimePeriod:
    end: str
    start: str


@typing.type_check_only
class FreeBusyCalendar:
    busy: _list[TimePeriod]
    errors: _list[Error]
