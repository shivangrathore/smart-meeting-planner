from datetime import datetime, timedelta
from models import User, BookRequest
from pydantic import BaseModel, Field

from utils import format_time, parse_time


class BookedSlot(BaseModel):
    participants: list[int] = Field(..., description="List of user IDs who booked the slot")
    start: str = Field(..., description="Start time of the booked slot")
    end: str = Field(..., description="End time of the booked slot")


WORK_START = "09:00"
WORK_END = "18:00"


# Utils

def merge_intervals(intervals: list[tuple[str, str]]) -> list[list[datetime]]:
    nintervals = sorted([tuple(map(parse_time, i)) for i in intervals])
    merged = []
    for start, end in nintervals:
        if not merged or start > merged[-1][1]:
            merged.append([start, end])
        else:
            merged[-1][1] = max(merged[-1][1], end)
    return merged

def invert_intervals(intervals: list[list[datetime]], start_time: datetime, end_time: datetime) -> list[tuple[datetime, datetime]]:
    result: list[tuple[datetime, datetime]] = []
    current = start_time
    for s, e in intervals:
        if current < s:
            result.append((current, s))
        current = max(current, e)
    if current < end_time:
        result.append((current, end_time))
    return result



class Database:
    def __init__(self):
        self.users: dict[int, User] = {}
        self.booked: list[BookedSlot] = []

    def add_slots(self, users: list[User]) -> None:
        for user in users:
            self.users[user.id] = user

    def get_user_calendar(self, user_id: int):
        user = self.users.get(user_id)
        return {
            "user_id": user_id,
            "busy": [] if user is None else user.busy,
            "booked": [b for b in self.booked if user_id in b.participants]
        }

    def book_slot(self, payload: BookRequest) -> None:
        start, end = payload.interval
        slot = BookedSlot(
            participants=payload.participants or list(self.users.keys()),
            start=start,
            end=end
        )
        self.booked.append(slot)

    def suggest_slots(self, duration_minutes: int):
        work_start = parse_time(WORK_START)
        work_end = parse_time(WORK_END)

        all_busy = []

        for user_busy in self.users.values():
            all_busy.extend(user_busy.busy)

        all_busy.extend([(b.start, b.end) for b in self.booked])
        merged = merge_intervals(all_busy)
        free_slots = invert_intervals(merged, work_start, work_end)
        duration = timedelta(minutes=duration_minutes)
        suggestions = []
        for start, end in free_slots:
            while start + duration <= end:
                suggestions.append({
                    "start": format_time(start),
                    "end": format_time(start + duration),
                    "participants": list(self.users.keys())
                })
                start += duration

        return suggestions

