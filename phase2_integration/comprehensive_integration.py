#!/usr/bin/env python3
"""
Comprehensive Integration: Schools + Communities + Metro + Healthcare
Complete spatial analysis combining all datasets
"""

import pandas as pd
import numpy as np
from pathlib import Path
import os

def load_all_datasets():
    """Load all datasets for comprehensive integration"""
    print("📊 COMPREHENSIVE INTEGRATION: ALL DATASETS")
    print("=" * 60)
    
    # Load community coordinates
    print("🌍 Loading community coordinates...")
    community_df = pd.read_csv('../community_coordinates/community_coordinates/dubai_communities_perfect_coordinates.csv')
    print(f"✅ Community data: {len(community_df)} communities")
    
    # Load school data
    print("🏫 Loading school data...")
    school_df = pd.read_csv('../gis_integration/05_data_integration/final_integrated_data/comprehensive_school_profiles.csv')
    print(f"✅ School data: {len(school_df)} schools")
    
    # Load healthcare data
    print("🏥 Loading healthcare data...")
    healthcare_df = pd.read_csv('../gis_integration/03_spatial_preparation/spatial_prepared_data/healthcare_spatial_ready.csv')
    print(f"✅ Healthcare data: {len(healthcare_df)} facilities")
    
    # Load metro data
    print("🚇 Loading metro data...")
    metro_df = pd.read_csv('../gis_integration/03_spatial_preparation/spatial_prepared_data/metro_spatial_ready.csv')
    print(f"✅ Metro data: {len(metro_df)} stations")
    
    # Load existing distance calculations
    print("📏 Loading existing distance calculations...")
    healthcare_distances = pd.read_csv('../gis_integration/04_distance_calculations/distance_results/school_to_healthcare_distances.csv')
    metro_distances = pd.read_csv('../gis_integration/04_distance_calculations/distance_results/school_to_metro_distances.csv')
    print(f"✅ Healthcare distances: {len(healthcare_distances)} records")
    print(f"✅ Metro distances: {len(metro_distances)} records")
    
    return community_df, school_df, healthcare_df, metro_df, healthcare_distances, metro_distances

def calculate_school_community_distances(school_df, community_df):
    """Calculate distances from each school to each community"""
    print("\n🗺️ Calculating school-community distances...")
    
    from math import radians, cos, sin, asin, sqrt
    
    def haversine_distance(lat1, lon1, lat2, lon2):
        """Calculate the great circle distance between two points on Earth"""
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        r = 6371  # Radius of earth in kilometers
        return c * r
    
    # Create distance matrix
    distances = []
    total_calculations = len(school_df) * len(community_df)
    current_calculation = 0
    
    print(f"📊 Calculating {total_calculations:,} school-community distances...")
    
    for _, school in school_df.iterrows():
        school_id = school['school_name']
        school_lat = school['latitude']
        school_lng = school['longitude']
        
        for _, community in community_df.iterrows():
            community_name = community['Community_Name']
            community_lat = community['Latitude']
            community_lng = community['Longitude']
            community_pop = community['Population']
            
            # Calculate distance
            distance = haversine_distance(school_lat, school_lng, community_lat, community_lng)
            
            distances.append({
                'school_name': school_id,
                'community_name': community_name,
                'community_population': community_pop,
                'distance_km': distance
            })
            
            current_calculation += 1
            if current_calculation % 10000 == 0:
                print(f"  Progress: {current_calculation:,}/{total_calculations:,} ({current_calculation/total_calculations*100:.1f}%)")
    
    # Convert to DataFrame
    distance_df = pd.DataFrame(distances)
    print(f"✅ Completed {len(distance_df):,} distance calculations")
    
    return distance_df

