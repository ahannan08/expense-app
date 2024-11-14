# preprocess_data.py

import pandas as pd
from sklearn.model_selection import train_test_split
import joblib

def preprocess_data():
    # Load dataset
    df = pd.read_csv('dataset3/expense_data_v2.csv')  # Adjust path as needed

    # Manual encoding for ordered levels
    food_level_mapping = {'Low': 1, 'Medium': 2, 'High': 0}
    entertainment_level_mapping = {'Low': 1, 'High': 0}

    # Map levels to ordered numerical values
    df['food_level'] = df['food_level'].map(food_level_mapping)
    df['entertainment_level'] = df['entertainment_level'].map(entertainment_level_mapping)

    # Initialize LabelEncoder for other categorical columns
    df['month_type'] = df['month_type'].astype('category').cat.codes
    df['category'] = df['category'].astype('category').cat.codes

    # Define feature and target columns
    X = df[['month', 'category', 'month_type', 'food_level', 'entertainment_level']]
    y = df['expense_amount']

    # Split into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Save preprocessed data
    X_train.to_csv('dataset3/X_train.csv', index=False)
    X_test.to_csv('dataset3/X_test.csv', index=False)
    y_train.to_csv('dataset3/y_train.csv', index=False)
    y_test.to_csv('dataset3/y_test.csv', index=False)

    print("Data preprocessing complete, files saved for model training.")

# Run preprocessing
if __name__ == "__main__":
    preprocess_data()
