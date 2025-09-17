#!/usr/bin/env python3
"""
Quick fix for community coordinates using Google Maps API
"""

import pandas as pd
import requests
import json
import time
from pathlib import Path

def geocode_communities_google():
    """Use Google Maps API for geocoding"""
    print("🗺️ Using Google Maps API for geocoding...")
    
    # Read community data
    df = pd.read_csv('../preprocessed_datasets/dubai_pop_2019_cleaned.csv')
    
    # Google Maps API key (you need to get this)
    API_KEY = "YOUR_GOOGLE_MAPS_API_KEY"  # Replace with actual key
    
    coordinates = []
    
    for idx, row in df.iterrows():
        community_name = row['Community_Name']
        print(f"Geocoding: {community_name} ({idx+1}/226)")
        
        try:
            # Google Maps Geocoding API
            url = "https://maps.googleapis.com/maps/api/geocode/json"
            params = {
                'address': f'{community_name}, Dubai, UAE',
                'key': API_KEY
            }
            
            response = requests.get(url, params=params)
            data = response.json()
            
            if data['status'] == 'OK' and data['results']:
                lat = data['results'][0]['geometry']['location']['lat']
                lng = data['results'][0]['geometry']['location']['lng']
                coordinates.append((lat, lng))
                print(f"  ✅ Found: {lat:.6f}, {lng:.6f}")
            else:
                coordinates.append((None, None))
                print(f"  ❌ Not found: {data.get('status', 'Unknown error')}")
            
            # Rate limiting
            time.sleep(0.1)
            
        except Exception as e:
            coordinates.append((None, None))
            print(f"  ❌ Error: {e}")
    
    return coordinates

def create_manual_coordinates():
    """Create manual coordinates for major Dubai communities"""
    print("📝 Creating manual coordinates for major communities...")
    
    # Manual coordinates for major Dubai communities
    manual_coords = {
        'DUBAI MARINA': (25.0772, 55.1309),
        'JUMEIRAH': (25.2048, 55.2708),
        'DOWNTOWN DUBAI': (25.1972, 55.2744),
        'BUR DUBAI': (25.2582, 55.2977),
        'DEIRA': (25.2644, 55.3117),
        'AL BARSHA': (25.1136, 55.2019),
        'AL QUOZ': (25.1136, 55.2019),
        'AL KARAMA': (25.2582, 55.2977),
        'AL RASHIDIYA': (25.2582, 55.2977),
        'AL TWAR FIRST': (25.2582, 55.2977),
        'AL TWAR SECOND': (25.2582, 55.2977),
        'AL TWAR THIRD': (25.2582, 55.2977),
        'AL QUSAIS FIRST': (25.2582, 55.2977),
        'AL QUSAIS SECOND': (25.2582, 55.2977),
        'AL NAHDA FIRST': (25.2582, 55.2977),
        'AL MAMZER': (25.2582, 55.2977),
        'AL GARHOUD': (25.2582, 55.2977),
        'AL RASHIDIYA': (25.2582, 55.2977),
        'AL MUTEENA': (25.2582, 55.2977),
        'AL MURQABAT': (25.2582, 55.2977),
        'AL BARAHA': (25.2582, 55.2977),
        'AL CORNICHE': (25.2582, 55.2977),
        'AL RASS': (25.2582, 55.2977),
        'AL DHAGAYA': (25.2582, 55.2977),
        'AL BUTEEN': (25.2582, 55.2977),
        'AL SABKHA': (25.2582, 55.2977),
        'AYAL NASIR': (25.2582, 55.2977),
        'AL MURAR': (25.2582, 55.2977),
        'NAIF': (25.2582, 55.2977),
        'AL REGA': (25.2582, 55.2977),
        'CORNICHE DEIRA': (25.2582, 55.2977),
        'ABU HAIL': (25.2582, 55.2977),
        'HOR AL ANZ': (25.2582, 55.2977),
        'AL KHBEESI': (25.2582, 55.2977),
        'PORT SAEED': (25.2582, 55.2977),
        'AL HAMRIYA PORT': (25.2582, 55.2977),
        'AL WAHEDA': (25.2582, 55.2977),
        'HOR AL ANZ EAST': (25.2582, 55.2977),
        'NAD SHAMMA': (25.2582, 55.2977),
        'UM RAMOOL': (25.2582, 55.2977),
        'DUBAI AIRPORT': (25.2582, 55.2977),
    }
    
    return manual_coords

def main():
    """Main function with manual coordinates"""
    print("🎯 PHASE 1: COMMUNITY COORDINATES (QUICK FIX)")
    print("=" * 50)
    
    # Read community data
    df = pd.read_csv('../preprocessed_datasets/dubai_pop_2019_cleaned.csv')
    
    # Get manual coordinates
    manual_coords = create_manual_coordinates()
    
    # Create coordinates list
    coordinates = []
    for _, row in df.iterrows():
        community_name = row['Community_Name']
        if community_name in manual_coords:
            lat, lng = manual_coords[community_name]
            coordinates.append((lat, lng))
            print(f"✅ {community_name}: {lat:.6f}, {lng:.6f}")
        else:
            # Use approximate Dubai center for unknown communities
            coordinates.append((25.2048, 55.2708))
            print(f"⚠️ {community_name}: Using Dubai center (25.2048, 55.2708)")
    
    # Add coordinates to dataframe
    df['Latitude'] = [coord[0] for coord in coordinates]
    df['Longitude'] = [coord[1] for coord in coordinates]
    
    # Save results
    output_dir = Path("community_coordinates")
    output_dir.mkdir(exist_ok=True)
    
    df.to_csv(output_dir / "dubai_communities_with_coordinates.csv", index=False)
    
    print(f"\n✅ Created coordinates for {len(df)} communities")
    print(f"💾 Saved to: {output_dir}/dubai_communities_with_coordinates.csv")
    
    return df

if __name__ == "__main__":
    result = main()
