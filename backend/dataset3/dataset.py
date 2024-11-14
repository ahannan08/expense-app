import pandas as pd
import numpy as np
import random

# Define the range values for each category and condition
expense_ranges = {
    'Food': {
        'Low': (1000, 1300),
        'Medium': (1400, 1900),
        'High': (2000, 2500)
    },
    'Entertainment': {
        'Low': (700, 900),
        'High': (1000, 1500)
    },
    'Sports': (500, 500),
    'Shopping': {
        'Regular': (0, 500),
        'Festival': (5000, 10000)
    },
    'Gym': (2500, 2500),
    'Petrol': (1200, 1600),
    'Travel': {
        'Regular': (200, 200),
        'Vacation': (6000, 10000)
    },
    'Snacks': (800, 1200),
    'Misc': (0, 1200)
}

# Define festival months for Shopping and high Travel months
festival_months = [4, 7, 10, 11, 12]  # April, July, October, November, December
vacation_month = 5  # May

# Generate data
data = {
    'month': [],
    'category': [],
    'expense_amount': [],
    'month_type': [],
    'food_level': [],
    'entertainment_level': []
}

# Loop through each month and category to populate data
for month in range(1, 13):
    month_type = 'Festival' if month in festival_months else ('Vacation' if month == vacation_month else 'Regular')

    # Populate each category expense based on the rules
    for category in expense_ranges.keys():
        # Set default levels
        food_level = random.choice(['Low', 'Medium', 'High']) if category == 'Food' else 'N/A'
        entertainment_level = random.choice(['Low', 'High']) if category == 'Entertainment' else 'N/A'

        # Determine expense based on category and special conditions
        if category == 'Food':
            min_expense, max_expense = expense_ranges['Food'][food_level]
        elif category == 'Entertainment':
            min_expense, max_expense = expense_ranges['Entertainment'][entertainment_level]
        elif category == 'Shopping':
            min_expense, max_expense = expense_ranges['Shopping']['Festival' if month_type == 'Festival' else 'Regular']
        elif category == 'Travel':
            min_expense, max_expense = expense_ranges['Travel']['Vacation' if month_type == 'Vacation' else 'Regular']
        else:
            min_expense, max_expense = expense_ranges[category]

        # Random expense amount within the defined range
        expense_amount = random.randint(min_expense, max_expense)

        # Append to the data dictionary
        data['month'].append(month)
        data['category'].append(category)
        data['expense_amount'].append(expense_amount)
        data['month_type'].append(month_type)
        data['food_level'].append(food_level)
        data['entertainment_level'].append(entertainment_level)

# Create a DataFrame
df = pd.DataFrame(data)

# Save the DataFrame to a CSV file
csv_file_name = 'expense_data_v2.csv'
df.to_csv(csv_file_name, index=False)
print(f"CSV file '{csv_file_name}' has been generated successfully!")
