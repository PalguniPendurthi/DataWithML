import pandas as pd

data = pd.read_csv('uncleaned_dataset.csv')

# Create a DataFrame
df = pd.DataFrame(data)

# Filter valid records based on height and alcohol consumption
valid_height = df['Height_(cm)'].between(63, 248)
valid_alcohol = df['Alcohol_Consumption'].between(0, 30)

# Filter records with no missing values
no_missing_values = df.notnull().all(axis=1)

# Create a mask for rows that should be considered normal
valid_records = valid_height & valid_alcohol & no_missing_values

# Separate the data into normal and abnormal
clean_data = df[valid_records]
abnormal_data = df[~valid_records]

# Save to CSV
clean_data.to_csv('clean.csv', index=False)
abnormal_data.to_csv('abnormal.csv', index=False)

# Output the first few rows of the clean and abnormal data for inspection
# clean_data.head(), abnormal_data.head()