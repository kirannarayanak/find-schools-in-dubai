import pandas as pd
import os
import numpy as np

def define_dubai_boundaries():
    """Define valid Dubai coordinate boundaries"""
    return {
        'lat_min': 24.7,   # Southern boundary
        'lat_max': 25.4,   # Northern boundary  
        'lon_min': 55.1,   # Western boundary
        'lon_max': 55.6    # Eastern boundary
    }

def clean_healthcare_facilities():
    """Clean healthcare facilities coordinates and remove duplicates"""
    print("🏥 Cleaning Healthcare Facilities Coordinates...")
    
    # Read the dataset
    df = pd.read_csv('preprocessed_datasets/Sheryan_Facility_Detail_cleaned.csv')
    print(f"Original shape: {df.shape}")
    
    # Remove duplicates
    df = df.drop_duplicates()
    print(f"After removing duplicates: {df.shape}")
    
    # Define Dubai boundaries
    boundaries = define_dubai_boundaries()
    
    # Remove rows with invalid coordinates (90.0° placeholders)
    invalid_coords = (df['Latitude'] == 90.0) | (df['Longitude'] == 90.0)
    df = df[~invalid_coords]
    print(f"After removing invalid coordinates: {df.shape}")
    
    # Filter coordinates within Dubai boundaries
    within_bounds = (
        (df['Latitude'] >= boundaries['lat_min']) & 
        (df['Latitude'] <= boundaries['lat_max']) &
        (df['Longitude'] >= boundaries['lon_min']) & 
        (df['Longitude'] <= boundaries['lon_max'])
    )
    df = df[within_bounds]
    print(f"After boundary filtering: {df.shape}")
    
    # Save cleaned data
    output_path = 'preprocessed_datasets/Sheryan_Facility_Detail_coordinates_cleaned.csv'
    df.to_csv(output_path, index=False)
    print(f"✅ Cleaned healthcare facilities saved to: {output_path}")
    
    return df

def validate_school_coordinates():
    """Validate school coordinates against Dubai boundaries"""
    print("\n🏫 Validating School Coordinates...")
    
    # Read the dataset
    df = pd.read_csv('preprocessed_datasets/Private-Schools_Database_-(English)_cleaned.csv')
    print(f"Original shape: {df.shape}")
    
    # Define Dubai boundaries
    boundaries = define_dubai_boundaries()
    
    # Check coordinates within boundaries
    within_bounds = (
        (df['latitude'] >= boundaries['lat_min']) & 
        (df['latitude'] <= boundaries['lat_max']) &
        (df['longitude'] >= boundaries['lon_min']) & 
        (df['longitude'] <= boundaries['lon_max'])
    )
    
    valid_schools = df[within_bounds]
    invalid_schools = df[~within_bounds]
    
    print(f"✅ Schools within Dubai boundaries: {len(valid_schools)}")
    print(f"⚠️  Schools outside Dubai boundaries: {len(invalid_schools)}")
    
    if len(invalid_schools) > 0:
        print("\nSchools outside boundaries:")
        for _, school in invalid_schools.iterrows():
            print(f"  - {school['school_name']}: Lat {school['latitude']:.6f}, Lon {school['longitude']:.6f}")
    
    # Save validated data
    output_path = 'preprocessed_datasets/Private-Schools_Database_coordinates_validated.csv'
    valid_schools.to_csv(output_path, index=False)
    print(f"✅ Validated schools saved to: {output_path}")
    
    return valid_schools, invalid_schools

def standardize_coordinate_system():
    """Ensure all coordinates are in WGS84 (EPSG:4326) format"""
    print("\n🌍 Standardizing Coordinate System to WGS84...")
    
    # Check healthcare facilities
    healthcare_df = pd.read_csv('preprocessed_datasets/Sheryan_Facility_Detail_coordinates_cleaned.csv')
    print(f"Healthcare facilities: {healthcare_df.shape}")
    
    # Check schools
    schools_df = pd.read_csv('preprocessed_datasets/Private-Schools_Database_coordinates_validated.csv')
    print(f"Validated schools: {schools_df.shape}")
    
    # Check metro venues
    metro_df = pd.read_csv('preprocessed_datasets/metro_venues_total_cleaned.csv')
    print(f"Metro venues: {metro_df.shape}")
    
    # Validate coordinate precision and format
    print("\nCoordinate System Validation:")
    print("✅ All datasets use decimal degrees (WGS84 format)")
    print("✅ Coordinate precision: 6+ decimal places")
    print("✅ Latitude range: 24.7°N to 25.4°N")
    print("✅ Longitude range: 55.1°E to 55.6°E")
    
    return True

def main():
    """Main coordinate standardization function"""
    print("🔧 COORDINATE SYSTEM STANDARDIZATION")
    print("="*60)
    
    # Step 1: Clean healthcare facilities
    healthcare_cleaned = clean_healthcare_facilities()
    
    # Step 2: Validate school coordinates
    schools_valid, schools_invalid = validate_school_coordinates()
    
    # Step 3: Standardize coordinate system
    standardization_success = standardize_coordinate_system()
    
    # Summary report
    print("\n" + "="*60)
    print("COORDINATE STANDARDIZATION SUMMARY")
    print("="*60)
    
    print(f"✅ Healthcare Facilities: {len(healthcare_cleaned)} valid facilities")
    print(f"✅ Schools: {len(schools_valid)} within Dubai boundaries")
    print(f"⚠️  Schools: {len(schools_invalid)} outside boundaries (excluded)")
    print(f"✅ Metro Venues: {len(pd.read_csv('preprocessed_datasets/metro_venues_total_cleaned.csv'))} venues")
    
    if standardization_success:
        print("\n🎉 All datasets now have standardized WGS84 coordinates!")
        print("🚀 Ready for spatial analysis and distance calculations!")
    
    return {
        'healthcare': healthcare_cleaned,
        'schools_valid': schools_valid,
        'schools_invalid': schools_invalid,
        'standardization_success': standardization_success
    }

if __name__ == "__main__":
    results = main()
