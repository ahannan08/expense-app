from sklearn.ensemble import RandomForestRegressor
import joblib
import pandas as pd

# List of categories to predict
categories = ['Food', 'Entertainment', 'Sports', 'Shopping', 'Gym', 'Petrol', 'Travel', 'Snacks', 'Misc']

for category in categories:
    # Load the preprocessed data for the category
    X_train = pd.read_csv(f'dataset3/{category}_X_train.csv')
    X_test = pd.read_csv(f'dataset3/{category}_X_test.csv')
    y_train = pd.read_csv(f'dataset3/{category}_y_train.csv').squeeze()  # Convert to 1D array
    y_test = pd.read_csv(f'dataset3/{category}_y_test.csv').squeeze()  # Convert to 1D array

    # Initialize the Random Forest model
    model = RandomForestRegressor(n_estimators=100, random_state=42)

    # Train the model
    model.fit(X_train, y_train)

    # Save the trained model for each category
    joblib.dump(model, f'models3/{category}_model.pkl')

    print(f'Model for {category} trained and saved!')
