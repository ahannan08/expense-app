from flask import Blueprint, jsonify, request

from extensions import db
from models.expense import Expense
from models.Prediction import Prediction

expense_bp = Blueprint("expense_bp", __name__)

DEFAULT_LIMIT = 50
MAX_LIMIT = 100


def _parse_limit_offset():
    limit = request.args.get("limit", DEFAULT_LIMIT, type=int)
    offset = request.args.get("offset", 0, type=int)
    if limit is None or limit < 1:
        limit = DEFAULT_LIMIT
    if limit > MAX_LIMIT:
        limit = MAX_LIMIT
    if offset is None or offset < 0:
        offset = 0
    return limit, offset


@expense_bp.route("/expenses", methods=["POST"])
def save_expense():
    data = request.get_json() or {}
    amount = data.get("amount")
    category = data.get("category")
    month = data.get("month")
    year = data.get("year")

    if not amount or not category or not month or not year:
        return jsonify({"error": "Missing required fields"}), 400

    expense = Expense(
        amount=float(amount),
        category=category,
        month=int(month),
        year=int(year),
    )

    try:
        db.session.add(expense)
        db.session.commit()
        return jsonify({"message": "Expense saved successfully", "expense": expense.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@expense_bp.route("/expenses", methods=["GET"])
def list_expenses():
    try:
        month = request.args.get("month", type=int)
        year = request.args.get("year", type=int)
        limit, offset = _parse_limit_offset()

        query = Expense.query.order_by(Expense.created_at.desc())
        if month is not None:
            query = query.filter_by(month=month)
        if year is not None:
            query = query.filter_by(year=year)

        expenses = query.limit(limit).offset(offset).all()
        return jsonify([e.to_dict() for e in expenses]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@expense_bp.route("/x", methods=["GET"])
def get_all_expenses_legacy():
    """Deprecated: use GET /api/expenses"""
    return list_expenses()


@expense_bp.route("/expenses/monthly-summary", methods=["GET"])
def get_monthly_expenses():
    month = request.args.get("month", type=int)
    year = request.args.get("year", type=int)

    if not month or not year:
        return jsonify({"error": "Month and year are required"}), 400

    category_summary = {
        "Food": 0,
        "Sports": 0,
        "Shopping": 0,
        "Travel": 0,
        "Misc": 0,
        "Snacks": 0,
        "Petrol": 0,
        "Gym": 0,
        "Entertainment": 0,
    }
    total_expense = 0

    expenses = Expense.query.filter_by(month=month, year=year).all()

    for expense in expenses:
        total_expense += expense.amount
        category_cleaned = expense.category.strip("{}").strip('"')

        if category_cleaned in category_summary:
            category_summary[category_cleaned] += expense.amount
        else:
            category_summary[category_cleaned] = expense.amount

    return jsonify(
        {
            "total_expense": total_expense,
            "category_expenses": category_summary,
        }
    )


@expense_bp.route("/dashboard", methods=["GET"])
def dashboard():
    try:
        expense_limit = request.args.get("expense_limit", 15, type=int)
        prediction_limit = request.args.get("prediction_limit", 10, type=int)
        if expense_limit is None or expense_limit < 1:
            expense_limit = 15
        if prediction_limit is None or prediction_limit < 1:
            prediction_limit = 10
        expense_limit = min(expense_limit, MAX_LIMIT)
        prediction_limit = min(prediction_limit, MAX_LIMIT)

        recent_expenses = (
            Expense.query.order_by(Expense.created_at.desc()).limit(expense_limit).all()
        )
        recent_predictions = (
            Prediction.query.order_by(
                Prediction.year.desc(),
                Prediction.month.desc(),
                Prediction.created_at.desc(),
            )
            .limit(prediction_limit)
            .all()
        )

        return jsonify(
            {
                "recent_expenses": [e.to_dict() for e in recent_expenses],
                "recent_predictions": [p.to_dict() for p in recent_predictions],
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500
