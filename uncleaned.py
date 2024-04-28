import pandas as pd
import random
import numpy as np

# Load the clean dataset
clean_data = pd.read_csv('original_dataset.csv')

# Create a copy of the clean dataset
dirty_data = clean_data.copy()

# Introduce missing values
columns_to_modify = ['Depression', 'BMI', 'Alcohol_Consumption']
for column in columns_to_modify:
    dirty_data[column] = dirty_data[column].astype(str)
    num_missing = int(len(dirty_data) * 0.1)  # Introduce 10% missing values
    missing_indices = random.sample(range(len(dirty_data)), num_missing)
    dirty_data.loc[missing_indices, column] = ''

# Introduce typos and inconsistent values
columns_to_modify = ['Sex', 'Age_Category', 'Checkup']
for column in columns_to_modify:
    num_errors = int(len(dirty_data) * 0.1)  # Introduce errors in 5% of the rows
    error_indices = random.sample(range(len(dirty_data)), num_errors)
    for index in error_indices:
        if column == 'Sex':
            dirty_data.at[index, column] = 'Femle' if dirty_data.at[index, column] == 'Female' else 'ale'
        elif column == 'Age_Category':
            dirty_data.at[index, column] = dirty_data.at[index, column].replace('-', '')
        elif column == 'Checkup':
            dirty_data.at[index, column] = dirty_data.at[index, column].replace('W', 'w')

# Introduce invalid values
columns_to_modify = ['Height_(cm)', 'Weight_(kg)', 'FriedPotato_Consumption']
for column in columns_to_modify:
    num_invalid = int(len(dirty_data) * 0.05)  # Introduce invalid values in 2% of the rows
    invalid_indices = random.sample(range(len(dirty_data)), num_invalid)
    for index in invalid_indices:
        if column == 'Height_(cm)':
            dirty_data.at[index, column] = random.choice([0, 1000])
        elif column == 'Weight_(kg)':
            dirty_data.at[index, column] = random.choice([0, 500])
        elif column == 'FriedPotato_Consumption':
            dirty_data.at[index, column] = random.choice([-10, 100])

# Save the dirty dataset
dirty_data.to_csv('dirty_dataset.csv', index=False)