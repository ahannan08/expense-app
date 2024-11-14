# routes/predictionDb.py
from flask import Blueprint, request, jsonify
from datetime import datetime
from models.Prediction import Prediction  # Updated import
from extensions import db

predictions_bp = Blueprint('predictions', __name__)

@predictions_bp.route('/save-prediction', methods=['POST'])
def save_prediction():
    try:
        data = request.get_json()
        month = data.get('month')
        budget = data.get('budget', 0)  # Use 0 if budget is None
        total_expense = data.get('total_expense')
        category_expenses = data.get('category_expenses')
        budget_status = data.get('budget_status')

        if not all([month, budget, total_expense, category_expenses, budget_status]):
            return jsonify({'error': 'Missing required fields'}), 400

        current_year = datetime.now().year
        existing_prediction = Prediction.query.filter_by(
            month=month, 
            year=current_year
        ).first()

        # If an existing prediction is found, return an error message instead of updating
        if existing_prediction:
            return jsonify({"error": "Prediction for this month already exists. Use the update endpoint instead."}), 409

        # Create new prediction
        new_prediction = Prediction(
            month=month,
            year=current_year,
            budget=data['budget'],  # This should be data['budget']
            total_expense=total_expense,
            budget_status=budget_status,
            food=category_expenses.get('Food', 0),
            entertainment=category_expenses.get('Entertainment', 0),
            sports=category_expenses.get('Sports', 0),
            shopping=category_expenses.get('Shopping', 0),
            gym=category_expenses.get('Gym', 0),
            petrol=category_expenses.get('Petrol', 0),
            travel=category_expenses.get('Travel', 0),
            snacks=category_expenses.get('Snacks', 0),
            misc=category_expenses.get('Misc', 0)
        )

        db.session.add(new_prediction)
        db.session.commit()
        return jsonify({"message": "Prediction saved successfully."})

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
 
 
 
 
 
 
 

# Retrieve a prediction for a given month and year
@predictions_bp.route('/get-prediction', methods=['GET'])
def get_prediction():
    try:
        # Get month and year from query parameters
        month = request.args.get('month')
        year = request.args.get('year')

        if not month or not year:
            return jsonify({'error': 'Month and Year are required'}), 400

        prediction = Prediction.query.filter_by(month=month, year=year).first()
        if prediction:
            return jsonify({
                'month': prediction.month,
                'year': prediction.year,
                'category_expenses': {
                    'Food': prediction.food,
                    'Entertainment': prediction.entertainment,
                    'Sports': prediction.sports,
                    'Shopping': prediction.shopping,
                    'Gym': prediction.gym,
                    'Petrol': prediction.petrol,
                    'Travel': prediction.travel,
                    'Snacks': prediction.snacks,
                    'Misc': prediction.misc,
                },
                'total_expense': prediction.total_expense,
                'budget_status': prediction.budget_status
            })
        else:
            return jsonify({'message': 'No prediction found for this month and year'}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500







@predictions_bp.route('/update-all-predictions', methods=['POST'])
def update_all_predictions():
    try:
        # Get the list of predictions to update
        data = request.get_json()

        # Ensure the data is an array of predictions
        if not isinstance(data, list) or not data:
            return jsonify({"error": "Invalid data format. Expected a list of predictions."}), 400

        # Iterate through each prediction and update the corresponding record
        for prediction_data in data:
            month = prediction_data.get('month')
            year = prediction_data.get('year')
            budget = prediction_data.get('budget', 0)
            total_expense = prediction_data.get('total_expense')
            category_expenses = prediction_data.get('category_expenses')
            budget_status = prediction_data.get('budget_status')

            # Check if all necessary data is present for each prediction
            if not all([month, year, budget, total_expense, category_expenses, budget_status]):
                continue  # Skip this entry if any required fields are missing

            # Find the existing prediction in the database
            existing_prediction = Prediction.query.filter_by(month=month, year=year).first()

            if existing_prediction:
                # If prediction exists, we simulate a user confirmation to update it
                # Since this is a backend, we don't directly prompt the user
                # In a real-world scenario, this could be handled on the frontend (confirmation popup)
                
                # For simplicity, we assume that the frontend handles the user prompt (yes/no)
                # and sends a "confirm" flag with the data

                # In this case, if "confirm" flag is True, we will update the existing prediction.
                confirm_update = prediction_data.get('confirm', False)

                if confirm_update:
                    # Update existing prediction
                    existing_prediction.budget = budget
                    existing_prediction.total_expense = total_expense
                    existing_prediction.budget_status = budget_status

                    # Update category expenses
                    for category, amount in category_expenses.items():
                        setattr(existing_prediction, category.lower(), amount)

                    # Commit the changes for this prediction
                    db.session.commit()

            else:
                # If no existing prediction is found, do nothing (do not create a new one)
                continue

        return jsonify({"message": "Predictions processed successfully. Updates were made where applicable."})

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