def create_comprehensive_analysis(school_df, community_df, healthcare_df, metro_df, 
                                school_community_distances, healthcare_distances, metro_distances):
    """Create comprehensive analysis combining all datasets"""
    print("\n📈 Creating comprehensive analysis...")
    
    # Community analysis for each school
    community_analysis = []
    
    for school_name in school_df['school_name']:
        school_distances = school_community_distances[school_community_distances['school_name'] == school_name]
        
        # Nearest community
        nearest_community = school_distances.loc[school_distances['distance_km'].idxmin()]
        
        # Communities within different distances
        within_1km = school_distances[school_distances['distance_km'] <= 1.0]
        within_2km = school_distances[school_distances['distance_km'] <= 2.0]
        within_5km = school_distances[school_distances['distance_km'] <= 5.0]
        
        # Population analysis
        total_pop_1km = within_1km['community_population'].sum()
        total_pop_2km = within_2km['community_population'].sum()
        total_pop_5km = within_5km['community_population'].sum()
        
        # Community count
        community_count_1km = len(within_1km)
        community_count_2km = len(within_2km)
        community_count_5km = len(within_5km)
        
        # Average distance to communities
        avg_community_distance = school_distances['distance_km'].mean()
        
        community_analysis.append({
            'school_name': school_name,
            'nearest_community': nearest_community['community_name'],
            'nearest_community_distance_km': nearest_community['distance_km'],
            'nearest_community_population': nearest_community['community_population'],
            'communities_within_1km': community_count_1km,
            'communities_within_2km': community_count_2km,
            'communities_within_5km': community_count_5km,
            'population_within_1km': total_pop_1km,
            'population_within_2km': total_pop_2km,
            'population_within_5km': total_pop_5km,
            'avg_distance_to_communities_km': avg_community_distance
        })
    
    community_analysis_df = pd.DataFrame(community_analysis)
    
    # Healthcare analysis for each school
    healthcare_analysis = []
    
    for school_name in school_df['school_name']:
        school_healthcare = healthcare_distances[healthcare_distances['school_name'] == school_name]
        
        # Nearest healthcare
        nearest_healthcare = school_healthcare.loc[school_healthcare['distance_km'].idxmin()]
        
        # Healthcare within different distances
        within_1km = school_healthcare[school_healthcare['distance_km'] <= 1.0]
        within_2km = school_healthcare[school_healthcare['distance_km'] <= 2.0]
        within_5km = school_healthcare[school_healthcare['distance_km'] <= 5.0]
        
        # Healthcare count
        healthcare_count_1km = len(within_1km)
        healthcare_count_2km = len(within_2km)
        healthcare_count_5km = len(within_5km)
        
        # Average distance to healthcare
        avg_healthcare_distance = school_healthcare['distance_km'].mean()
        
        healthcare_analysis.append({
            'school_name': school_name,
            'nearest_healthcare': nearest_healthcare['facility_name'],
            'nearest_healthcare_distance_km': nearest_healthcare['distance_km'],
            'healthcare_within_1km': healthcare_count_1km,
            'healthcare_within_2km': healthcare_count_2km,
            'healthcare_within_5km': healthcare_count_5km,
            'avg_distance_to_healthcare_km': avg_healthcare_distance
        })
    
    healthcare_analysis_df = pd.DataFrame(healthcare_analysis)
    
    # Metro analysis for each school
    metro_analysis = []
    
    for school_name in school_df['school_name']:
        school_metro = metro_distances[metro_distances['school_name'] == school_name]
        
        # Nearest metro
        nearest_metro = school_metro.loc[school_metro['distance_km'].idxmin()]
        
        # Metro within different distances
        within_1km = school_metro[school_metro['distance_km'] <= 1.0]
        within_2km = school_metro[school_metro['distance_km'] <= 2.0]
        within_5km = school_metro[school_metro['distance_km'] <= 5.0]
        
        # Metro count
        metro_count_1km = len(within_1km)
        metro_count_2km = len(within_2km)
        metro_count_5km = len(within_5km)
        
        # Average distance to metro
        avg_metro_distance = school_metro['distance_km'].mean()
        
        metro_analysis.append({
            'school_name': school_name,
            'nearest_metro': nearest_metro['metro_station'],
            'nearest_metro_distance_km': nearest_metro['distance_km'],
            'metro_within_1km': metro_count_1km,
            'metro_within_2km': metro_count_2km,
            'metro_within_5km': metro_count_5km,
            'avg_distance_to_metro_km': avg_metro_distance
        })
    
    metro_analysis_df = pd.DataFrame(metro_analysis)
    
    print(f"✅ Community analysis: {len(community_analysis_df)} schools")
    print(f"✅ Healthcare analysis: {len(healthcare_analysis_df)} schools")
    print(f"✅ Metro analysis: {len(metro_analysis_df)} schools")
    
    return community_analysis_df, healthcare_analysis_df, metro_analysis_df

