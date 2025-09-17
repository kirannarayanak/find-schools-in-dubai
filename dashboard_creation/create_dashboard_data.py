import pandas as pd
import numpy as np
import os
from pathlib import Path

def load_final_integrated_data():
    """Load the final integrated dataset for dashboard creation"""
    print("📊 Loading Final Integrated Data for Dashboard...")
    
    # Load comprehensive school profiles
    comprehensive_df = pd.read_csv('gis_integration/05_data_integration/final_integrated_data/comprehensive_school_profiles.csv')
    print(f"✅ Comprehensive profiles: {len(comprehensive_df)} schools")
    
    # Load insights data
    top_accessible = pd.read_csv('gis_integration/05_data_integration/final_integrated_data/top_accessible_schools.csv')
    best_healthcare = pd.read_csv('gis_integration/05_data_integration/final_integrated_data/best_healthcare_access_schools.csv')
    best_metro = pd.read_csv('gis_integration/05_data_integration/final_integrated_data/best_metro_access_schools.csv')
    best_urban = pd.read_csv('gis_integration/05_data_integration/final_integrated_data/best_urban_schools.csv')
    
    print(f"✅ Top accessible schools: {len(top_accessible)}")
    print(f"✅ Best healthcare access: {len(best_healthcare)}")
    print(f"✅ Best metro access: {len(best_metro)}")
    print(f"✅ Best urban schools: {len(best_urban)}")
    
    return comprehensive_df, top_accessible, best_healthcare, best_metro, best_urban

def create_dashboard_insights(comprehensive_df):
    """Create key insights and statistics for the dashboard"""
    print("\n💡 Creating Dashboard Insights...")
    
    insights = {}
    
    # Overall statistics
    insights['total_schools'] = len(comprehensive_df)
    insights['total_locations'] = comprehensive_df['location'].nunique()
    insights['curriculum_types'] = comprehensive_df['type_of_school'].nunique()
    
    # Healthcare accessibility insights
    insights['avg_healthcare_distance'] = comprehensive_df['nearest_healthcare_distance_km'].mean()
    insights['schools_within_1km_healthcare'] = len(comprehensive_df[comprehensive_df['nearest_healthcare_distance_km'] <= 1.0])
    insights['schools_within_2km_healthcare'] = len(comprehensive_df[comprehensive_df['nearest_healthcare_distance_km'] <= 2.0])
    insights['schools_within_5km_healthcare'] = len(comprehensive_df[comprehensive_df['nearest_healthcare_distance_km'] <= 5.0])
    
    # Metro accessibility insights
    insights['avg_metro_distance'] = comprehensive_df['nearest_metro_distance_km'].mean()
    insights['schools_within_1km_metro'] = len(comprehensive_df[comprehensive_df['nearest_metro_distance_km'] <= 1.0])
    insights['schools_within_2km_metro'] = len(comprehensive_df[comprehensive_df['nearest_metro_distance_km'] <= 2.0])
    insights['schools_within_5km_metro'] = len(comprehensive_df[comprehensive_df['nearest_metro_distance_km'] <= 5.0])
    
    # School type distribution
    school_types = comprehensive_df['type_of_school'].value_counts()
    insights['school_type_distribution'] = school_types.to_dict()
    
    # Location distribution
    location_counts = comprehensive_df['location'].value_counts().head(10)
    insights['top_locations'] = location_counts.to_dict()
    
    # Grade level distribution
    grade_counts = comprehensive_df['grades'].value_counts()
    insights['grade_level_distribution'] = grade_counts.to_dict()
    
    # Accessibility score distribution
    insights['avg_accessibility_score'] = comprehensive_df['accessibility_score'].mean()
    insights['avg_urban_score'] = comprehensive_df['overall_urban_score'].mean()
    
    print(f"✅ Created {len(insights)} key insights for dashboard")
    return insights

def create_filtering_categories(comprehensive_df):
    """Create categories and filters for the dashboard"""
    print("\n🔍 Creating Dashboard Filters...")
    
    # Location filters
    locations = sorted(comprehensive_df['location'].unique())
    
    # School type filters
    school_types = sorted(comprehensive_df['type_of_school'].unique())
    
    # Grade level filters
    grade_levels = sorted(comprehensive_df['grades'].unique())
    
    # Distance range filters
    distance_ranges = [
        "Within 1km",
        "Within 2km", 
        "Within 5km",
        "More than 5km"
    ]
    
    # Accessibility score ranges
    score_ranges = [
        "Excellent (0-1)",
        "Good (1-2)",
        "Fair (2-3)",
        "Limited (3+)"
    ]
    
    filters = {
        'locations': locations,
        'school_types': school_types,
        'grade_levels': grade_levels,
        'distance_ranges': distance_ranges,
        'score_ranges': score_ranges
    }
    
    print(f"✅ Created filtering categories for dashboard")
    return filters

