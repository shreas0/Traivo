import pickle
from pathlib import Path

import pandas as pd


MODEL_DIR = Path(__file__).resolve().parent
DATA_PATH = MODEL_DIR.parent / "data_processing" / "traivo_destination_knn_training.csv"
data = pd.read_csv(DATA_PATH)

with open(MODEL_DIR / "main_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)
with open(MODEL_DIR / "vectorizer.pkl", "rb") as vectorizer_file:
    vectorizer = pickle.load(vectorizer_file)

def model_response(budget_preference, group_preference, vibe_preference,
                   climate_preference, continent_preference):
    destinations = data.drop_duplicates("destination_name").copy()
    preferences = [budget_preference, group_preference, vibe_preference,
                   climate_preference, continent_preference]
    destination_columns = ["destination_budget", "destination_group_size",
                           "destination_vibe", "destination_climate",
                           "destination_continent"]
    preference_columns = [
        "budget_preference", "group_preference", "vibe_preference",
        "climate_preference", "continent_preference",
    ]
    for preference, column in zip(preferences, preference_columns):
        destinations[column] = preference

    feature_columns = preference_columns + destination_columns
    features = vectorizer.transform(destinations[feature_columns].to_dict("records"))
    destinations["score"] = model.predict_proba(features)[:, 1]

    return destinations.sort_values("score", ascending=False)["destination_name"].head(3).tolist()

