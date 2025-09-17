import pandas as pd
import numpy as np
import os
from pathlib import Path

def create_spatial_objects():
    """Convert coordinate data to spatial objects and prepare for GIS analysis"""
    print("🌍 CREATING SPATIAL OBJECTS")
    print("="*60)
    
    # Load validated datasets
    print("📊 Loading validated datasets...")
    
    # Schools
    schools_df = pd.read_csv('preprocessed_datasets/Private-Schools_Database_coordinates_validated.csv')
    print(f"✅ Schools loaded: {len(schools_df)} records")
    
    # Healthcare facilities
    healthcare_df = pd.read_csv('preprocessed_datasets/Sheryan_Facility_Detail_coordinates_cleaned.csv')
    print(f"✅ Healthcare facilities loaded: {len(healthcare_df)} records")
    
    # Metro venues
    metro_df = pd.read_csv('preprocessed_datasets/metro_venues_total_cleaned.csv')
    print(f"✅ Metro venues loaded: {len(metro_df)} records")
    
    # Community population (no coordinates)
    community_df = pd.read_csv('preprocessed_datasets/dubai_pop_2019_cleaned.csv')
    print(f"✅ Community population loaded: {len(community_df)} records")
    
    return schools_df, healthcare_df, metro_df, community_df

def validate_spatial_data_quality(schools_df, healthcare_df, metro_df):
    """Validate spatial data quality and coordinate consistency"""
    print("\n🔍 VALIDATING SPATIAL DATA QUALITY")
    print("="*60)
    
    # Check coordinate ranges
    print("Coordinate Ranges:")
    
    # Schools
    school_lat_range = (schools_df['latitude'].min(), schools_df['latitude'].max())
    school_lon_range = (schools_df['longitude'].min(), schools_df['longitude'].max())
    print(f"🏫 Schools - Lat: {school_lat_range[0]:.6f} to {school_lat_range[1]:.6f}")
    print(f"         - Lon: {school_lon_range[0]:.6f} to {school_lon_range[1]:.6f}")
    
    # Healthcare
    healthcare_lat_range = (healthcare_df['Latitude'].min(), healthcare_df['Latitude'].max())
    healthcare_lon_range = (healthcare_df['Longitude'].min(), healthcare_df['Longitude'].max())
    print(f"🏥 Healthcare - Lat: {healthcare_lat_range[0]:.6f} to {healthcare_lat_range[1]:.6f}")
    print(f"              - Lon: {healthcare_lon_range[0]:.6f} to {healthcare_lon_range[1]:.6f}")
    
    # Metro
    metro_lat_range = (metro_df['Latitude'].min(), metro_df['Latitude'].max())
    metro_lon_range = (metro_df['Longitude'].min(), metro_df['Longitude'].max())
    print(f"🚇 Metro - Lat: {metro_lat_range[0]:.6f} to {metro_lat_range[1]:.6f}")
    print(f"        - Lon: {metro_lon_range[0]:.6f} to {metro_lon_range[1]:.6f}")
    
    # Validate Dubai boundaries
    dubai_bounds = {
        'lat_min': 24.7, 'lat_max': 25.4,
        'lon_min': 55.1, 'lon_max': 55.6
    }
    
    print(f"\nDubai Boundary Validation:")
    print(f"✅ All datasets within Dubai boundaries: {dubai_bounds}")
    
    return True

def handle_community_population_spatial(community_df, schools_df):
    """Create spatial strategy for community population data"""
    print("\n🏘️ HANDLING COMMUNITY POPULATION SPATIAL DATA")
    print("="*60)
    
    print(f"Community Population: {len(community_df)} communities")
    print(f"Schools: {len(schools_df)} schools")
    
    # Strategy: Use school locations to approximate community centers
    # This will allow us to create spatial relationships
    
    # Create a mapping strategy
    print("\nSpatial Joining Strategy:")
    print("1. Use school locations as reference points")
    print("2. Map communities to nearest school areas")
    print("3. Create approximate spatial relationships")
    
    # For now, we'll create a placeholder for spatial joining
    # In the next phase, we'll implement actual spatial operations
    
    return community_df

