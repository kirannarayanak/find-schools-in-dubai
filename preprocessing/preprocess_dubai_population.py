import pandas as pd
import os

# Input and output paths
dataset_path = 'datasets/dubai_pop_2019.csv'
output_path = 'preprocessed_datasets/dubai_pop_2019_cleaned.csv'

# Read the CSV file
df = pd.read_csv(dataset_path)

# Rename columns
df = df.rename(columns={
    'Community Number': 'Community_Number',
    'Community Name': 'Community_Name',
    'Total population': 'Population'
})

# Keep only relevant columns
df = df[['Community_Number', 'Community_Name', 'Population']]

# Remove non-community rows: drop rows where Community_Number or Population is not a number
# (e.g., repeated headers, totals, or missing values)
df = df[pd.to_numeric(df['Community_Number'], errors='coerce').notnull()]
df = df[pd.to_numeric(df['Population'], errors='coerce').notnull()]

# Convert types
df['Community_Number'] = df['Community_Number'].astype(int)
df['Population'] = df['Population'].astype(int)

# Remove rows with empty or null Community_Name
df = df[df['Community_Name'].notnull() & (df['Community_Name'].str.strip() != '')]

# Save cleaned data
os.makedirs(os.path.dirname(output_path), exist_ok=True)
df.to_csv(output_path, index=False)
print(f'Preprocessed data saved to {output_path}') 