from datetime import datetime

def find_common_dates(date_ranges):
    starts = [datetime.strptime(d[0], "%Y-%m-%d") for d in date_ranges]
    ends = [datetime.strptime(d[1], "%Y-%m-%d") for d in date_ranges]

    latest_start = max(starts)
    earliest_end = min(ends)

    if latest_start <= earliest_end:
        stay_days = (earliest_end - latest_start).days + 1
        return stay_days
    return 0
