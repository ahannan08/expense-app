import pandas as pd

# Define the data
data = {
    'month': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    'category': ['Food', 'Entertainment', 'Food', 'Shopping', 'Food', 'Entertainment', 'Sports', 'Food', 'Shopping', 'Entertainment', 'Food', 'Entertainment'],
    'expense_amount': [1500, 400, 1800, 5000, 3000, 500, 800, 3500, 4500, 600, 4500, 700],
    'month_type': ['Regular', 'Regular', 'Regular', 'Vacation', 'Vacation', 'Vacation', 'Holiday', 'Holiday', 'Holiday', 'Holiday', 'Regular', 'Regular'],
    'food_level': ['Low', 'High', 'Medium', 'Low', 'High', 'Low', 'Medium', 'High', 'Low', 'Medium', 'High', 'Low'],
    'entertainment_flag': ['Yes', 'No', 'Yes', 'No', 'Yes', 'No', 'Yes', 'No', 'Yes', 'No', 'Yes', 'No']
}

# Create a DataFrame from the data
df = pd.DataFrame(data)

# Save the DataFrame to a CSV file
csv_file_name = 'dataset/expense_data.csv'
df.to_csv(csv_file_name, index=False)

print(f"CSV file '{csv_file_name}' has been generated successfully!")
