from datetime import datetime


def format_time(dt: datetime) -> str:
    hour = dt.hour
    if hour <= 4:
        hour += 24
    return f'{hour:02d}:{dt.minute:02d}:{dt.second:02d}'


def format_full_time(dt: datetime) -> str:
    return dt.strftime("%m月%d日 %H:%M:%S")
