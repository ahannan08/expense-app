import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib

def preprocess_data():
    # Load the dataset
    df = pd.read_csv('dataset/expense_data.csv')
    
    # Initialize LabelEncoders for categorical columns
    label_encoder_category = LabelEncoder()
    label_encoder_month_type = LabelEncoder()
    label_encoder_food_level = LabelEncoder()
    label_encoder_entertainment_flag = LabelEncoder()
    
    # Encode categorical columns (food_level, entertainment_flag, category, month_type)
    df['category'] = label_encoder_category.fit_transform(df['category'])
    df['month'] = df['month'].astype(int)  # Keep 'month' as an integer (no encoding)
    df['food_level'] = label_encoder_food_level.fit_transform(df['food_level'])
    df['entertainment_flag'] = label_encoder_entertainment_flag.fit_transform(df['entertainment_flag'])
    df['month_type'] = label_encoder_month_type.fit_transform(df['month_type'])
    
    # Save the encoders for use during prediction
    joblib.dump(label_encoder_category, 'models/label_encoder_category.pkl')
    joblib.dump(label_encoder_month_type, 'models/label_encoder_month_type.pkl')
    joblib.dump(label_encoder_food_level, 'models/label_encoder_food_level.pkl')
    joblib.dump(label_encoder_entertainment_flag, 'models/label_encoder_entertainment_flag.pkl')
    
    # Define features and target variable
    X = df[['month', 'category', 'month_type', 'food_level', 'entertainment_flag']]
    y = df['expense_amount']
    
    # Split into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Save processed data for model training
    X_train.to_csv('dataset/X_train.csv', index=False)
    X_test.to_csv('dataset/X_test.csv', index=False)
    y_train.to_csv('dataset/y_train.csv', index=False)
    y_test.to_csv('dataset/y_test.csv', index=False)

    print("Data preprocessing complete and files saved!")

# Run the preprocessing function
if __name__ == "__main__":
    preprocess_data()
