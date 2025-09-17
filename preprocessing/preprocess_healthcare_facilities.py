import pandas as pd
import os

# Input and output paths
dataset_path = 'datasets/Sheryan_Facility_Detail.csv'
output_path = 'preprocessed_datasets/Sheryan_Facility_Detail_cleaned.csv'

# Read the CSV file (handle large files efficiently)
df = pd.read_csv(dataset_path, low_memory=False)

# Define keywords to filter for hospitals/clinics
keywords = ['hospital', 'clinic', 'polyclinic']

# Filter rows where facility_category_name_english or facilitysubcategorynameenglish contains relevant keywords
def is_healthcare(row):
    cat = str(row['facility_category_name_english']).lower()
    subcat = str(row['facilitysubcategorynameenglish']).lower()
    return any(k in cat for k in keywords) or any(k in subcat for k in keywords)

filtered = df[df.apply(is_healthcare, axis=1)]

# Select and rename relevant columns
filtered = filtered.rename(columns={
    'f_name_english': 'Facility_Name',
    'x_coordinate': 'Latitude',
    'y_coordinate': 'Longitude',
    'facility_category_name_english': 'Type'
})
filtered = filtered[['Facility_Name', 'Latitude', 'Longitude', 'Type']]

# Drop rows with missing essential values
filtered = filtered.dropna(subset=['Facility_Name', 'Latitude', 'Longitude', 'Type'])

# Save cleaned data
os.makedirs(os.path.dirname(output_path), exist_ok=True)
filtered.to_csv(output_path, index=False)
print(f'Preprocessed data saved to {output_path}') 