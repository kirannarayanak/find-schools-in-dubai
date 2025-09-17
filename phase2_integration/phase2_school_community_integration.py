#!/usr/bin/env python3
"""
Phase 2: School-Community Integration
Integrate community coordinates with school data for enhanced spatial analysis
"""

import pandas as pd
import numpy as np
from pathlib import Path
import os

def load_phase2_data():
    """Load all required data for Phase 2 integration"""
    print("📊 PHASE 2: SCHOOL-COMMUNITY INTEGRATION")
    print("=" * 60)
    
    # Load community coordinates
    print("🌍 Loading community coordinates...")
    community_df = pd.read_csv('../community_coordinates/community_coordinates/dubai_communities_perfect_coordinates.csv')
    print(f"✅ Community data: {len(community_df)} communities")
    
    # Load school data
    print("🏫 Loading school data...")
    school_df = pd.read_csv('../gis_integration/05_data_integration/final_integrated_data/comprehensive_school_profiles.csv')
    print(f"✅ School data: {len(school_df)} schools")
    
    # Load existing distance data
    print("📏 Loading existing distance calculations...")
    healthcare_distances = pd.read_csv('../gis_integration/04_distance_calculations/distance_results/school_to_healthcare_distances.csv')
    metro_distances = pd.read_csv('../gis_integration/04_distance_calculations/distance_results/school_to_metro_distances.csv')
    print(f"✅ Healthcare distances: {len(healthcare_distances)} records")
    print(f"✅ Metro distances: {len(metro_distances)} records")
    
    return community_df, school_df, healthcare_distances, metro_distances

def calculate_school_community_distances(school_df, community_df):
    """Calculate distances from each school to each community"""
    print("\n🗺️ Calculating school-community distances...")
    
    from math import radians, cos, sin, asin, sqrt
    
    def haversine_distance(lat1, lon1, lat2, lon2):
        """Calculate the great circle distance between two points on Earth"""
        # Convert decimal degrees to radians
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        
        # Haversine formula
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

def create_community_analysis(school_df, community_df, distance_df):
    """Create comprehensive community analysis for each school"""
    print("\n📈 Creating community analysis...")
    
    # Find nearest community for each school
    nearest_communities = distance_df.loc[distance_df.groupby('school_name')['distance_km'].idxmin()]
    
    # Find communities within 1km, 2km, 5km for each school
    community_analysis = []
    
    for school_name in school_df['school_name']:
        school_distances = distance_df[distance_df['school_name'] == school_name]
        
        # Nearest community
        nearest = school_distances.loc[school_distances['distance_km'].idxmin()]
        
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
        avg_distance = school_distances['distance_km'].mean()
        
        community_analysis.append({
            'school_name': school_name,
            'nearest_community': nearest['community_name'],
            'nearest_community_distance_km': nearest['distance_km'],
            'nearest_community_population': nearest['community_population'],
            'communities_within_1km': community_count_1km,
            'communities_within_2km': community_count_2km,
            'communities_within_5km': community_count_5km,
            'population_within_1km': total_pop_1km,
            'population_within_2km': total_pop_2km,
            'population_within_5km': total_pop_5km,
            'avg_distance_to_communities_km': avg_distance
        })
    
    community_analysis_df = pd.DataFrame(community_analysis)
    print(f"✅ Created community analysis for {len(community_analysis_df)} schools")
    
    return community_analysis_df

def create_enhanced_school_profiles(school_df, community_analysis_df):
    """Create enhanced school profiles with community data"""
    print("\n🏫 Creating enhanced school profiles...")
    
    # Merge school data with community analysis
    enhanced_profiles = school_df.merge(community_analysis_df, on='school_name', how='left')
    
    # Add community accessibility scores
    enhanced_profiles['community_accessibility_score'] = enhanced_profiles.apply(
        lambda row: calculate_community_accessibility_score(row), axis=1
    )
    
    # Add community density score
    enhanced_profiles['community_density_score'] = enhanced_profiles.apply(
        lambda row: calculate_community_density_score(row), axis=1
    )
    
    # Add overall community score
    enhanced_profiles['overall_community_score'] = (
        enhanced_profiles['community_accessibility_score'] * 0.6 +
        enhanced_profiles['community_density_score'] * 0.4
    )
    
    print(f"✅ Enhanced profiles created for {len(enhanced_profiles)} schools")
    
    return enhanced_profiles

def calculate_community_accessibility_score(row):
    """Calculate community accessibility score (0-5, lower is better)"""
    nearest_dist = row['nearest_community_distance_km']
    communities_1km = row['communities_within_1km']
    communities_2km = row['communities_within_2km']
    
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

def calculate_community_density_score(row):
    """Calculate community density score (0-5, higher is better)"""
    pop_1km = row['population_within_1km']
    pop_2km = row['population_within_2km']
    pop_5km = row['population_within_5km']
    
    # Score based on population density
    if pop_1km >= 50000:
        score = 5.0
    elif pop_1km >= 25000:
        score = 4.0
    elif pop_2km >= 50000:
        score = 3.0
    elif pop_5km >= 100000:
        score = 2.0
    else:
        score = 1.0
    
    return score

