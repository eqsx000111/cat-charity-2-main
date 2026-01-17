from datetime import datetime


def calculate_duration_days(
    start: datetime,
    end: datetime
) -> int:
    return (end.date() - start.date()).days
