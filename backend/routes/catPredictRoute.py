from pathlib import Path

import joblib
import numpy as np
from flask import Blueprint, jsonify, request

from config.config import BACKEND_ROOT

category_bp = Blueprint("category", __name__)

CATEGORIES = [
    "Food",
    "Entertainment",
    "Sports",
    "Shopping",
    "Gym",
    "Petrol",
    "Travel",
    "Snacks",
    "Misc",
]

MODELS_DIR = BACKEND_ROOT / "models3"

_food_level_mapping = {"Low": 1, "Medium": 2, "High": 0}
_entertainment_mapping = {"Low": 1, "High": 0}

_category_models = {}


def _load_models():
    global _category_models
    if _category_models:
        return
    for category in CATEGORIES:
        path = MODELS_DIR / f"{category}_model.pkl"
        _category_models[category] = joblib.load(path)


@category_bp.record_once
def _on_register(state):
    _load_models()


@category_bp.route("/predict-category", methods=["POST"])
def predict_category():
    try:
        data = request.get_json() or {}
        budget = data.get("budget")
        month = data.get("month")
        food_level = data.get("food_level")
        entertainment_level = data.get("entertainment_level")

        if budget is None or month is None or food_level is None or entertainment_level is None:
            return jsonify({"error": "Missing required fields"}), 400

        budget = float(budget)
        month = int(month)
        if month < 1 or month > 12:
            return jsonify({"error": "Month must be between 1 and 12"}), 400
        if budget <= 0:
            return jsonify({"error": "Budget must be positive"}), 400

        food_level_value = _food_level_mapping.get(food_level, -1)
        entertainment_value = _entertainment_mapping.get(entertainment_level, -1)

        if food_level_value == -1 or entertainment_value == -1:
            return jsonify({"error": "Invalid food_level or entertainment_level provided"}), 400

        _load_models()
        input_features = np.array([[month, food_level_value, entertainment_value]])

        category_expenses = {}
        for category in CATEGORIES:
            category_expenses[category] = float(
                _category_models[category].predict(input_features)[0]
            )

        total_expense = sum(category_expenses.values())
        budget_status = "Under Budget" if total_expense <= budget else "Over Budget"
        budget_difference = (
            budget - total_expense if total_expense <= budget else total_expense - budget
        )

        return jsonify(
            {
                "category_expenses": category_expenses,
                "total_expense": total_expense,
                "budget_status": budget_status,
                "budget_difference": budget_difference,
            }
        )

    except FileNotFoundError:
        return jsonify({"error": "ML models not found. Ensure models3/ exists under backend."}), 503
    except Exception as e:
        return jsonify({"error": str(e)}), 500