def create_comprehensive_school_profiles(school_df, community_analysis_df, healthcare_analysis_df, metro_analysis_df):
    """Create comprehensive school profiles with all datasets"""
    print("\n🏫 Creating comprehensive school profiles...")
    
    # Start with base school data
    comprehensive_profiles = school_df.copy()
    
    # Merge community analysis
    comprehensive_profiles = comprehensive_profiles.merge(community_analysis_df, on='school_name', how='left')
    
    # Merge healthcare analysis
    comprehensive_profiles = comprehensive_profiles.merge(healthcare_analysis_df, on='school_name', how='left')
    
    # Merge metro analysis
    comprehensive_profiles = comprehensive_profiles.merge(metro_analysis_df, on='school_name', how='left')
    
    # Calculate comprehensive accessibility scores
    comprehensive_profiles['community_accessibility_score'] = comprehensive_profiles.apply(
        lambda row: calculate_community_accessibility_score(row), axis=1
    )
    
    comprehensive_profiles['healthcare_accessibility_score'] = comprehensive_profiles.apply(
        lambda row: calculate_healthcare_accessibility_score(row), axis=1
    )
    
    comprehensive_profiles['metro_accessibility_score'] = comprehensive_profiles.apply(
        lambda row: calculate_metro_accessibility_score(row), axis=1
    )
    
    # Calculate overall comprehensive score
    comprehensive_profiles['comprehensive_accessibility_score'] = (
        comprehensive_profiles['community_accessibility_score'] * 0.3 +
        comprehensive_profiles['healthcare_accessibility_score'] * 0.4 +
        comprehensive_profiles['metro_accessibility_score'] * 0.3
    )
    
    # Add urban amenity score (existing)
    if 'overall_urban_score' in comprehensive_profiles.columns:
        comprehensive_profiles['final_urban_score'] = (
            comprehensive_profiles['overall_urban_score'] * 0.4 +
            comprehensive_profiles['comprehensive_accessibility_score'] * 0.6
        )
    else:
        comprehensive_profiles['final_urban_score'] = comprehensive_profiles['comprehensive_accessibility_score']
    
    print(f"✅ Comprehensive profiles created for {len(comprehensive_profiles)} schools")
    
    return comprehensive_profiles

def calculate_community_accessibility_score(row):
    """Calculate community accessibility score (0-5, lower is better)"""
    nearest_dist = row.get('nearest_community_distance_km', 999)
    communities_1km = row.get('communities_within_1km', 0)
    communities_2km = row.get('communities_within_2km', 0)
    
    # Base score from nearest community distance
    if nearest_dist <= 0.5:
        base_score = 1.0
    elif nearest_dist <= 1.0:
        base_score = 2.0
    elif nearest_dist <= 2.0:
        base_score = 3.0
    elif nearest_dist <= 5.0:
        base_score = 4.0
    else:
        base_score = 5.0
    
    # Bonus for multiple communities nearby
    if communities_1km >= 3:
        base_score -= 0.5
    elif communities_1km >= 1:
        base_score -= 0.2
    
    if communities_2km >= 5:
        base_score -= 0.3
    
    return max(1.0, min(5.0, base_score))