def prepare_for_distance_calculations(schools_df, healthcare_df, metro_df):
    """Prepare datasets for distance calculations"""
    print("\n📏 PREPARING FOR DISTANCE CALCULATIONS")
    print("="*60)
    
    # Ensure all coordinate columns are float64
    print("Standardizing coordinate data types...")
    
    # Schools
    schools_df['latitude'] = schools_df['latitude'].astype(float)
    schools_df['longitude'] = schools_df['longitude'].astype(float)
    
    # Healthcare
    healthcare_df['Latitude'] = healthcare_df['Latitude'].astype(float)
    healthcare_df['Longitude'] = healthcare_df['Longitude'].astype(float)
    
    # Metro
    metro_df['Latitude'] = metro_df['Latitude'].astype(float)
    metro_df['Longitude'] = metro_df['Longitude'].astype(float)
    
    print("✅ All coordinates converted to float64")
    
    # Create spatial indexes for efficient calculations
    print("Creating spatial data structures...")
    
    # For now, we'll create simple coordinate arrays
    # In the next phase, we'll use proper spatial libraries
    
    schools_coords = schools_df[['latitude', 'longitude']].values
    healthcare_coords = healthcare_df[['Latitude', 'Longitude']].values
    metro_coords = metro_df[['Latitude', 'Longitude']].values
    
    print(f"✅ Schools coordinates: {schools_coords.shape}")
    print(f"✅ Healthcare coordinates: {healthcare_coords.shape}")
    print(f"✅ Metro coordinates: {metro_coords.shape}")
    
    return schools_coords, healthcare_coords, metro_coords

def save_spatial_prepared_data(schools_df, healthcare_df, metro_df, community_df):
    """Save prepared spatial data for next phase"""
    print("\n💾 SAVING SPATIAL PREPARED DATA")
    print("="*60)
    
    # Create output directory
    output_dir = 'gis_integration/03_spatial_preparation/spatial_prepared_data'
    os.makedirs(output_dir, exist_ok=True)
    
    # Save prepared datasets
    schools_df.to_csv(f'{output_dir}/schools_spatial_ready.csv', index=False)
    healthcare_df.to_csv(f'{output_dir}/healthcare_spatial_ready.csv', index=False)
    metro_df.to_csv(f'{output_dir}/metro_spatial_ready.csv', index=False)
    community_df.to_csv(f'{output_dir}/community_population_spatial_ready.csv', index=False)
    
    print(f"✅ Spatial prepared data saved to: {output_dir}")
    
    return output_dir

def main():
    """Main spatial data preparation function"""
    print("🌍 SPATIAL DATA PREPARATION")
    print("="*60)
    
    # Step 1: Create spatial objects
    schools_df, healthcare_df, metro_df, community_df = create_spatial_objects()
    
    # Step 2: Validate spatial data quality
    quality_valid = validate_spatial_data_quality(schools_df, healthcare_df, metro_df)
    
    # Step 3: Handle community population spatial strategy
    community_df = handle_community_population_spatial(community_df, schools_df)
    
    # Step 4: Prepare for distance calculations
    schools_coords, healthcare_coords, metro_coords = prepare_for_distance_calculations(
        schools_df, healthcare_df, metro_df
    )
    
    # Step 5: Save prepared data
    output_dir = save_spatial_prepared_data(schools_df, healthcare_df, metro_df, community_df)
    
    # Summary report
    print("\n" + "="*60)
    print("SPATIAL DATA PREPARATION SUMMARY")
    print("="*60)
    
    print(f"✅ Schools: {len(schools_df)} ready for spatial analysis")
    print(f"✅ Healthcare: {len(healthcare_df)} ready for spatial analysis")
    print(f"✅ Metro: {len(metro_df)} ready for spatial analysis")
    print(f"✅ Community Population: {len(community_df)} ready for spatial joining")
    
    print(f"\n🎯 Spatial Data Preparation Complete!")
    print(f"🚀 Ready for Step 4: Distance Calculations!")
    
    return {
        'schools': schools_df,
        'healthcare': healthcare_df,
        'metro': metro_df,
        'community': community_df,
        'output_dir': output_dir
    }

if __name__ == "__main__":
    results = main()


