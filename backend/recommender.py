from collections import defaultdict
from csv_loader import load_destinations
from utils import get_common_dates


MIN_TRIP_DAYS = 2
MAX_TRIP_DAYS = 7


def estimate_travel_cost(avg_distance, transport_modes):
    """
    Simple travel model:
    - Road/Rail: distance * 2 (round trip) * ₹2 per km
    - Flight: flat ₹4000 minimum
    """

    if "flight" in transport_modes:
        return 4000

    # road/rail default
    return avg_distance * 2 * 2


def recommend_destinations(users):

    destinations = load_destinations()
    date_range, duration = get_common_dates(users)

    if duration <= 0:
        return []

    lowest_budget = min(u["budget"] for u in users)

    # Remove food as structural vibe
    all_vibes = {
        v.lower()
        for u in users
        for v in u["vibes"]
        if v.lower() not in ["food", "cuisine", "eat"]
    }

    city_data = defaultdict(list)

    # -------- PHASE 1: Filter & group by city --------
    for dest in destinations:

        if not dest["recommended_for_groups"]:
            continue

        matched_vibes = [
            vibe
            for vibe in all_vibes
            if any(vibe in dv for dv in dest["vibe_all"])
        ]

        if not matched_vibes:
            continue

        city_data[dest["city"]].append({
            "matched_vibes": matched_vibes,
            "rating": dest["rating"],
            "group_score": dest["group_suitability_score"],
            "cost_per_day": dest["total_estimated_cost_per_person_per_day"],
            "distance": dest["distance_from_major_city"],
            "transport_modes": dest.get("possible_transport_modes", ["road"]),
            "place": dest["place"],
            "famous_food": dest.get("famous_food", "")
        })

    results = []

    # -------- PHASE 2: Aggregate city-level --------
    for city, places in city_data.items():

        covered_vibes = set()
        ratings = []
        group_scores = []
        costs = []
        distances = []
        transport_modes = set()

        for p in places:
            covered_vibes.update(p["matched_vibes"])
            ratings.append(p["rating"])
            group_scores.append(p["group_score"])
            costs.append(p["cost_per_day"])
            distances.append(p["distance"])
            transport_modes.update(p["transport_modes"])

        coverage_ratio = len(covered_vibes) / len(all_vibes)

        avg_cost_per_day = sum(costs) / len(costs)
        avg_distance = sum(distances) / len(distances)

        travel_cost = estimate_travel_cost(avg_distance, transport_modes)

        # -------- PHASE 3: Budget-aware duration --------
        max_affordable_days = int(
            (lowest_budget - travel_cost) // avg_cost_per_day
        )

        suggested_days = min(duration, max_affordable_days)
        suggested_days = min(suggested_days, MAX_TRIP_DAYS)

        if suggested_days < MIN_TRIP_DAYS:
            continue

        stay_cost = avg_cost_per_day * suggested_days
        total_cost = stay_cost + travel_cost

        if total_cost > lowest_budget:
            continue

        # -------- Viability Filters --------
        if coverage_ratio < 0.6:
            continue

        avg_rating = sum(ratings) / len(ratings)
        avg_group_score = sum(group_scores) / len(group_scores)

        if avg_rating < 4:
            continue

        results.append({
            "city": city,
            "coverage_ratio": round(coverage_ratio, 2),
            "covered_vibes": list(covered_vibes),
            "missing_vibes": list(all_vibes - covered_vibes),
            "suggested_days": suggested_days,
            "stay_cost_per_person": round(stay_cost, 2),
            "travel_cost_per_person": round(travel_cost, 2),
            "total_cost_per_person": round(total_cost, 2),
            "budget_headroom": round(lowest_budget - total_cost, 2),
            "avg_rating": round(avg_rating, 2),
            "avg_group_score": round(avg_group_score, 2),
            "sample_places": [p["place"] for p in places[:3]],
            "famous_foods": list({
                p["famous_food"] for p in places if p["famous_food"]
            })
        })

    if not results:
        return []

    # -------- FINAL RANKING --------
    results = sorted(
        results,
        key=lambda x: (
            -x["coverage_ratio"],
            -x["avg_rating"],
            -x["avg_group_score"],
            x["total_cost_per_person"]
        )
    )

    return results[:2]
