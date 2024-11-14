import pandas as pd
import joblib
import numpy as np

# Load the trained model
model = joblib.load('models/expense_model.pkl')

# Load the label encoders used during training
label_encoder_category = joblib.load('models/label_encoder_category.pkl')
label_encoder_month_type = joblib.load('models/label_encoder_month_type.pkl')
label_encoder_food_level = joblib.load('models/label_encoder_food_level.pkl')
label_encoder_entertainment_flag = joblib.load('models/label_encoder_entertainment_flag.pkl')

def handle_unseen_labels(encoder, data, fallback_value=None, is_numeric=False):
    """Handles unseen labels by replacing them with a fallback value."""
    if is_numeric:
        # Handle numeric features
        try:
            data = [float(label) for label in data]
        except ValueError:
            print(f"Encountered non-numeric values: {data}. Substituting with '{fallback_value}'.")
            data = [fallback_value if label in [str(x) for x in encoder.classes_] else float(label) for label in data]
    else:
        # Handle categorical features
        unseen_labels = [label for label in data if label not in encoder.classes_]
        if unseen_labels:
            print(f"Encountered unseen labels: {unseen_labels}. Substituting with '{fallback_value}'.")
        
        # Create a mapping for the unseen labels
        label_map = {label: fallback_value for label in unseen_labels}
        
        # Replace unseen labels with the fallback value
        data = [label_map.get(label, label) for label in data]
    
    # Transform the data using the encoder
    return encoder.transform(data)

def predict_expense(budget, month, food_level, entertainment_flag):
    """Predict the expense based on the provided features."""
    
    # Ensure 'month' is passed as a numeric feature (1 to 12)
    month_encoded = month  # Directly use month as numeric value (1, 2, ..., 12)
    
    # Handle food_level encoding
    food_level = food_level if food_level in ['Low', 'High'] else 'Low'  # Default to 'Low' if invalid
    food_level_encoded = label_encoder_food_level.transform([food_level])[0]
    
    # Handle entertainment_flag encoding
    entertainment_flag_encoded = label_encoder_entertainment_flag.transform([entertainment_flag])[0]
    
    # Prepare features for prediction (remove 'entertainment_expense' from features)
    features = pd.DataFrame({
        'month': [month_encoded],
        'category': [food_level_encoded],  # Encode food_level as 'category'
        'month_type': [month_encoded],  # Using month_type logic from month (if needed)
        'food_level': [food_level_encoded],  # Keep food_level as part of features
        'entertainment_flag': [entertainment_flag_encoded]  # Encode entertainment_flag
    })
    
    # Make the prediction
    predicted_expenses = model.predict(features)
    
    # If you want to add custom logic for entertainment expenses, do it separately
    if entertainment_flag == 'Yes':
        entertainment_expense = 800  # Cap for 'Yes'
    else:
        entertainment_expense = 200  # Cap for 'No'
    
    # Return the predicted expenses and any additional breakdowns
    total_expense = np.sum(predicted_expenses) + entertainment_expense
    return predicted_expenses, total_expense
