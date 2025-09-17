#!/usr/bin/env python3
"""
Phase 1: Community Coordinates Solution
Get latitude and longitude for all 226 Dubai communities
"""

import pandas as pd
import requests
import json
import time
from pathlib import Path
import os

def download_dubai_community_data():
    """Download official Dubai community data from Dubai Pulse"""
    print("🌍 Downloading Dubai Community Data from Dubai Pulse...")
    
    # Dubai Pulse API endpoint
    url = "https://www.dubaipulse.gov.ae/api/v1/data/dm-location/dm_community-open"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        # Save raw data
        output_dir = Path("community_coordinates")
        output_dir.mkdir(exist_ok=True)
        
        with open(output_dir / "dubai_communities_raw.json", "w") as f:
            json.dump(response.json(), f, indent=2)
        
        print("✅ Dubai community data downloaded successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error downloading Dubai data: {e}")
        return False

def geocode_communities_fallback():
    """Fallback method: Geocode community names using OpenStreetMap"""
    print("🗺️ Using OpenStreetMap geocoding as fallback...")
    
    # Read community data
    df = pd.read_csv('../preprocessed_datasets/dubai_pop_2019_cleaned.csv')
    
    coordinates = []
    
    for idx, row in df.iterrows():
        community_name = row['Community_Name']
        print(f"Geocoding: {community_name} ({idx+1}/226)")
        
        try:
            # Use OpenStreetMap Nominatim API (free)
            url = f"https://nominatim.openstreetmap.org/search"
            params = {
                'q': f'{community_name}, Dubai, UAE',
                'format': 'json',
                'limit': 1
            }
            
            response = requests.get(url, params=params)
            data = response.json()
            
            if data:
                lat = float(data[0]['lat'])
                lng = float(data[0]['lon'])
                coordinates.append((lat, lng))
                print(f"  ✅ Found: {lat:.6f}, {lng:.6f}")
            else:
                coordinates.append((None, None))
                print(f"  ❌ Not found")
            
            # Be respectful to the API
            time.sleep(1)
            
        except Exception as e:
            coordinates.append((None, None))
            print(f"  ❌ Error: {e}")
    
    return coordinates

def validate_dubai_coordinates(lat, lng):
    """Validate coordinates are within Dubai boundaries"""
    # Dubai approximate boundaries
    min_lat, max_lat = 24.7, 25.4
    min_lng, max_lng = 55.1, 55.6
    
    if lat is None or lng is None:
        return False
    
    return (min_lat <= lat <= max_lat) and (min_lng <= lng <= max_lng)

def create_community_coordinates_dataset():
    """Main function to create community coordinates dataset"""
    print("🎯 PHASE 1: COMMUNITY COORDINATES")
    print("=" * 50)
    
    # Step 1: Try to download official Dubai data
    if download_dubai_community_data():
        print("✅ Official Dubai data downloaded - processing...")
        # TODO: Process KML/JSON data to extract coordinates
        # For now, use fallback method
    
    # Step 2: Use geocoding fallback
    print("\n🗺️ Using geocoding fallback method...")
    coordinates = geocode_communities_fallback()
    
    # Step 3: Create enhanced dataset
    print("\n📊 Creating enhanced community dataset...")
    
    # Read original data
    df = pd.read_csv('../preprocessed_datasets/dubai_pop_2019_cleaned.csv')
    
    # Add coordinates
    df['Latitude'] = [coord[0] for coord in coordinates]
    df['Longitude'] = [coord[1] for coord in coordinates]
    
    # Validate coordinates
    df['Valid_Coordinates'] = df.apply(
        lambda row: validate_dubai_coordinates(row['Latitude'], row['Longitude']), 
        axis=1
    )
    
    # Statistics
    valid_count = df['Valid_Coordinates'].sum()
    total_count = len(df)
    
    print(f"\n📈 COORDINATE EXTRACTION RESULTS:")
    print(f"✅ Valid coordinates: {valid_count}/{total_count} ({valid_count/total_count*100:.1f}%)")
    print(f"❌ Missing coordinates: {total_count - valid_count}")
    
    # Save results
    output_dir = Path("community_coordinates")
    output_dir.mkdir(exist_ok=True)
    
    # Save enhanced dataset
    df.to_csv(output_dir / "dubai_communities_with_coordinates.csv", index=False)
    
    # Save validation report
    validation_report = {
        'total_communities': total_count,
        'valid_coordinates': valid_count,
        'missing_coordinates': total_count - valid_count,
        'success_rate': f"{valid_count/total_count*100:.1f}%",
        'dubai_boundaries': {
            'min_lat': 24.7,
            'max_lat': 25.4,
            'min_lng': 55.1,
            'max_lng': 55.6
        }
    }
    
    with open(output_dir / "coordinate_validation_report.json", "w") as f:
        json.dump(validation_report, f, indent=2)
    
    print(f"\n💾 Files saved to: {output_dir}")
    print(f"📄 Enhanced dataset: dubai_communities_with_coordinates.csv")
    print(f"📄 Validation report: coordinate_validation_report.json")
    
    return df

def main():
    """Main execution function"""
    try:
        df = create_community_coordinates_dataset()
        
        print("\n" + "=" * 50)
        print("🎉 PHASE 1 COMPLETE!")
        print("=" * 50)
        print("✅ Community coordinates extracted")
        print("✅ Dataset enhanced with lat/lng")
        print("✅ Validation completed")
        print("✅ Ready for Phase 2: Integration")
        
        return df
        
    except Exception as e:
        print(f"\n❌ Error in Phase 1: {e}")
        return None

if __name__ == "__main__":
    result = main()
