import pandas as pd
from collections import defaultdict

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
cleaned_data = df[valid_records]
abnormal_data = df[~valid_records]

# Save to CSV
cleaned_data.to_csv('clean.csv', index=False)
abnormal_data.to_csv('abnormal.csv', index=False)

# Load the clean and dirty dataset
clean_data = pd.read_csv('clean.csv')
abnormal_data = pd.read_csv('abnormal.csv')

# Define data quality rules
rules = [
    # Rule 1: 'Depression', 'BMI', and 'Alcohol_Consumption' should not have missing values.
    "Depression(x, d) => d != ''",
    "BMI(x, b) => b != ''",
    "Alcohol_Consumption(x, a) => a != ''",
    
    # Rule 2: 'Sex' should be either 'Male' or 'Female'.
    "Sex(x, s) => s == 'Male' || s == 'Female'",
    
    # Rule 3: 'Age_Category' should be in the format 'XX-XX'.
    "Age_Category(x, a) => match(a, '\\d{2}-\\d{2}')",
    
    # Rule 4: 'Checkup' should start with an uppercase 'W'.
    "Checkup(x, c) => match(c, '^W.*')",
    
    # Rule 5: 'Height_(cm)' should be within a valid range (e.g., 50 to 250).
    "Height_cm(x, h) => h >= 50 && h <= 250",
    
    # Rule 6: 'Weight_(kg)' should be within a valid range (e.g., 30 to 200).
    "Weight_kg(x, w) => w >= 30 && w <= 200",
    
    # Rule 7: 'FriedPotato_Consumption' should be non-negative.
    "FriedPotato_Consumption(x, f) => f >= 0"
]

# Transform the dataset into a standard form with a set of tuples
clean_tuples = []
for _, row in clean_data.iterrows():
    tuple_data = {
        'Depression': row['Depression'],
        'BMI': row['BMI'],
        'Alcohol_Consumption': row['Alcohol_Consumption'],
        'Sex': row['Sex'],
        'Age_Category': row['Age_Category'],
        'Checkup': row['Checkup'],
        'Height_cm': row['Height_(cm)'],
        'Weight_kg': row['Weight_(kg)'],
        'FriedPotato_Consumption': row['FriedPotato_Consumption']
    }
    clean_tuples.append(tuple_data)

abnormal_tuples = []
for _, row in abnormal_data.iterrows():
    tuple_data = {
        'Depression': row['Depression'],
        'BMI': row['BMI'],
        'Alcohol_Consumption': row['Alcohol_Consumption'],
        'Sex': row['Sex'],
        'Age_Category': row['Age_Category'],
        'Checkup': row['Checkup'],
        'Height_cm': row['Height_(cm)'],
        'Weight_kg': row['Weight_(kg)'],
        'FriedPotato_Consumption': row['FriedPotato_Consumption']
    }
    abnormal_tuples.append(tuple_data)

# Transform data quality rules into MLN rules
mln_rules = []
for rule in rules:
    # Split the rule into reason and result parts
    reason, result = rule.split('=>')
    # Remove unnecessary whitespace
    reason = reason.strip()
    result = result.strip()
    # Create an MLN rule
    mln_rule = f"{reason} => {result}"
    mln_rules.append(mln_rule)

# Print the transformed dataset and MLN rules
print("Transformed Dataset:")


print("\nMLN Rules:")
for mln_rule in mln_rules:
    print(mln_rule)

# MLN index construction
def construct_mln_index(tuples, mln_rules):
    mln_index = defaultdict(lambda: defaultdict(list))

    for rule_idx, mln_rule in enumerate(mln_rules):
        reason, _ = mln_rule.split('=>')
        reason = reason.strip()

        for tuple_data in tuples:
            # Extract the values from the tuple based on the reason part
            reason_values = tuple(tuple_data[attr.split('(')[0]] for attr in reason.split('&&'))

            # Create a γ (piece of data) with the reason values
            gamma = {attr.split('(')[0]: value for attr, value in zip(reason.split('&&'), reason_values)}

            # Add the γ to the corresponding group in the block
            mln_index[rule_idx][tuple(reason_values)].append(gamma)

    return mln_index

# Construct the MLN index
mln_index = construct_mln_index(clean_tuples, mln_rules)

print("\nMLN Index:")
for block_idx, block in mln_index.items():
    print(f"Block {block_idx} (Rule: {mln_rules[block_idx]})")
    for group_idx, group in enumerate(block.values()):
        gammas = ", ".join([f"γ: {gamma}" for gamma in group])
        print(f"  Group {group_idx} with gammas: [{gammas}]")
            
