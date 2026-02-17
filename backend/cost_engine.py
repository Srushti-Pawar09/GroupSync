def calculate_travel_cost(distance_km):
    """
    Conservative Indian blended cost estimate
    Train + bus blended cost ~ ₹4/km
    """
    cost_per_km = 4
    return distance_km * cost_per_km * 2  # round trip


def calculate_stay_cost(per_day_cost, stay_days):
    return per_day_cost * stay_days


def calculate_total_cost(travel_cost, stay_cost):
    return travel_cost + stay_cost
