import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import joblib

def train_model():
    # Load the training and testing data
    X_train = pd.read_csv('dataset/X_train.csv')
    X_test = pd.read_csv('dataset/X_test.csv')
    y_train = pd.read_csv('dataset/y_train.csv')
    y_test = pd.read_csv('dataset/y_test.csv')

    # Initialize and train the model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Save the trained model
    joblib.dump(model, 'models/expense_model.pkl')

    # Make predictions on the test set
    y_pred = model.predict(X_test)

    # Evaluate the model
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"Mean Squared Error: {mse}")
    print(f"R-squared: {r2}")

# Run the training function
if __name__ == "__main__":
    train_model()
