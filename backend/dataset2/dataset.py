import pandas as pd

# Define the data with fixed lengths for all lists
data = {
    'month': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],  # Fixed length: 24
    'category': ['Food', 'Entertainment', 'Food', 'Shopping', 'Food', 'Entertainment', 'Sports', 'Food', 
                 'Shopping', 'Entertainment', 'Food', 'Entertainment', 'Food', 'Entertainment', 'Food', 'Food', 
                 'Food', 'Entertainment', 'Food', 'Shopping', 'Food', 'Entertainment', 'Food', 'Shopping'],  # Fixed length: 24
    'expense_amount': [1500, 400, 1800, 5000, 3000, 500, 800, 3500, 4500, 600, 4500, 700, 1500, 400, 1800, 5000, 
                       3000, 500, 800, 3500, 4500, 600, 4500, 700],  # Fixed length: 24
    'month_type': ['Regular', 'Regular', 'Regular', 'Vacation', 'Vacation', 'Vacation', 'Holiday', 'Holiday', 
                   'Holiday', 'Holiday', 'Regular', 'Regular', 'Regular', 'Vacation', 'Vacation', 'Vacation', 
                   'Holiday', 'Holiday', 'Holiday', 'Holiday', 'Regular', 'Regular', 'Regular', 'Regular'],  # Fixed length: 24
    'food_level': ['Low', 'High', 'Medium', 'Low', 'High', 'Low', 'Medium', 'High', 'Low', 'Medium', 'High', 'Low', 
                   'Low', 'High', 'Medium', 'Low', 'High', 'Medium', 'Low', 'Low', 'High', 'Medium', 'High', 'Low'],  # Fixed length: 24
    'entertainment_flag': ['Yes', 'No', 'Yes', 'No', 'Yes', 'No', 'Yes', 'No', 'Yes', 'No', 'Yes', 'No', 'Yes', 
                           'No', 'Yes', 'No', 'Yes', 'No', 'Yes', 'No', 'Yes', 'No', 'Yes', 'No']  # Fixed length: 24
}

# Check if all lists have the same length
for key, value in data.items():
    print(f"{key}: {len(value)}")

# Create a DataFrame from the data
df = pd.DataFrame(data)

# Save the DataFrame to a CSV file
csv_file_name = 'expense_data.csv'
df.to_csv(csv_file_name, index=False)

print(f"CSV file '{csv_file_name}' has been generated successfully!")