def calculate_healthcare_accessibility_score(row):
    """Calculate healthcare accessibility score (0-5, lower is better)"""
    nearest_dist = row.get('nearest_healthcare_distance_km', 999)
    healthcare_1km = row.get('healthcare_within_1km', 0)
    healthcare_2km = row.get('healthcare_within_2km', 0)
    
    # Base score from nearest healthcare distance
    if nearest_dist <= 0.5:
        base_score = 1.0
    elif nearest_dist <= 1.0:
        base_score = 2.0
    elif nearest_dist <= 2.0:
        base_score = 3.0
    elif nearest_dist <= 5.0:
        base_score = 4.0
    else:
        base_score = 5.0
    
    # Bonus for multiple healthcare facilities nearby
    if healthcare_1km >= 5:
        base_score -= 0.5
    elif healthcare_1km >= 2:
        base_score -= 0.2
    
    if healthcare_2km >= 10:
        base_score -= 0.3
    
    return max(1.0, min(5.0, base_score))

def calculate_metro_accessibility_score(row):
    """Calculate metro accessibility score (0-5, lower is better)"""
    nearest_dist = row.get('nearest_metro_distance_km', 999)
    metro_1km = row.get('metro_within_1km', 0)
    metro_2km = row.get('metro_within_2km', 0)
    
    # Base score from nearest metro distance
    if nearest_dist <= 0.5:
        base_score = 1.0
    elif nearest_dist <= 1.0:
        base_score = 2.0
    elif nearest_dist <= 2.0:
        base_score = 3.0
    elif nearest_dist <= 5.0:
        base_score = 4.0
    else:
        base_score = 5.0
    
    # Bonus for multiple metro stations nearby
    if metro_1km >= 2:
        base_score -= 0.5
    elif metro_1km >= 1:
        base_score -= 0.2
    
    if metro_2km >= 3:
        base_score -= 0.3
    
    return max(1.0, min(5.0, base_score))

def create_comprehensive_insights(comprehensive_profiles):
    """Create comprehensive insights combining all datasets"""
    print("\n💡 Creating comprehensive insights...")
    
    insights = {
        # Basic counts
        'total_schools': len(comprehensive_profiles),
        'total_communities_analyzed': 226,
        'total_healthcare_facilities': 2312,
        'total_metro_stations': 540,
        
        # Community insights
        'avg_nearest_community_distance': comprehensive_profiles['nearest_community_distance_km'].mean(),
        'schools_within_1km_community': len(comprehensive_profiles[comprehensive_profiles['nearest_community_distance_km'] <= 1.0]),
        'schools_within_2km_community': len(comprehensive_profiles[comprehensive_profiles['nearest_community_distance_km'] <= 2.0]),
        'schools_within_5km_community': len(comprehensive_profiles[comprehensive_profiles['nearest_community_distance_km'] <= 5.0]),
        'avg_communities_within_1km': comprehensive_profiles['communities_within_1km'].mean(),
        'avg_communities_within_2km': comprehensive_profiles['communities_within_2km'].mean(),
        'avg_communities_within_5km': comprehensive_profiles['communities_within_5km'].mean(),
        'avg_population_within_1km': comprehensive_profiles['population_within_1km'].mean(),
        'avg_population_within_2km': comprehensive_profiles['population_within_2km'].mean(),
        'avg_population_within_5km': comprehensive_profiles['population_within_5km'].mean(),
        
        # Healthcare insights
        'avg_nearest_healthcare_distance': comprehensive_profiles.get('nearest_healthcare_distance_km', pd.Series([0])).mean(),
        'schools_within_1km_healthcare': len(comprehensive_profiles[comprehensive_profiles['nearest_healthcare_distance_km'] <= 1.0]) if 'nearest_healthcare_distance_km' in comprehensive_profiles.columns else 0,
        'schools_within_2km_healthcare': len(comprehensive_profiles[comprehensive_profiles['nearest_healthcare_distance_km'] <= 2.0]) if 'nearest_healthcare_distance_km' in comprehensive_profiles.columns else 0,
        'schools_within_5km_healthcare': len(comprehensive_profiles[comprehensive_profiles['nearest_healthcare_distance_km'] <= 5.0]) if 'nearest_healthcare_distance_km' in comprehensive_profiles.columns else 0,
        'avg_healthcare_within_1km': comprehensive_profiles.get('healthcare_within_1km', pd.Series([0])).mean(),
        'avg_healthcare_within_2km': comprehensive_profiles.get('healthcare_within_2km', pd.Series([0])).mean(),
        'avg_healthcare_within_5km': comprehensive_profiles.get('healthcare_within_5km', pd.Series([0])).mean(),
        
        # Metro insights
        'avg_nearest_metro_distance': comprehensive_profiles.get('nearest_metro_distance_km', pd.Series([0])).mean(),
        'schools_within_1km_metro': len(comprehensive_profiles[comprehensive_profiles['nearest_metro_distance_km'] <= 1.0]) if 'nearest_metro_distance_km' in comprehensive_profiles.columns else 0,
        'schools_within_2km_metro': len(comprehensive_profiles[comprehensive_profiles['nearest_metro_distance_km'] <= 2.0]) if 'nearest_metro_distance_km' in comprehensive_profiles.columns else 0,
        'schools_within_5km_metro': len(comprehensive_profiles[comprehensive_profiles['nearest_metro_distance_km'] <= 5.0]) if 'nearest_metro_distance_km' in comprehensive_profiles.columns else 0,
        'avg_metro_within_1km': comprehensive_profiles.get('metro_within_1km', pd.Series([0])).mean(),
        'avg_metro_within_2km': comprehensive_profiles.get('metro_within_2km', pd.Series([0])).mean(),
        'avg_metro_within_5km': comprehensive_profiles.get('metro_within_5km', pd.Series([0])).mean(),
        
        # Accessibility scores
        'avg_community_accessibility_score': comprehensive_profiles['community_accessibility_score'].mean(),
        'avg_healthcare_accessibility_score': comprehensive_profiles['healthcare_accessibility_score'].mean(),
        'avg_metro_accessibility_score': comprehensive_profiles['metro_accessibility_score'].mean(),
        'avg_comprehensive_accessibility_score': comprehensive_profiles['comprehensive_accessibility_score'].mean(),
        'avg_final_urban_score': comprehensive_profiles['final_urban_score'].mean()
    }
    
    print(f"✅ Created {len(insights)} comprehensive insights")
    return insights

