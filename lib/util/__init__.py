from __future__ import annotations
from typing import TypeVar, TYPE_CHECKING

if TYPE_CHECKING:
    from lib.datastructure.calendarEvent import CalendarEvent

T = TypeVar("T")


def Optional_or(value: T | None, default: T) -> T:
    return value if value is not None else default


def event_diff(before: CalendarEvent, after: CalendarEvent) -> dict[str, str]:
    msg: dict[str, str] = {}
    if before.title != after.title:
        msg["タイトル"] = f"{before.title} -> {after.title}"
    if before.description != after.description:
        msg["概要"] = f"{before.description} -> {after.description}"
    if before.location != after.location:
        msg["場所"] = f"{before.location} -> {after.location}"
    if before.start != after.start:
        msg["開始時刻"] = (
            f"{before.start.strftime('%Y-%m-%d %H:%M')} -> {after.start.strftime('%Y-%m-%d %H:%M')}"
        )
    if before.end != after.end:
        msg["終了時刻"] = (
            f"{before.end.strftime('%Y-%m-%d %H:%M')} -> {after.end.strftime('%Y-%m-%d %H:%M')}"
        )

    return msg
