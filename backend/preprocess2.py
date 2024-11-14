import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib

def preprocess_data():
    # Load the dataset
    df = pd.read_csv('dataset/expense_data.csv')
    
    # Initialize LabelEncoders
    label_encoder_category = LabelEncoder()
    label_encoder_month_type = LabelEncoder()
    label_encoder_food_level = LabelEncoder()
    label_encoder_entertainment_flag = LabelEncoder()
    
    # Encode each categorical column
    df['category'] = label_encoder_category.fit_transform(df['category'])
    df['month'] = df['month'].astype(int)  # Keep the month as a numeric value, no need for label encoding 
    df['month_type'] = label_encoder_month_type.fit_transform(df['month_type'])  # Encoding for month_type
    df['food_level'] = label_encoder_food_level.fit_transform(df['food_level'])
    df['entertainment_flag'] = label_encoder_entertainment_flag.fit_transform(df['entertainment_flag'])
    
    # Save the encoders for use during prediction
    joblib.dump(label_encoder_category, 'models/label_encoder_category.pkl')
    joblib.dump(label_encoder_month_type, 'models/label_encoder_month_type.pkl')
    joblib.dump(label_encoder_food_level, 'models/label_encoder_food_level.pkl')
    joblib.dump(label_encoder_entertainment_flag, 'models/label_encoder_entertainment_flag.pkl')
    
    # Define features (X) and target variable (y)
    X = df[['month', 'category', 'month_type', 'food_level', 'entertainment_flag']]
    y = df['expense_amount']
    
    # Step 1: Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Step 2: Save the split data into CSV files
    X_train.to_csv('dataset2/X_train.csv', index=False)
    X_test.to_csv('dataset2/X_test.csv', index=False)
    y_train.to_csv('dataset2/y_train.csv', index=False)
    y_test.to_csv('dataset2/y_test.csv', index=False)

    print("Data preprocessing complete and files saved!")

# Run the preprocessing function
if __name__ == "__main__":
    preprocess_data()
