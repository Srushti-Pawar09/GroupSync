from datetime import datetime


def get_common_dates(users):
    start_dates = [datetime.fromisoformat(u["start_date"]) for u in users]
    end_dates = [datetime.fromisoformat(u["end_date"]) for u in users]

    latest_start = max(start_dates)
    earliest_end = min(end_dates)

    if earliest_end <= latest_start:
        return None, 0

    duration = (earliest_end - latest_start).days
    return (latest_start, earliest_end), duration
