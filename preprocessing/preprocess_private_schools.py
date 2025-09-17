import pandas as pd
import os

# Input and output paths
dataset_path = 'datasets/Private-Schools_Database_-(English).xlsx'
output_path = 'preprocessed_datasets/Private-Schools_Database_-(English)_cleaned.csv'

# Read the Excel file, using the second row as header (skip first row)
df = pd.read_excel(dataset_path, header=1)

# Standardize column names (strip, lower, replace spaces with underscores)
def clean_col(col):
    return col.strip().lower().replace(' ', '_').replace('-', '_')
df.columns = [clean_col(col) for col in df.columns]

# Print columns for reference
print('Columns after cleaning:', df.columns.tolist())

# Guess relevant columns (adjust as needed)
relevant_cols = [
    'school_name', 'location', 'curriculum', 'rating',
    'latitude', 'longitude', 'grades_2014_15', 'students_2014_15',
    'year_established_in_dubai', 'type_of_school'
]
# Keep only columns that exist in the DataFrame
relevant_cols = [col for col in relevant_cols if col in df.columns]
df = df[relevant_cols]

# Drop rows with missing essential values (school_name, latitude, longitude)
essential = [col for col in ['school_name', 'latitude', 'longitude'] if col in df.columns]
df = df.dropna(subset=essential)

# Normalize coordinates to float if present
for col in ['latitude', 'longitude']:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

# Drop rows again if lat/lon couldn't be converted
if 'latitude' in df.columns and 'longitude' in df.columns:
    df = df.dropna(subset=['latitude', 'longitude'])

# Save cleaned data
os.makedirs(os.path.dirname(output_path), exist_ok=True)
df.to_csv(output_path, index=False)
print(f'Preprocessed data saved to {output_path}') 