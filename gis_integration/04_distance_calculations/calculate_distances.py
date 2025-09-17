import pandas as pd
import numpy as np
import os
from math import radians, cos, sin, asin, sqrt

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    Returns distance in kilometers
    """
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    
    # Radius of earth in kilometers
    r = 6371
    return c * r

def calculate_school_to_healthcare_distances(schools_df, healthcare_df):
    """Calculate distances from each school to all healthcare facilities"""
    print("🏥 Calculating School to Healthcare Distances...")
    
    distances = []
    
    for _, school in schools_df.iterrows():
        school_lat, school_lon = school['latitude'], school['longitude']
        school_name = school['school_name']
        
        # Calculate distances to all healthcare facilities
        for _, facility in healthcare_df.iterrows():
            facility_lat, facility_lon = facility['Latitude'], facility['Longitude']
            facility_name = facility['Facility_Name']
            facility_type = facility['Type']
            
            distance = haversine_distance(school_lat, school_lon, facility_lat, facility_lon)
            
            distances.append({
                'school_name': school_name,
                'facility_name': facility_name,
                'facility_type': facility_type,
                'distance_km': distance,
                'school_lat': school_lat,
                'school_lon': school_lon,
                'facility_lat': facility_lat,
                'facility_lon': facility_lon
            })
    
    distances_df = pd.DataFrame(distances)
    print(f"✅ Calculated {len(distances_df)} school-healthcare distances")
    
    return distances_df

def calculate_school_to_metro_distances(schools_df, metro_df):
    """Calculate distances from each school to all metro stations"""
    print("🚇 Calculating School to Metro Distances...")
    
    distances = []
    
    for _, school in schools_df.iterrows():
        school_lat, school_lon = school['latitude'], school['longitude']
        school_name = school['school_name']
        
        # Calculate distances to all metro stations
        for _, metro in metro_df.iterrows():
            metro_lat, metro_lon = metro['Latitude'], metro['Longitude']
            station_name = metro['Station']
            venue_category = metro['Venue_Category']
            
            distance = haversine_distance(school_lat, school_lon, metro_lat, metro_lon)
            
            distances.append({
                'school_name': school_name,
                'metro_station': station_name,
                'venue_category': venue_category,
                'distance_km': distance,
                'school_lat': school_lat,
                'school_lon': school_lon,
                'metro_lat': metro_lat,
                'metro_lon': metro_lon
            })
    
    distances_df = pd.DataFrame(distances)
    print(f"✅ Calculated {len(distances_df)} school-metro distances")
    
    return distances_df

def create_enriched_school_profiles(schools_df, healthcare_distances, metro_distances):
    """Create enriched school profiles with proximity metrics"""
    print("🏫 Creating Enriched School Profiles...")
    
    enriched_profiles = []
    
    for _, school in schools_df.iterrows():
        school_name = school['school_name']
        
        # Get healthcare distances for this school
        school_healthcare = healthcare_distances[healthcare_distances['school_name'] == school_name]
        
        # Get metro distances for this school
        school_metro = metro_distances[metro_distances['school_name'] == school_name]
        
        # Calculate proximity metrics
        nearest_healthcare = school_healthcare.loc[school_healthcare['distance_km'].idxmin()]
        nearest_metro = school_metro.loc[school_metro['distance_km'].idxmin()]
        
        # Count facilities within different distance ranges
        healthcare_within_1km = len(school_healthcare[school_healthcare['distance_km'] <= 1.0])
        healthcare_within_2km = len(school_healthcare[school_healthcare['distance_km'] <= 2.0])
        healthcare_within_5km = len(school_healthcare[school_healthcare['distance_km'] <= 5.0])
        
        metro_within_1km = len(school_metro[school_metro['distance_km'] <= 1.0])
        metro_within_2km = len(school_metro[school_metro['distance_km'] <= 2.0])
        metro_within_5km = len(school_metro[school_metro['distance_km'] <= 5.0])
        
        # Create enriched profile
        enriched_profile = {
            'school_name': school_name,
            'location': school['location'],
            'latitude': school['latitude'],
            'longitude': school['longitude'],
            'grades': school['grades_2014_15'],
            'students': school['students_2014_15'],
            'year_established': school['year_established_in_dubai'],
            'type_of_school': school['type_of_school'],
            
            # Nearest healthcare
            'nearest_healthcare_name': nearest_healthcare['facility_name'],
            'nearest_healthcare_type': nearest_healthcare['facility_type'],
            'nearest_healthcare_distance_km': nearest_healthcare['distance_km'],
            
            # Nearest metro
            'nearest_metro_station': nearest_metro['metro_station'],
            'nearest_metro_distance_km': nearest_metro['distance_km'],
            
            # Healthcare accessibility
            'healthcare_within_1km': healthcare_within_1km,
            'healthcare_within_2km': healthcare_within_2km,
            'healthcare_within_5km': healthcare_within_5km,
            
            # Metro accessibility
            'metro_within_1km': metro_within_1km,
            'metro_within_2km': metro_within_2km,
            'metro_within_5km': metro_within_5km,
            
            # Overall accessibility score (lower is better)
            'accessibility_score': (
                nearest_healthcare['distance_km'] * 0.4 +  # Healthcare weight
                nearest_metro['distance_km'] * 0.6         # Metro weight
            )
        }
        
        enriched_profiles.append(enriched_profile)
    
    enriched_df = pd.DataFrame(enriched_profiles)
    print(f"✅ Created enriched profiles for {len(enriched_df)} schools")
    
    return enriched_df

def save_distance_data(healthcare_distances, metro_distances, enriched_profiles):
    """Save all distance calculation results"""
    print("\n💾 Saving Distance Calculation Results...")
    
    # Create output directory
    output_dir = 'gis_integration/04_distance_calculations/distance_results'
    os.makedirs(output_dir, exist_ok=True)
    
    # Save detailed distance data
    healthcare_distances.to_csv(f'{output_dir}/school_to_healthcare_distances.csv', index=False)
    metro_distances.to_csv(f'{output_dir}/school_to_metro_distances.csv', index=False)
    
    # Save enriched school profiles
    enriched_profiles.to_csv(f'{output_dir}/enriched_school_profiles.csv', index=False)
    
    # Save summary statistics
    summary_stats = {
        'total_schools': len(enriched_profiles),
        'total_healthcare_facilities': len(healthcare_distances['facility_name'].unique()),
        'total_metro_stations': len(metro_distances['metro_station'].unique()),
        'total_distance_calculations': len(healthcare_distances) + len(metro_distances)
    }
    
    summary_df = pd.DataFrame([summary_stats])
    summary_df.to_csv(f'{output_dir}/distance_calculation_summary.csv', index=False)
    
    print(f"✅ Distance calculation results saved to: {output_dir}")
    
    return output_dir

def main():
    """Main distance calculation function"""
    print("📏 DISTANCE CALCULATIONS FOR SCHOOL SELECTION PLATFORM")
    print("="*70)
    
    # Load spatial prepared data
    print("📊 Loading spatial prepared data...")
    schools_df = pd.read_csv('gis_integration/03_spatial_preparation/spatial_prepared_data/schools_spatial_ready.csv')
    healthcare_df = pd.read_csv('gis_integration/03_spatial_preparation/spatial_prepared_data/healthcare_spatial_ready.csv')
    metro_df = pd.read_csv('gis_integration/03_spatial_preparation/spatial_prepared_data/metro_spatial_ready.csv')
    
    print(f"✅ Schools: {len(schools_df)}")
    print(f"✅ Healthcare: {len(healthcare_df)}")
    print(f"✅ Metro: {len(metro_df)}")
    
    # Step 1: Calculate school to healthcare distances
    healthcare_distances = calculate_school_to_healthcare_distances(schools_df, healthcare_df)
    
    # Step 2: Calculate school to metro distances
    metro_distances = calculate_school_to_metro_distances(schools_df, metro_df)
    
    # Step 3: Create enriched school profiles
    enriched_profiles = create_enriched_school_profiles(schools_df, healthcare_distances, metro_distances)
    
    # Step 4: Save all results
    output_dir = save_distance_data(healthcare_distances, metro_distances, enriched_profiles)
    
    # Summary report
    print("\n" + "="*70)
    print("DISTANCE CALCULATION SUMMARY")
    print("="*70)
    
    print(f"🏫 Schools analyzed: {len(schools_df)}")
    print(f"🏥 Healthcare facilities: {len(healthcare_df)}")
    print(f"🚇 Metro stations: {len(metro_df)}")
    print(f"📏 Total distance calculations: {len(healthcare_distances) + len(metro_distances):,}")
    
    print(f"\n🎯 Distance Calculations Complete!")
    print(f"🚀 Ready for Step 5: Data Integration!")
    
    return {
        'healthcare_distances': healthcare_distances,
        'metro_distances': metro_distances,
        'enriched_profiles': enriched_profiles,
        'output_dir': output_dir
    }

if __name__ == "__main__":
    results = main()
