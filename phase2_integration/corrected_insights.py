#!/usr/bin/env python3
"""
Corrected Insights for Comprehensive Integration
"""

import pandas as pd
import json

def create_corrected_insights():
    """Create corrected insights with proper column names"""
    print("🔧 Creating corrected insights...")
    
    # Load the comprehensive data
    df = pd.read_csv('phase2_integration/comprehensive_results/comprehensive_school_profiles_all_datasets.csv')
    
    # Create corrected insights
    insights = {
        # Basic counts
        'total_schools': len(df),
        'total_communities_analyzed': 226,
        'total_healthcare_facilities': 2312,
        'total_metro_stations': 540,
        
        # Community insights
        'avg_nearest_community_distance': df['nearest_community_distance_km'].mean(),
        'schools_within_1km_community': len(df[df['nearest_community_distance_km'] <= 1.0]),
        'schools_within_2km_community': len(df[df['nearest_community_distance_km'] <= 2.0]),
        'schools_within_5km_community': len(df[df['nearest_community_distance_km'] <= 5.0]),
        'avg_communities_within_1km': df['communities_within_1km'].mean(),
        'avg_communities_within_2km': df['communities_within_2km'].mean(),
        'avg_communities_within_5km': df['communities_within_5km'].mean(),
        'avg_population_within_1km': df['population_within_1km'].mean(),
        'avg_population_within_2km': df['population_within_2km'].mean(),
        'avg_population_within_5km': df['population_within_5km'].mean(),
        
        # Healthcare insights (using correct column names)
        'avg_nearest_healthcare_distance': df['nearest_healthcare_distance_km_x'].mean(),
        'schools_within_1km_healthcare': len(df[df['nearest_healthcare_distance_km_x'] <= 1.0]),
        'schools_within_2km_healthcare': len(df[df['nearest_healthcare_distance_km_x'] <= 2.0]),
        'schools_within_5km_healthcare': len(df[df['nearest_healthcare_distance_km_x'] <= 5.0]),
        'avg_healthcare_within_1km': df['healthcare_within_1km_x'].mean(),
        'avg_healthcare_within_2km': df['healthcare_within_2km_x'].mean(),
        'avg_healthcare_within_5km': df['healthcare_within_5km_x'].mean(),
        
        # Metro insights (using correct column names)
        'avg_nearest_metro_distance': df['nearest_metro_distance_km_x'].mean(),
        'schools_within_1km_metro': len(df[df['nearest_metro_distance_km_x'] <= 1.0]),
        'schools_within_2km_metro': len(df[df['nearest_metro_distance_km_x'] <= 2.0]),
        'schools_within_5km_metro': len(df[df['nearest_metro_distance_km_x'] <= 5.0]),
        'avg_metro_within_1km': df['metro_within_1km_x'].mean(),
        'avg_metro_within_2km': df['metro_within_2km_x'].mean(),
        'avg_metro_within_5km': df['metro_within_5km_x'].mean(),
        
        # Accessibility scores
        'avg_community_accessibility_score': df['community_accessibility_score'].mean(),
        'avg_healthcare_accessibility_score': df['healthcare_accessibility_score'].mean(),
        'avg_metro_accessibility_score': df['metro_accessibility_score'].mean(),
        'avg_comprehensive_accessibility_score': df['comprehensive_accessibility_score'].mean(),
        'avg_final_urban_score': df['final_urban_score'].mean()
    }
    
    # Save corrected insights
    with open('phase2_integration/comprehensive_results/corrected_insights.json', 'w') as f:
        json.dump(insights, f, indent=2)
    
    # Create corrected summary report
    summary_report = f"""
# CORRECTED Comprehensive Integration Results

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

## 🏥 Healthcare Analysis (CORRECTED)
- **Average Nearest Healthcare Distance**: {insights['avg_nearest_healthcare_distance']:.3f} km
- **Schools within 1km of healthcare**: {insights['schools_within_1km_healthcare']} ({insights['schools_within_1km_healthcare']/insights['total_schools']*100:.1f}%)
- **Schools within 2km of healthcare**: {insights['schools_within_2km_healthcare']} ({insights['schools_within_2km_healthcare']/insights['total_schools']*100:.1f}%)
- **Schools within 5km of healthcare**: {insights['schools_within_5km_healthcare']} ({insights['schools_within_5km_healthcare']/insights['total_schools']*100:.1f}%)
- **Average healthcare within 1km**: {insights['avg_healthcare_within_1km']:.1f}

## 🚇 Metro Analysis (CORRECTED)
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
- `corrected_insights.json` - CORRECTED insights and statistics
- `corrected_summary_report.md` - CORRECTED comprehensive summary report

## 🚀 Integration Complete
All datasets successfully integrated with CORRECTED insights! Ready for enhanced dashboard creation.
"""
    
    with open('phase2_integration/comprehensive_results/corrected_summary_report.md', 'w') as f:
        f.write(summary_report)
    
    print("✅ Corrected insights created!")
    print(f"📊 Healthcare: {insights['avg_nearest_healthcare_distance']:.3f} km average")
    print(f"🚇 Metro: {insights['avg_nearest_metro_distance']:.3f} km average")
    print(f"🏥 Schools within 1km healthcare: {insights['schools_within_1km_healthcare']}")
    print(f"🚇 Schools within 1km metro: {insights['schools_within_1km_metro']}")
    
    return insights

if __name__ == "__main__":
    insights = create_corrected_insights()