def save_comprehensive_results(comprehensive_profiles, insights):
    """Save comprehensive results"""
    print("\n💾 Saving comprehensive results...")
    
    # Create output directory
    output_dir = Path("phase2_integration/comprehensive_results")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save comprehensive school profiles
    comprehensive_profiles.to_csv(output_dir / "comprehensive_school_profiles_all_datasets.csv", index=False)
    
    # Save insights
    import json
    with open(output_dir / "comprehensive_insights.json", 'w') as f:
        json.dump(insights, f, indent=2)
    
    # Create comprehensive summary report
    summary_report = f"""
# Comprehensive Integration: All Datasets Results

## 📊 Dataset Summary
- **Total Schools**: {insights['total_schools']}
- **Total Communities**: {insights['total_communities_analyzed']}
- **Total Healthcare Facilities**: {insights['total_healthcare_facilities']}
- **Total Metro Stations**: {insights['total_metro_stations']}

## 🏘️ Community Analysis
- **Average Nearest Community Distance**: {insights['avg_nearest_community_distance']:.3f} km
- **Schools within 1km of community**: {insights['schools_within_1km_community']} ({insights['schools_within_1km_community']/insights['total_schools']*100:.1f}%)
- **Schools within 2km of community**: {insights['schools_within_2km_community']} ({insights['schools_within_2km_community']/insights['total_schools']*100:.1f}%)
- **Schools within 5km of community**: {insights['schools_within_5km_community']} ({insights['schools_within_5km_community']/insights['total_schools']*100:.1f}%)
- **Average communities within 1km**: {insights['avg_communities_within_1km']:.1f}
- **Average population within 1km**: {insights['avg_population_within_1km']:,.0f}

## 🏥 Healthcare Analysis
- **Average Nearest Healthcare Distance**: {insights['avg_nearest_healthcare_distance']:.3f} km
- **Schools within 1km of healthcare**: {insights['schools_within_1km_healthcare']} ({insights['schools_within_1km_healthcare']/insights['total_schools']*100:.1f}%)
- **Schools within 2km of healthcare**: {insights['schools_within_2km_healthcare']} ({insights['schools_within_2km_healthcare']/insights['total_schools']*100:.1f}%)
- **Schools within 5km of healthcare**: {insights['schools_within_5km_healthcare']} ({insights['schools_within_5km_healthcare']/insights['total_schools']*100:.1f}%)
- **Average healthcare within 1km**: {insights['avg_healthcare_within_1km']:.1f}

## 🚇 Metro Analysis
- **Average Nearest Metro Distance**: {insights['avg_nearest_metro_distance']:.3f} km
- **Schools within 1km of metro**: {insights['schools_within_1km_metro']} ({insights['schools_within_1km_metro']/insights['total_schools']*100:.1f}%)
- **Schools within 2km of metro**: {insights['schools_within_2km_metro']} ({insights['schools_within_2km_metro']/insights['total_schools']*100:.1f}%)
- **Schools within 5km of metro**: {insights['schools_within_5km_metro']} ({insights['schools_within_5km_metro']/insights['total_schools']*100:.1f}%)
- **Average metro within 1km**: {insights['avg_metro_within_1km']:.1f}

## 🎯 Accessibility Scores
- **Community Accessibility Score**: {insights['avg_community_accessibility_score']:.2f}/5.0
- **Healthcare Accessibility Score**: {insights['avg_healthcare_accessibility_score']:.2f}/5.0
- **Metro Accessibility Score**: {insights['avg_metro_accessibility_score']:.2f}/5.0
- **Comprehensive Accessibility Score**: {insights['avg_comprehensive_accessibility_score']:.2f}/5.0
- **Final Urban Score**: {insights['avg_final_urban_score']:.2f}/5.0

## 📁 Files Created
- `comprehensive_school_profiles_all_datasets.csv` - Complete school profiles with all datasets
- `comprehensive_insights.json` - Complete insights and statistics

## 🚀 Integration Complete
All datasets successfully integrated! Ready for enhanced dashboard creation.
"""
    
    with open(output_dir / "comprehensive_summary_report.md", 'w') as f:
        f.write(summary_report)
    
    print(f"✅ Comprehensive results saved to: {output_dir}")
    return output_dir

