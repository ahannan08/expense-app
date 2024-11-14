import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib

def train_model():
    # Load the preprocessed data (X_train, X_test, y_train, y_test)
    X_train = pd.read_csv('dataset2/X_train.csv')
    X_test = pd.read_csv('dataset2/X_test.csv')
    y_train = pd.read_csv('dataset2/y_train.csv')
    y_test = pd.read_csv('dataset2/y_test.csv')
    
    # Initialize the model (RandomForestRegressor, you can change it if needed)
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    
    # Train the model
    model.fit(X_train, y_train)
    
    # Make predictions on the test set
    y_pred = model.predict(X_test)
    
    # Evaluate the model
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    # Print evaluation metrics
    print(f"Mean Squared Error: {mse}")
    print(f"R-squared: {r2}")
    
    # Save the trained model
    joblib.dump(model, 'models/expense_model.pkl')
    
    print("Model training complete and saved as 'expense_model.pkl'.")

# Run the train_model function
if __name__ == "__main__":
    train_model()