# Print the MLN index
def process_abnormal_groups(mln_index):
    for block_idx, block in mln_index.items():
        normal_groups = []
        abnormal_groups = []

        # Identify normal and abnormal groups
        for group_idx, group in enumerate(block.values()):
            is_abnormal = False
            for gamma in group:
                if any(value == '' for value in gamma.values()):
                    is_abnormal = True
                    break
            if is_abnormal:
                abnormal_groups.append((group_idx, group))
            else:
                normal_groups.append((group_idx, group))

        # Merge abnormal groups with their most similar normal group
        for abnormal_group_idx, abnormal_group in abnormal_groups:
            most_similar_group_idx = None
            max_similarity = 0

            for normal_group_idx, normal_group in normal_groups:
                similarity = calculate_similarity(abnormal_group, normal_group)
                if similarity > max_similarity:
                    max_similarity = similarity
                    most_similar_group_idx = normal_group_idx

            if most_similar_group_idx is not None:
                # Merge the abnormal group with the most similar normal group
                mln_index[block_idx][normal_groups[most_similar_group_idx][0]] += abnormal_group
                del mln_index[block_idx][abnormal_group_idx]

    return mln_index

def calculate_similarity(group1, group2):
    # Calculate the similarity between two groups
    # You can implement your own similarity metric here
    # For example, you can use Jaccard similarity or cosine similarity
    # based on the values of the γs in each group
    # This is just a placeholder implementation
    return len(set(group1) & set(group2)) / len(set(group1) | set(group2))

# Process abnormal groups
mln_index = process_abnormal_groups(mln_index)

# Print the updated MLN index after processing abnormal groups
def clean_multiple_versions(mln_index):
    cleaned_versions = defaultdict(dict)

    for block_idx, block in mln_index.items():
        for group_idx, group in enumerate(block.values()):
            if len(group) > 1:
                # Clean dirty values within the group
                clean_gamma = max(group, key=lambda x: calculate_reliability_score(x))
                cleaned_versions[block_idx][group_idx] = clean_gamma
            else:
                cleaned_versions[block_idx][group_idx] = group[0]

    return cleaned_versions

def calculate_reliability_score(gamma):
    # Calculate the reliability score for a γ
    # You can implement your own reliability score calculation logic here
    # For example, you can consider factors such as the completeness of the data,
    # the consistency with other data pieces, or external knowledge
    # This is just a placeholder implementation
    return sum(1 for value in gamma.values() if value != '')

# Clean multiple data versions
cleaned_versions = clean_multiple_versions(mln_index)
def regenerate_values(attr, tuple_data, cleaned_versions):
    # Regenerate values for a conflicting attribute
    # You can implement your own logic here based on the specific requirements
    # This is just a placeholder implementation
    regenerated_values = set()
    for block in cleaned_versions.values():
        for gamma in block.values():
            if gamma.get(attr) is not None:
                regenerated_values.add(gamma[attr])
    return list(regenerated_values)

def calculate_fusion_score(value, cleaned_versions):
    # Calculate the fusion score for a regenerated value
    # You can implement your own fusion score calculation logic here
    # This is just a placeholder implementation
    score = 0
    for block in cleaned_versions.values():
        for gamma in block.values():
            if value in gamma.values():
                score += 1
    return score
# Print the cleaned data versions
def derive_unified_data(cleaned_versions, tuples):
    unified_data = []

    for tuple_data in tuples:
        conflicting_attributes = defaultdict(set)

        # Detect conflicting values across different data versions
        for block in cleaned_versions.values():
            for group_idx, gamma in block.items():
                for attr, value in gamma.items():
                    if attr in tuple_data and tuple_data[attr] != value:
                        conflicting_attributes[attr].add(value)

        # Regenerate values for conflicting attributes
        regenerated_tuple = tuple_data.copy()
        for attr, values in conflicting_attributes.items():
            if len(values) > 1:
                regenerated_values = regenerate_values(attr, tuple_data, cleaned_versions)
                regenerated_tuple[attr] = max(regenerated_values, key=lambda x: calculate_fusion_score(x, cleaned_versions))

        unified_data.append(regenerated_tuple)

    return unified_data
# Derive the unified clean data
unified_data = derive_unified_data(cleaned_versions, clean_tuples)

# Print the unified clean data
print("\nUnified Clean Data:")
for tuple_data in unified_data:
    print(tuple_data)