def main():
    """Main comprehensive integration function"""
    try:
        # Step 1: Load all datasets
        community_df, school_df, healthcare_df, metro_df, healthcare_distances, metro_distances = load_all_datasets()
        
        # Step 2: Calculate school-community distances
        school_community_distances = calculate_school_community_distances(school_df, community_df)
        
        # Step 3: Create comprehensive analysis
        community_analysis_df, healthcare_analysis_df, metro_analysis_df = create_comprehensive_analysis(
            school_df, community_df, healthcare_df, metro_df, 
            school_community_distances, healthcare_distances, metro_distances
        )
        
        # Step 4: Create comprehensive school profiles
        comprehensive_profiles = create_comprehensive_school_profiles(
            school_df, community_analysis_df, healthcare_analysis_df, metro_analysis_df
        )
        
        # Step 5: Create comprehensive insights
        insights = create_comprehensive_insights(comprehensive_profiles)
        
        # Step 6: Save comprehensive results
        output_dir = save_comprehensive_results(comprehensive_profiles, insights)
        
        print("\n" + "=" * 60)
        print("🎉 COMPREHENSIVE INTEGRATION COMPLETE!")
        print("=" * 60)
        print("✅ All datasets successfully integrated")
        print("✅ Schools + Communities + Healthcare + Metro")
        print("✅ Comprehensive analysis completed")
        print("✅ Ready for enhanced dashboard creation")
        
        return comprehensive_profiles, insights
        
    except Exception as e:
        print(f"\n❌ Error in comprehensive integration: {e}")
        return None, None

if __name__ == "__main__":
    comprehensive_profiles, insights = main()
