import pandas as pd
import numpy as np
df = pd.read_csv("uncleaned_dataset1.csv")  
random_rows = np.random.choice(df.index, size=int(len(df) * 0.1), replace=False) 
df.loc[random_rows, random_cols] = np.nan
df['Age_Category'].iloc[0] = '100-104' 
df['Sex'].iloc[2] = 'Unknown'
df['Height_(cm)'].iloc[4] = -150  
df['Alcohol_Consumption'].iloc[6] = 999  
df.to_csv("uncleaned_dataset.csv", index=False)
