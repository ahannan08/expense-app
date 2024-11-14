from flask import Blueprint, request, jsonify
import joblib
import numpy as np

# Initialize the blueprint
category_bp = Blueprint('category', __name__)

# Load the label encoders
label_encoder_food_level = joblib.load('models3/label_encoder_food_level.pkl')
label_encoder_entertainment_level = joblib.load('models3/label_encoder_entertainment_level.pkl')

# List of categories to predict
categories = ['Food', 'Entertainment', 'Sports', 'Shopping', 'Gym', 'Petrol', 'Travel', 'Snacks', 'Misc']

@category_bp.route('/predict-category', methods=['POST'])
def predict_category():
    try:
        # Get the input JSON data
        data = request.get_json()
        print("Received Data:", data)  # Debugging line

        # Extract the input features from the JSON
        budget = data.get('budget')
        month = data.get('month')
        food_level = data.get('food_level')
        entertainment_level = data.get('entertainment_level')

        # Handle missing or incorrect data
        if budget is None or month is None or food_level is None or entertainment_level is None:
            return jsonify({'error': 'Missing required fields'}), 400

        # Map food_level and entertainment_level to numerical values
        food_level_mapping = {'Low': 1, 'Medium': 2, 'High': 0}
        entertainment_mapping = {'Low': 1, 'High': 0}

        food_level_value = food_level_mapping.get(food_level, -1)
        entertainment_value = entertainment_mapping.get(entertainment_level, -1)

        if food_level_value == -1 or entertainment_value == -1:
            return jsonify({'error': 'Invalid food_level or entertainment_level provided'}), 400

        # Prepare the input features for prediction (month, food_level, entertainment_level)
        input_features = np.array([[month, food_level_value, entertainment_value]])

        # Prepare the response dictionary
        category_expenses = {}

        # Predict the expense for each category using its respective model
        for category in categories:
            # Load the model for the current category
            model = joblib.load(f'models3/{category}_model.pkl')

            # Predict the expense for the category
            category_expenses[category] = model.predict(input_features)[0]

        # Calculate the total expense
        total_expense = sum(category_expenses.values())

        # Calculate the budget status
        budget_status = "Under Budget" if total_expense <= budget else "Over Budget"
        budget_difference = budget - total_expense if total_expense <= budget else total_expense - budget

        # Return the response with category predictions and budget status
        response = {
            'category_expenses': category_expenses,
            'total_expense': total_expense,
            'budget_status': budget_status,
            'budget_difference': budget_difference
        }

        return jsonify(response)

    except Exception as e:
        print(f"Error: {e}")  # Print the error message to the console for debugging
        return jsonify({'error': str(e)}), 500
