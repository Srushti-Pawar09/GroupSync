from csv_loader import load_destinations
from cost_engine import calculate_stay_days, calculate_total_cost

def recommend_destinations(group_members):

    df = load_destinations()

    min_budget = min(member["budget"] for member in group_members)
    all_vibes = set()

    for member in group_members:
        all_vibes.update(member["vibes"])

    results = []

    for _, row in df.iterrows():

        destination_vibes = set(row["vibes"].split(","))
        matched_vibes = list(destination_vibes.intersection(all_vibes))

        if not matched_vibes:
            continue

        days = calculate_stay_days(
            group_members[0]["start_date"],
            group_members[0]["end_date"]
        )

        stay_cost, travel_cost, total = calculate_total_cost(
            row["per_day_cost"],
            days,
            row["distance_km"]
        )

        if total > min_budget:
            continue

        results.append({
            "city": row["city"],
            "place": row["place"],
            "stay_days": days,
            "travel_cost": travel_cost,
            "stay_cost": stay_cost,
            "total_cost": total,
            "matched_vibes": matched_vibes,
            "famous_food": row["famous_food"],
            "rating": row["rating"]
        })

    results = sorted(
        results,
        key=lambda x: (
            -len(x["matched_vibes"]),
            -x["rating"],
            x["total_cost"]
        )
    )

    return results[:2]
