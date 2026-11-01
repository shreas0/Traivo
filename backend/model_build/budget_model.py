import pickle
from pathlib import Path

import pandas as pd


MODEL_DIR = Path(__file__).resolve().parent

with open(MODEL_DIR / "budget_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)


def predict_budget(details):
    trip = {
        "destination": details.get("destination") or "Goa",
        "travellers": details.get("travellers") or 1,
        "trip_days": details.get("trip_days") or 3,
        "travel_style": details.get("travel_style") or "comfortable",
        "season_demand": details.get("season_demand") or "low",
        "activity_intensity": details.get("activity_intensity") or "balanced",
        "accommodation_type": details.get("accommodation_type") or "midrange_hotel",
        "trip_origin_type": details.get("trip_origin_type") or "same_country",
    }
    estimate = model.predict(pd.DataFrame([trip]))[0]
    return max(0, round(estimate))
