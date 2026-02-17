import pandas as pd
import os

def load_destinations():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(BASE_DIR, "data", "PROJECT_CSV.csv")

    df = pd.read_csv(file_path)

    # 🔥 Strip column names
    df.columns = df.columns.str.strip()

    # Normalize vibes
    df["vibe_all"] = df["vibe_all"].apply(
        lambda x: [v.strip().lower() for v in str(x).split(",") if v.strip()]
    )

    # Normalize recommended_for_groups
    df["recommended_for_groups"] = (
        df["recommended_for_groups"]
        .astype(str)
        .str.strip()
        .str.lower()
        .isin(["true", "yes", "1"])
    )

    # Normalize numeric columns safely
    numeric_cols = [
        "total_estimated_cost_per_person_per_day",
        "rating",
        "group_suitability_score",
        "distance_from_major_city",
        "ideal_stay_duration_days"
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    # Fill NaNs globally
    df = df.fillna("")

    # Ensure famous_food exists
    if "famous_food" not in df.columns:
        df["famous_food"] = ""

    df["famous_food"] = df["famous_food"].astype(str).fillna("")

    # Transport inference
    if "possible_transport_modes" in df.columns:
        df["possible_transport_modes"] = df["possible_transport_modes"].apply(
            lambda x: [m.strip().lower() for m in str(x).split(",") if m.strip()]
        )
    else:
        def infer_transport(row):
            modes = []
            if row.get("nearest_airport"):
                modes.append("flight")
            if row.get("nearest_railway_station"):
                modes.append("train")
            if row.get("nearest_bus_stop"):
                modes.append("road")
            return modes if modes else ["road"]

        df["possible_transport_modes"] = df.apply(infer_transport, axis=1)

    return df.to_dict(orient="records")
