import pandas as pd
import re

class MLNIndex:
    def __init__(self, rules):
        self.index = {}
        for rule in rules:
            column = rule['column']
            if column not in self.index:
                self.index[column] = []
            self.index[column].append(rule)

    def get_rules_for_column(self, column):
        return self.index.get(column, [])
    
    def print_index(self):
        for column, rules in self.index.items():
            print(f"Column: {column}")
            for rule in rules:
                print(f"  Rule: {rule['rule']}")

def load_dataset(file_path):
    dataset = pd.read_csv(file_path)
    return dataset

def preprocess_dataset(dataset):
    # Perform any necessary preprocessing steps
    # e.g., handling missing values, converting data types, etc.
    return dataset

# Load the dirty dataset
dirty_dataset = load_dataset('dirty_dataset.csv')

# Preprocess the dataset
preprocessed_dataset = preprocess_dataset(dirty_dataset)

def define_data_quality_rules():
    rules = [
        # Missing Values
        {'column': 'Depression', 'rule': 'lambda x: x != ""'},  # Rule 1
        {'column': 'BMI', 'rule': 'lambda x: pd.notnull(x)'},  # Rule 2
        {'column': 'Alcohol_Consumption', 'rule': 'lambda x: pd.notnull(x)'},  # Rule 3
        
        # Typos and Inconsistent Values
        {'column': 'Sex', 'rule': 'lambda x: x in ["Male", "Female"]'},  # Rule 4
        {'column': 'Age_Category', 'rule': 'lambda x: bool(re.match(r"\\d+-\\d+", x))'},  # Rule 5
        {'column': 'Checkup', 'rule': 'lambda x: bool(re.match(r"(?i)within the past year", str(x)))'},  # Rule 6
        
        # Invalid Values
        {'column': 'Height_(cm)', 'rule': 'lambda x: 100 <= x <= 250'},  # Rule 7
        {'column': 'Weight_(kg)', 'rule': 'lambda x: 30 <= x <= 200'},  # Rule 8
        {'column': 'FriedPotato_Consumption', 'rule': 'lambda x: x >= 0'},  # Rule 9
    ]
    return rules

# Define the data quality rules
data_quality_rules = define_data_quality_rules()

# Initialize MLN index
mln_index = MLNIndex(data_quality_rules)

# Print the MLN index
mln_index.print_index()

