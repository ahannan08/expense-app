from datetime import datetime

from flask import Blueprint, jsonify, request

from extensions import db
from models.Prediction import Prediction

predictions_bp = Blueprint("predictions", __name__)


def _category_column_map():
    return {
        "Food": "food",
        "Entertainment": "entertainment",
        "Sports": "sports",
        "Shopping": "shopping",
        "Gym": "gym",
        "Petrol": "petrol",
        "Travel": "travel",
        "Snacks": "snacks",
        "Misc": "misc",
    }


@predictions_bp.route("/save-prediction", methods=["POST"])
def save_prediction():
    try:
        data = request.get_json() or {}
        month = data.get("month")
        year = data.get("year", datetime.now().year)
        budget = data.get("budget", 0)
        total_expense = data.get("total_expense")
        category_expenses = data.get("category_expenses")
        budget_status = data.get("budget_status")

        if not all([month, budget, total_expense, category_expenses, budget_status]):
            return jsonify({"error": "Missing required fields"}), 400

        existing_prediction = Prediction.query.filter_by(month=month, year=year).first()

        if existing_prediction:
            return jsonify(
                {
                    "error": "Prediction for this month already exists. Use the update endpoint instead."
                }
            ), 409

        new_prediction = Prediction(
            month=month,
            year=year,
            budget=data["budget"],
            total_expense=total_expense,
            budget_status=budget_status,
            food=category_expenses.get("Food", 0),
            entertainment=category_expenses.get("Entertainment", 0),
            sports=category_expenses.get("Sports", 0),
            shopping=category_expenses.get("Shopping", 0),
            gym=category_expenses.get("Gym", 0),
            petrol=category_expenses.get("Petrol", 0),
            travel=category_expenses.get("Travel", 0),
            snacks=category_expenses.get("Snacks", 0),
            misc=category_expenses.get("Misc", 0),
        )

        db.session.add(new_prediction)
        db.session.commit()
        return jsonify({"message": "Prediction saved successfully.", "prediction": new_prediction.to_dict()})

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@predictions_bp.route("/get-prediction", methods=["GET"])
def get_prediction():
    try:
        month = request.args.get("month")
        year = request.args.get("year")

        if not month or not year:
            return jsonify({"error": "Month and Year are required"}), 400

        prediction = Prediction.query.filter_by(month=int(month), year=int(year)).first()
        if prediction:
            return jsonify(prediction.to_dict())
        return jsonify({"message": "No prediction found for this month and year"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@predictions_bp.route("/update-all-predictions", methods=["POST"])
def update_all_predictions():
    try:
        data = request.get_json()

        if not isinstance(data, list) or not data:
            return jsonify({"error": "Invalid data format. Expected a list of predictions."}), 400

        col_map = _category_column_map()
        updated = 0

        for prediction_data in data:
            month = prediction_data.get("month")
            year = prediction_data.get("year")
            budget = prediction_data.get("budget", 0)
            total_expense = prediction_data.get("total_expense")
            category_expenses = prediction_data.get("category_expenses")
            budget_status = prediction_data.get("budget_status")

            if not all([month, year, budget, total_expense, category_expenses, budget_status]):
                continue

            existing_prediction = Prediction.query.filter_by(month=month, year=year).first()
            confirm_update = prediction_data.get("confirm", False)

            if existing_prediction and confirm_update:
                existing_prediction.budget = budget
                existing_prediction.total_expense = total_expense
                existing_prediction.budget_status = budget_status

                for category, amount in category_expenses.items():
                    col = col_map.get(category, category.lower())
                    if hasattr(existing_prediction, col):
                        setattr(existing_prediction, col, amount)
                updated += 1

        db.session.commit()
        return jsonify(
            {"message": "Predictions processed successfully.", "updated_count": updated}
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
