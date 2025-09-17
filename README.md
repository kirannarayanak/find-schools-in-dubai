# Dubai Schools Accessibility Analysis Platform

A comprehensive data science platform for analyzing school accessibility in Dubai, UAE. This project integrates multiple datasets including schools, communities, healthcare facilities, and metro stations to provide advanced spatial analysis and interactive visualizations.

## Features

### Comprehensive Data Integration
- **170 Schools** with complete profiles and accessibility metrics
- **226 Communities** with precise geographic coordinates
- **2,312 Healthcare Facilities** with distance calculations
- **540 Metro Stations** with accessibility analysis
- **Advanced Spatial Analysis** using Haversine distance calculations

### Interactive Dashboard
- **Real-time Interactive Map** with zoom, pan, and hover functionality
- **Advanced Filtering System** by school type, performance, geographic clusters
- **Small, Refined Markers** (3-7px) for clean visualization
- **Dubai-Focused Design** with proper boundaries and styling
- **Mobile Responsive** interface

### Advanced Analytics
- **Accessibility Scoring** for healthcare, metro, and community access
- **Urban Performance Metrics** with comprehensive scoring
- **Geographic Clustering** analysis
- **Distance-based Insights** and recommendations
- **Real-time Data Updates** with filtering

## Quick Start

### Prerequisites
```bash
pip install pandas numpy plotly dash dash-bootstrap-components geopy scikit-learn
```

### Launch Interactive Dashboard
```bash
# Option 1: Direct launch
python phase3_dashboard/advanced_dubai_map_dashboard.py

# Option 2: Using launcher
python phase3_dashboard/launch_interactive_dashboard.py
```

**Dashboard URL:** http://localhost:8053

### Alternative: Static Dashboard
```bash
open phase3_dashboard/static_dashboard.html
```

## Project Structure

```
F21RP/
├── datasets/                          # Raw datasets
│   ├── dubai_pop_2019.csv
│   ├── metro_venues_total.csv
│   ├── Private-Schools_Database_-(English).xlsx
│   └── Sheryan_Facility_Detail.csv
├── preprocessing/                     # Data cleaning scripts
│   ├── preprocess_dubai_population.py
│   ├── preprocess_healthcare_facilities.py
│   ├── preprocess_metro_venues.py
│   └── preprocess_private_schools.py
├── gis_integration/                   # GIS analysis pipeline
│   ├── 01_data_validation/
│   ├── 02_coordinate_standardization/
│   ├── 03_spatial_preparation/
│   ├── 04_distance_calculations/
│   └── 05_data_integration/
├── community_coordinates/             # Community mapping
│   └── community_coordinates/
├── phase2_integration/               # Comprehensive integration
│   └── phase2_integration/
└── phase3_dashboard/                 # Interactive dashboards
    ├── advanced_dubai_map_dashboard.py
    ├── futuristic_dashboard.py
    ├── simple_advanced_dashboard.py
    └── static_dashboard.html
```

## Key Insights

### Healthcare Accessibility
- **Average Distance:** 0.44 km to nearest healthcare facility
- **Excellent Access:** Schools within 0.5km of healthcare
- **Coverage:** 2,312 healthcare facilities analyzed

### Metro Accessibility
- **Average Distance:** 4.91 km to nearest metro station
- **Excellent Access:** Schools within 1km of metro
- **Coverage:** 540 metro stations mapped

### Community Integration
- **226 Communities** with precise coordinates
- **Population Analysis** within 5km radius
- **Accessibility Scoring** based on community proximity

## Technical Implementation

### Data Processing Pipeline
1. **Data Validation** - Quality assessment and cleaning
2. **Coordinate Standardization** - WGS84 (EPSG:4326) conversion
3. **Spatial Preparation** - Geographic data processing
4. **Distance Calculations** - Haversine formula implementation
5. **Data Integration** - Comprehensive profile creation

### Dashboard Technology Stack
- **Backend:** Python, Dash, Plotly
- **Frontend:** HTML5, CSS3, JavaScript
- **Maps:** Mapbox with interactive features
- **Styling:** Glassmorphism, neon themes, modern typography
- **Data:** Pandas, NumPy for processing

### Key Algorithms
- **Haversine Distance:** Accurate geographic distance calculations
- **K-Means Clustering:** Geographic cluster analysis
- **Accessibility Scoring:** Multi-factor scoring system
- **Real-time Filtering:** Dynamic data updates

## Sample Results

### Top Performing Schools
- **Rashid School for Boys:** 3.03 Urban Score
- **Healthcare Access:** 0.44km average
- **Metro Access:** 4.91km average
- **Community Integration:** High population density

### Geographic Distribution
- **Northern Cluster:** 34 schools
- **Central Cluster:** 45 schools  
- **Southern Cluster:** 28 schools
- **Eastern Cluster:** 38 schools
- **Western Cluster:** 25 schools

## Dashboard Features

### Interactive Map
- **Zoom & Pan:** Full map navigation
- **Hover Tooltips:** Rich school information
- **Small Markers:** Clean 3-7px visualization
- **Color Coding:** Accessibility score visualization
- **Dubai Boundaries:** Proper geographic context

### Advanced Filtering
- **School Type:** Filter by curriculum type
- **Performance Category:** Low/Medium/High/Excellent
- **Geographic Clusters:** Regional filtering
- **Distance Ranges:** Healthcare and metro proximity
- **Urban Scores:** Performance-based filtering

### Modern Design
- **Glassmorphism:** Frosted glass effects
- **Neon Colors:** Cyan, green, red, yellow theme
- **Dark Theme:** Professional appearance
- **Mobile Responsive:** Works on all devices
- **Smooth Animations:** Professional transitions

## Usage Examples

### For Urban Planners
- Identify underserved areas for new school construction
- Analyze healthcare and metro accessibility gaps
- Plan infrastructure improvements based on data

### For Parents
- Find schools with best accessibility scores
- Compare healthcare and metro proximity
- Filter by specific requirements and preferences

### For Researchers
- Access comprehensive spatial analysis data
- Study urban accessibility patterns
- Analyze educational infrastructure distribution

## Development

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

### Issues
Report bugs and request features through GitHub Issues

### License
MIT License - see LICENSE file for details

## Contact

**Project:** Dubai Schools Accessibility Analysis Platform  
**Repository:** https://github.com/kirannarayanak/find-schools-in-dubai.git  
**Dashboard:** http://localhost:8053 (when running)

---

## Project Status: COMPLETE

- **Phase 1:** Community Coordinates - 226 communities mapped
- **Phase 2:** Data Integration - All datasets combined
- **Phase 3:** Interactive Dashboard - Advanced visualization platform
- **Phase 4:** GitHub Repository - Code and documentation published

**Ready for production use and further development!**