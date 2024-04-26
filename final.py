import pandas as pd
column_names = ['General_Health', 'Checkup', 'Exercise', 'Heart_Disease', 'Skin_Cancer', 'Other_Cancer', 'Depression', 'Diabetes', 'Arthritis', 'Sex', 'Age_Category', 'Height_(cm)', 'Weight_(kg)', 'BMI', 'Smoking_History', 'Alcohol_Consumption', 'Fruit_Consumption', 'Green_Vegetables_Consumption', 'FriedPotato_Consumption']

data = pd.read_csv('uncleaned_dataset.csv', delimiter='\t', names=column_names)


# Define data quality rules
# Rule 1: BMI should be non-negative
def rule1(row):
    return row['BMI'] >= 0

# Rule 2: Checkup values should be from a predefined set
valid_checkups = ['Within the past year', 'Within the past 2 years', 'Within the past 5 years', '5 or more years ago']
def rule2(row):
    return row['Checkup'] in valid_checkups

# Rule 3: Heart_Disease and Diabetes should influence General_Health status
def rule3(row):
    if row['Heart_Disease'] == 'Yes' or row['Diabetes'] == 'Yes':
        return row['General_Health'] in ['Fair', 'Poor']
    return True

# Transform rules into MLN format
def transform_rule(rule_func, rule_name):
    for index, row in data.iterrows():
        row_dict = row.to_dict()
        def mln_rule(row_dict):
            if not rule_func(row):
                return f"!{rule_name}(t)"
            return f"{rule_name}(t)"
        return mln_rule

mln_rule1 = transform_rule(rule1, 'BMI_Non_Negative')
mln_rule2 = transform_rule(rule2, 'Valid_Checkup')
mln_rule3 = transform_rule(rule3, 'Health_Consistency')

# Apply MLN rules to dataset
data['MLN_Rule1'] = data.apply(mln_rule1, axis=1)
data['MLN_Rule2'] = data.apply(mln_rule2, axis=1)
data['MLN_Rule3'] = data.apply(mln_rule3, axis=1)

# Save preprocessed data
data.to_csv('preprocessed_health_data.csv', index=False)