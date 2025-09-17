import pandas as pd
import os

# Input and output paths
dataset_path = 'datasets/metro_venues_total.csv'
output_path = 'preprocessed_datasets/metro_venues_total_cleaned.csv'

# Read the CSV file
df = pd.read_csv(dataset_path)

# Select and rename relevant columns
df = df.rename(columns={
    'station_name': 'Station',
    'latitude': 'Latitude',
    'longitude': 'Longitude',
    'category_name': 'Venue_Category'
})

# Keep only necessary columns
df = df[['Station', 'Latitude', 'Longitude', 'Venue_Category']]

# Remove duplicates
df = df.drop_duplicates()

# Save cleaned data
os.makedirs(os.path.dirname(output_path), exist_ok=True)
df.to_csv(output_path, index=False)
print(f'Preprocessed data saved to {output_path}') 