from datetime import datetime


def parse_time(time_str: str) -> datetime:
    return datetime.strptime(time_str, "%H:%M")

def format_time(t: datetime) -> str:
    return t.strftime("%H:%M")
