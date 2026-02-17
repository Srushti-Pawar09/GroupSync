def calculate_stay_cost(cost_per_day, duration):
    return cost_per_day * duration


def calculate_travel_cost(distance_km):
    # Assume ₹7 per km round-trip divided per person
    return distance_km * 7
