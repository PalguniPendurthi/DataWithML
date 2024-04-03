import pandas as pd
input_data = pd.read_csv('uncleaned_dataset.csv')
def row_to_tuple(row):
    tuple_data = (
        row['General_Health'],
        row['Checkup'],
        row['Exercise'],
        row['Heart_Disease'],
        row['Skin_Cancer'],
        row['Other_Cancer'],
        row['Depression'],
        row['Diabetes'],
        row['Arthritis'],
        row['Sex'],
        row['Age_Category'],
        row['Height_(cm)'],
        row['Weight_(kg)'],
        row['BMI'],
        row['Smoking_History'],
        row['Alcohol_Consumption'],
        row['Fruit_Consumption'],
        row['Green_Vegetables_Consumption'],
        row['FriedPotato_Consumption']
    )
    return tuple_data
tuples_list = input_data.apply(row_to_tuple, axis=1).tolist()
#abnormal groups computation
def is_valid_height(height):
    return 63 <= height <= 248

def is_valid_alcohol_consumption(alcohol_consumption):
    return 0 <= alcohol_consumption <= 30

abnormal_groups = []

for tuple_data in tuples_list:
    if not is_valid_height(tuple_data[11]):  
        abnormal_groups.append(tuple_data)
    if not is_valid_alcohol_consumption(tuple_data[15]): 
        abnormal_groups.append(tuple_data)

for group in abnormal_groups:
    print(group)
