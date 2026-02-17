from math import ceil

def calculate_stay_days(start_date, end_date):
    from datetime import datetime

    d1 = datetime.fromisoformat(start_date)
    d2 = datetime.fromisoformat(end_date)

    return (d2 - d1).days


def calculate_total_cost(per_day_cost, days, distance_km):

    stay_cost = per_day_cost * days
    travel_cost = distance_km * 8  # ₹8 per km estimate

    return stay_cost, travel_cost, stay_cost + travel_cost
