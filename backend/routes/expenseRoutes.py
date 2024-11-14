from flask import Blueprint, request, jsonify
from extensions import db
from models.expense import Expense
import datetime

# Create a Blueprint for expense routes
expense_bp = Blueprint('expense_bp', __name__)

# Route to save expenses
@expense_bp.route('/expenses', methods=['POST'])
def save_expense():
    data = request.get_json()
    amount = data.get('amount')
    category = data.get('category')
    month = data.get('month')
    year = data.get('year')

    # Validate the data (e.g., check for required fields)
    if not amount or not category or not month or not year:
        return jsonify({'error': 'Missing required fields'}), 400

    # Create a new Expense record
    expense = Expense(amount=amount, category=category, month=month, year=year)

    try:
        # Add and commit the expense to the database
        db.session.add(expense)
        db.session.commit()
        return jsonify({'message': 'Expense saved successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@expense_bp.route('/expenses/monthly-summary', methods=['GET'])
def get_monthly_expenses():
    month = request.args.get('month', type=int)
    year = request.args.get('year', type=int)

    if not month or not year:
        return jsonify({'error': 'Month and year are required'}), 400

    # Initialize the summary dictionary with all categories set to 0
    category_summary = {
        'Food': 0,
        'Sports': 0,
        'Shopping': 0,
        'Travel': 0,
        'Misc': 0,
        'Snacks': 0,
        'Petrol': 0,
        'Gym': 0,
        'Entertainment': 0,
    }
    total_expense = 0

    # Query to get expenses for the specified month and year
    expenses = Expense.query.filter_by(month=month, year=year).all()

    for expense in expenses:
        total_expense += expense.amount
        # Clean up the category string by stripping out extra characters like {} and ""
        category_cleaned = expense.category.strip("{}").strip('"')

        # If the cleaned category exists in the summary, add the amount to it
        if category_cleaned in category_summary:
            category_summary[category_cleaned] += expense.amount
        else:
            category_summary[category_cleaned] = expense.amount  # In case of unexpected categories

    # Return the structured response with all categories
    return jsonify({
        'total_expense': total_expense,
        'category_expenses': category_summary
    })



# New route to retrieve all expenses with detailed info
@expense_bp.route('/x', methods=['GET'])
def get_all_expenses():
    try:
        expenses = Expense.query.all()  # Fetch all expense records from the database
        expense_list = []

        # Convert each expense record to a dictionary format
        for expense in expenses:
            expense_data = {
                'amount': expense.amount,
                'category': expense.category,
                'month': expense.month,
                'year': expense.year
            }
            expense_list.append(expense_data)

        return jsonify(expense_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
