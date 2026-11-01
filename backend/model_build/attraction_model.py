import pickle
from pathlib import Path

import pandas as pd


MODEL_DIR = Path(__file__).resolve().parent
DATA_PATH = MODEL_DIR.parent / "data_processing" / "traivo_attractions.csv"
MODEL_PATH = MODEL_DIR / "attraction_model.pkl"
data = pd.read_csv(DATA_PATH)

with open(MODEL_PATH, "rb") as model_file:
    model, vectorizer = pickle.load(model_file)


def recommend_attractions(destination, vibe="any", budget="any", hours=8):
    attractions = data[data["destination"].str.lower() == destination.lower()].copy()
    if attractions.empty:
        return []

    if vibe != "any":
        attractions = attractions[attractions["vibe"] == vibe]
    if budget == "low":
        attractions = attractions[attractions["cost"] == "low"]
    elif budget == "medium":
        attractions = attractions[attractions["cost"].isin(["low", "medium"])]
    if attractions.empty:
        return []

    attractions["vibe_preference"] = vibe
    attractions["budget_preference"] = budget
    attractions["hours_available"] = hours
    feature_columns = ["category", "vibe", "cost", "visit_hours",
                       "vibe_preference", "budget_preference", "hours_available"]
    features = vectorizer.transform(attractions[feature_columns].to_dict("records"))
    attractions["score"] = model.predict_proba(features)[:, 1]
    attractions = attractions[attractions["visit_hours"] <= hours]
    return attractions.sort_values("score", ascending=False)["attraction"].head(3).tolist()
