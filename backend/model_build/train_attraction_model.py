import pickle
from itertools import product
from pathlib import Path

import pandas as pd
from sklearn.feature_extraction import DictVectorizer
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score


MODEL_DIR = Path(__file__).resolve().parent
DATA_PATH = MODEL_DIR.parent / "data_processing" / "traivo_attractions.csv"
data = pd.read_csv(DATA_PATH)
training_rows = []

for _, attraction in data.iterrows():
    for vibe, budget, hours in product(
        ["any", "beach", "nature", "history", "culture", "adventure", "food"],
        ["any", "low", "medium", "high"],
        [2, 4, 8],
    ):
        cost_match = budget == "any" or attraction["cost"] == "low" or (
            budget == "medium" and attraction["cost"] == "medium"
        ) or budget == "high"
        vibe_match = vibe == "any" or attraction["vibe"] == vibe
        enough_time = int(attraction["visit_hours"]) <= hours
        training_rows.append({
            "category": attraction["category"],
            "vibe": attraction["vibe"],
            "cost": attraction["cost"],
            "visit_hours": int(attraction["visit_hours"]),
            "vibe_preference": vibe,
            "budget_preference": budget,
            "hours_available": hours,
            "recommended": int(cost_match and vibe_match and enough_time),
        })

training_data = pd.DataFrame(training_rows)
feature_columns = ["category", "vibe", "cost", "visit_hours",
                   "vibe_preference", "budget_preference", "hours_available"]
vectorizer = DictVectorizer(sparse=True)
features = vectorizer.fit_transform(training_data[feature_columns].to_dict("records"))
labels = training_data["recommended"]
X_train, X_test, y_train, y_test = train_test_split(
    features, labels, test_size=0.2, random_state=42, stratify=labels
)
model = KNeighborsClassifier(n_neighbors=5, weights="distance")
model.fit(X_train, y_train)
predictions = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, predictions))

with open(MODEL_DIR / "attraction_model.pkl", "wb") as model_file:
    pickle.dump((model, vectorizer), model_file)