def create_sample_visualizations(comprehensive_df):
    """Create sample visualizations and charts for the dashboard"""
    print("\n📊 Creating Sample Visualizations...")
    
    # 1. Healthcare accessibility by location
    healthcare_by_location = comprehensive_df.groupby('location')['nearest_healthcare_distance_km'].mean().sort_values().head(10)
    
    # 2. Metro accessibility by location
    metro_by_location = comprehensive_df.groupby('location')['nearest_metro_distance_km'].mean().sort_values().head(10)
    
    # 3. School distribution by type
    school_type_dist = comprehensive_df['type_of_school'].value_counts()
    
    # 4. Accessibility score distribution
    accessibility_dist = comprehensive_df['accessibility_score'].value_counts(bins=5)
    
    # 5. Healthcare facilities within 5km by school
    healthcare_5km_dist = comprehensive_df['healthcare_within_5km'].value_counts().sort_index()
    
    # 6. Metro stations within 5km by school
    metro_5km_dist = comprehensive_df['metro_within_5km'].value_counts().sort_index()
    
    visualizations = {
        'healthcare_by_location': healthcare_by_location,
        'metro_by_location': metro_by_location,
        'school_type_distribution': school_type_dist,
        'accessibility_distribution': accessibility_dist,
        'healthcare_5km_distribution': healthcare_5km_dist,
        'metro_5km_distribution': metro_5km_dist
    }
    
    print(f"✅ Created {len(visualizations)} sample visualizations")
    return visualizations

def create_dashboard_data_files(comprehensive_df, insights, filters, visualizations):
    """Create all data files needed for the dashboard"""
    print("\n💾 Creating Dashboard Data Files...")
    
    # Create output directory
    output_dir = 'dashboard_creation/dashboard_data'
    os.makedirs(output_dir, exist_ok=True)
    
    # Save main dataset
    comprehensive_df.to_csv(f'{output_dir}/dashboard_main_data.csv', index=False)
    
    # Save insights as JSON
    import json
    with open(f'{output_dir}/dashboard_insights.json', 'w') as f:
        json.dump(insights, f, indent=2)
    
    # Save filters
    with open(f'{output_dir}/dashboard_filters.json', 'w') as f:
        json.dump(filters, f, indent=2)
    
    # Save visualizations
    for name, data in visualizations.items():
        if hasattr(data, 'to_csv'):
            data.to_csv(f'{output_dir}/{name}.csv')
        else:
            # Convert to DataFrame if it's a dict
            pd.DataFrame(list(data.items()), columns=['Category', 'Count']).to_csv(f'{output_dir}/{name}.csv', index=False)
    
    # Create dashboard configuration file
    dashboard_config = {
        'title': 'Dubai School Selection Platform',
        'subtitle': 'Data-Driven School Selection Based on Healthcare, Transport & Urban Amenities',
        'description': 'Interactive platform helping parents choose schools in Dubai based on proximity to healthcare facilities, metro stations, and urban amenities.',
        'data_sources': [
            'KHDA School Database',
            'Dubai Health Authority (Sheryan)',
            'RTA Metro Venues',
            'Dubai Municipality Demographics'
        ],
        'total_schools': len(comprehensive_df),
        'total_healthcare_facilities': 2312,
        'total_metro_stations': 540,
        'total_distance_calculations': 484840
    }
    
    with open(f'{output_dir}/dashboard_config.json', 'w') as f:
        json.dump(dashboard_config, f, indent=2)
    
    print(f"✅ Dashboard data files saved to: {output_dir}")
    return output_dir