def create_phase2_insights(enhanced_profiles):
    """Create insights and statistics for Phase 2"""
    print("\n💡 Creating Phase 2 insights...")
    
    insights = {
        'total_schools': len(enhanced_profiles),
        'total_communities_analyzed': 226,
        'avg_nearest_community_distance': enhanced_profiles['nearest_community_distance_km'].mean(),
        'schools_within_1km_community': len(enhanced_profiles[enhanced_profiles['nearest_community_distance_km'] <= 1.0]),
        'schools_within_2km_community': len(enhanced_profiles[enhanced_profiles['nearest_community_distance_km'] <= 2.0]),
        'schools_within_5km_community': len(enhanced_profiles[enhanced_profiles['nearest_community_distance_km'] <= 5.0]),
        'avg_communities_within_1km': enhanced_profiles['communities_within_1km'].mean(),
        'avg_communities_within_2km': enhanced_profiles['communities_within_2km'].mean(),
        'avg_communities_within_5km': enhanced_profiles['communities_within_5km'].mean(),
        'avg_population_within_1km': enhanced_profiles['population_within_1km'].mean(),
        'avg_population_within_2km': enhanced_profiles['population_within_2km'].mean(),
        'avg_population_within_5km': enhanced_profiles['population_within_5km'].mean(),
        'avg_community_accessibility_score': enhanced_profiles['community_accessibility_score'].mean(),
        'avg_community_density_score': enhanced_profiles['community_density_score'].mean(),
        'avg_overall_community_score': enhanced_profiles['overall_community_score'].mean()
    }
    
    print(f"✅ Created {len(insights)} key insights")
    return insights

def save_phase2_results(enhanced_profiles, community_analysis_df, distance_df, insights):
    """Save all Phase 2 results"""
    print("\n💾 Saving Phase 2 results...")
    
    # Create output directory
    output_dir = Path("phase2_integration/results")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save enhanced school profiles
    enhanced_profiles.to_csv(output_dir / "enhanced_school_profiles_with_communities.csv", index=False)
    
    # Save community analysis
    community_analysis_df.to_csv(output_dir / "school_community_analysis.csv", index=False)
    
    # Save distance matrix (sample for performance)
    distance_sample = distance_df.sample(n=min(10000, len(distance_df)))
    distance_sample.to_csv(output_dir / "school_community_distances_sample.csv", index=False)
    
    # Save insights
    import json
    with open(output_dir / "phase2_insights.json", 'w') as f:
        json.dump(insights, f, indent=2)
    
    # Create summary report
    summary_report = f"""
# Phase 2: School-Community Integration Results

## 📊 Summary Statistics
- **Total Schools Analyzed**: {insights['total_schools']}
- **Total Communities Analyzed**: {insights['total_communities_analyzed']}
- **Average Nearest Community Distance**: {insights['avg_nearest_community_distance']:.3f} km

## 🏘️ Community Proximity Analysis
- **Schools within 1km of community**: {insights['schools_within_1km_community']} ({insights['schools_within_1km_community']/insights['total_schools']*100:.1f}%)
- **Schools within 2km of community**: {insights['schools_within_2km_community']} ({insights['schools_within_2km_community']/insights['total_schools']*100:.1f}%)
- **Schools within 5km of community**: {insights['schools_within_5km_community']} ({insights['schools_within_5km_community']/insights['total_schools']*100:.1f}%)

## 📈 Community Density Analysis
- **Average communities within 1km**: {insights['avg_communities_within_1km']:.1f}
- **Average communities within 2km**: {insights['avg_communities_within_2km']:.1f}
- **Average communities within 5km**: {insights['avg_communities_within_5km']:.1f}

## 👥 Population Analysis
- **Average population within 1km**: {insights['avg_population_within_1km']:,.0f}
- **Average population within 2km**: {insights['avg_population_within_2km']:,.0f}
- **Average population within 5km**: {insights['avg_population_within_5km']:,.0f}

## 🎯 Community Scores
- **Average Community Accessibility Score**: {insights['avg_community_accessibility_score']:.2f}/5.0
- **Average Community Density Score**: {insights['avg_community_density_score']:.2f}/5.0
- **Average Overall Community Score**: {insights['avg_overall_community_score']:.2f}/5.0

## 📁 Files Created
- `enhanced_school_profiles_with_communities.csv` - Complete school profiles with community data
- `school_community_analysis.csv` - Detailed community analysis per school
- `school_community_distances_sample.csv` - Sample of distance calculations
- `phase2_insights.json` - Complete insights and statistics

## 🚀 Next Steps
Phase 2 complete! Ready for Phase 3: Enhanced Dashboard Creation
"""
    
    with open(output_dir / "phase2_summary_report.md", 'w') as f:
        f.write(summary_report)
    
    print(f"✅ Phase 2 results saved to: {output_dir}")
    return output_dir

def main():
    """Main Phase 2 execution function"""
    try:
        # Step 1: Load data
        community_df, school_df, healthcare_distances, metro_distances = load_phase2_data()
        
        # Step 2: Calculate school-community distances
        distance_df = calculate_school_community_distances(school_df, community_df)
        
        # Step 3: Create community analysis
        community_analysis_df = create_community_analysis(school_df, community_df, distance_df)
        
        # Step 4: Create enhanced school profiles
        enhanced_profiles = create_enhanced_school_profiles(school_df, community_analysis_df)
        
        # Step 5: Create insights
        insights = create_phase2_insights(enhanced_profiles)
        
        # Step 6: Save results
        output_dir = save_phase2_results(enhanced_profiles, community_analysis_df, distance_df, insights)
        
        print("\n" + "=" * 60)
        print("🎉 PHASE 2 COMPLETE!")
        print("=" * 60)
        print("✅ School-community integration successful")
        print("✅ Enhanced school profiles created")
        print("✅ Community analysis completed")
        print("✅ Ready for Phase 3: Enhanced Dashboard")
        
        return enhanced_profiles, insights
        
    except Exception as e:
        print(f"\n❌ Error in Phase 2: {e}")
        return None, None

if __name__ == "__main__":
    enhanced_profiles, insights = main()
