import pandas as pd
from cost_engine import calculate_travel_cost, calculate_stay_cost, calculate_total_cost
from datetime import datetime
from cost_engine import calculate_travel_cost, calculate_stay_cost, calculate_total_cost

import pandas as pd

DATA_PATH = "data/PROJECT_CSV.csv"

def load_data():
    df = pd.read_csv(DATA_PATH)

    # Clean text columns
    df["vibe_all"] = df["vibe_all"].fillna("").str.lower()
    df["recommended_for_groups"] = df["recommended_for_groups"].astype(str).str.lower()

    return df



def find_common_dates(members):
    start_dates = [datetime.fromisoformat(m['start_date']) for m in members]
    end_dates = [datetime.fromisoformat(m['end_date']) for m in members]

    max_start = max(start_dates)
    min_end = min(end_dates)

    if max_start >= min_end:
        return None, 0

    return max_start, (min_end - max_start).days

def recommend_destinations(members):

    df = load_data()

    common_start, stay_days = find_common_dates(members)

    if stay_days <= 0:
        return []

    lowest_budget = min(m["budget"] for m in members)

    group_vibes = set()
    for m in members:
        group_vibes.update([v.lower() for v in m["vibes"]])

    results = []

    for _, row in df.iterrows():

        # Filter only group-friendly destinations
        if row["recommended_for_groups"] != "yes":
            continue

        # Match vibes
        destination_vibes = set(row["vibe_all"].split(","))
        matched_vibes = group_vibes.intersection(destination_vibes)

        if len(matched_vibes) == 0:
            continue

        stay_days_effective = min(
            stay_days,
            int(row["ideal_stay_duration_days"])
        )

        travel_cost = calculate_travel_cost(
            float(row["distance_from_major_city"])
        )

        stay_cost = calculate_stay_cost(
            float(row["total_estimated_cost_per_person_per_day"]),
            stay_days_effective
        )

        total_cost = calculate_total_cost(travel_cost, stay_cost)

        # FAIRNESS CONSTRAINT
        if total_cost > lowest_budget:
            continue

        # Transparent scoring
        score = (
            len(matched_vibes) * 15 +
            float(row["rating"]) * 5 +
            float(row["group_suitability_score"]) * 3 -
            total_cost * 0.002
        )

        results.append({
            "city": row["city"],
            "place": row["place"],
            "stay_days": stay_days_effective,
            "travel_cost": round(travel_cost),
            "stay_cost": round(stay_cost),
            "total_cost": round(total_cost),
            "matched_vibes": list(matched_vibes),
            "famous_food": row["famous_food"],
            "why_recommended": row["why_recommended"],
            "rating": float(row["rating"]),
            "score": score
        })

    results = sorted(results, key=lambda x: x["score"], reverse=True)

    return results[:2]