def create_dashboard_instructions():
    """Create instructions for building the Tableau dashboard"""
    print("\n📋 Creating Dashboard Instructions...")
    
    instructions = """
# Dubai School Selection Platform - Dashboard Creation Instructions

## 🎯 Dashboard Overview
Create an interactive Tableau dashboard that helps parents in Dubai choose schools based on:
- Healthcare proximity
- Metro accessibility  
- Urban amenities
- Overall accessibility scores

## 📊 Key Dashboard Components

### 1. Main Map View
- **Map Type:** Geographic map of Dubai
- **Data Points:** All 170 schools with color coding by accessibility score
- **Filters:** Location, school type, grade levels
- **Tooltips:** School name, nearest healthcare, nearest metro, accessibility score

### 2. Healthcare Proximity Analysis
- **Chart Type:** Bar chart
- **X-Axis:** School locations
- **Y-Axis:** Distance to nearest healthcare facility
- **Color:** Healthcare accessibility score
- **Filters:** Distance ranges (1km, 2km, 5km)

### 3. Metro Accessibility Analysis  
- **Chart Type:** Bar chart
- **X-Axis:** School locations
- **Y-Axis:** Distance to nearest metro station
- **Color:** Metro accessibility score
- **Filters:** Distance ranges (1km, 2km, 5km)

### 4. School Comparison Table
- **Columns:** School name, location, grades, healthcare distance, metro distance, urban score
- **Sorting:** By any column
- **Filters:** All available filters
- **Highlighting:** Selected schools

### 5. Accessibility Score Distribution
- **Chart Type:** Histogram or box plot
- **X-Axis:** Accessibility score ranges
- **Y-Axis:** Number of schools
- **Color:** School type

### 6. Location-based Insights
- **Chart Type:** Scatter plot
- **X-Axis:** Healthcare distance
- **Y-Axis:** Metro distance
- **Color:** Location
- **Size:** Urban score

## 🔧 Technical Requirements

### Data Sources
- **Main Data:** dashboard_main_data.csv
- **Insights:** dashboard_insights.json
- **Filters:** dashboard_filters.json
- **Configuration:** dashboard_config.json

### Key Metrics to Display
- Total schools analyzed: 170
- Average healthcare distance: 0.159 km
- Average metro distance: 2.877 km
- Schools within 1km healthcare: 167
- Schools within 1km metro: 47

### Interactive Features
- **Filters:** Location, school type, grade level, distance ranges
- **Drill-down:** From location to individual schools
- **Search:** School name search functionality
- **Comparison:** Side-by-side school comparison
- **Export:** Data export capabilities

## 🎨 Design Guidelines

### Color Scheme
- **Healthcare:** Blue tones (medical/healthcare theme)
- **Metro:** Green tones (transport/accessibility theme)
- **Schools:** Neutral tones with accent colors
- **Scores:** Red (poor) to Green (excellent) gradient

### Layout
- **Header:** Title, subtitle, key statistics
- **Main Area:** Map view with filters
- **Sidebar:** Detailed analysis charts
- **Footer:** Data sources and methodology

### Responsiveness
- **Desktop:** Full dashboard with all features
- **Tablet:** Simplified view with key features
- **Mobile:** Essential information only

## 🚀 Implementation Steps

1. **Import Data:** Load all CSV files into Tableau
2. **Create Calculated Fields:** Distance categories, score ranges
3. **Build Visualizations:** Start with map, then add charts
4. **Add Interactivity:** Filters, tooltips, actions
5. **Design Layout:** Organize components logically
6. **Test Functionality:** Ensure all filters work correctly
7. **Optimize Performance:** Test with full dataset
8. **User Testing:** Get feedback from parents

## 📈 Success Metrics

- **Usability:** Parents can find schools within 5 minutes
- **Accuracy:** All distance calculations verified
- **Performance:** Dashboard loads within 10 seconds
- **User Satisfaction:** Positive feedback from test users
"""
    
    # Save instructions
    output_dir = 'dashboard_creation'
    os.makedirs(output_dir, exist_ok=True)
    
    with open(f'{output_dir}/dashboard_creation_instructions.md', 'w') as f:
        f.write(instructions)
    
    print(f"✅ Dashboard instructions saved to: {output_dir}/dashboard_creation_instructions.md")
    return instructions

def main():
    """Main dashboard data preparation function"""
    print("🎯 DASHBOARD DATA PREPARATION")
    print("="*60)
    
    # Step 1: Load final integrated data
    comprehensive_df, top_accessible, best_healthcare, best_metro, best_urban = load_final_integrated_data()
    
    # Step 2: Create dashboard insights
    insights = create_dashboard_insights(comprehensive_df)
    
    # Step 3: Create filtering categories
    filters = create_filtering_categories(comprehensive_df)
    
    # Step 4: Create sample visualizations
    visualizations = create_sample_visualizations(comprehensive_df)
    
    # Step 5: Create dashboard data files
    output_dir = create_dashboard_data_files(comprehensive_df, insights, filters, visualizations)
    
    # Step 6: Create dashboard instructions
    instructions = create_dashboard_instructions()
    
    # Final summary
    print("\n" + "="*60)
    print("🎉 DASHBOARD DATA PREPARATION COMPLETE!")
    print("="*60)
    
    print(f"✅ Main dataset: {len(comprehensive_df)} schools")
    print(f"✅ Insights created: {len(insights)} key metrics")
    print(f"✅ Filters created: {len(filters)} categories")
    print(f"✅ Visualizations: {len(visualizations)} sample charts")
    print(f"✅ Data files saved to: {output_dir}")
    
    print(f"\n🚀 Your dashboard data is ready!")
    print(f"📊 Import the CSV files into Tableau")
    print(f"📋 Follow the instructions in dashboard_creation_instructions.md")
    print(f"🎯 Create an amazing school selection platform!")
    
    return {
        'comprehensive_data': comprehensive_df,
        'insights': insights,
        'filters': filters,
        'visualizations': visualizations,
        'output_dir': output_dir
    }

if __name__ == "__main__":
    results = main()
