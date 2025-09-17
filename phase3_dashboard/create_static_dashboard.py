#!/usr/bin/env python3
"""
Create Static HTML Dashboard
Creates a static HTML version of the dashboard for easy viewing
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.offline as pyo
import json
import os

def create_static_dashboard():
    """Create a static HTML dashboard"""
    print("🚀 Creating static HTML dashboard...")
    
    # Load data
    df = pd.read_csv('phase2_integration/phase2_integration/comprehensive_results/comprehensive_school_profiles_all_datasets.csv')
    print(f"✅ Loaded {len(df)} schools with complete profiles")
    
    # Create enhanced data structure
    df['healthcare_accessibility_tier'] = pd.cut(
        df['nearest_healthcare_distance_km_x'],
        bins=[0, 0.5, 1.0, 2.0, float('inf')],
        labels=['Excellent', 'Good', 'Moderate', 'Poor']
    )
    
    df['metro_accessibility_tier'] = pd.cut(
        df['nearest_metro_distance_km_x'],
        bins=[0, 1.0, 2.0, 5.0, float('inf')],
        labels=['Excellent', 'Good', 'Moderate', 'Poor']
    )
    
    df['community_accessibility_tier'] = pd.cut(
        df['nearest_community_distance_km'],
        bins=[0, 1.0, 2.0, 5.0, float('inf')],
        labels=['Excellent', 'Good', 'Moderate', 'Poor']
    )
    
    df['performance_category'] = pd.cut(
        df['final_urban_score'],
        bins=[0, 2.0, 3.0, 4.0, 5.0],
        labels=['Low', 'Medium', 'High', 'Excellent']
    )
    
    # Create insights
    insights = {
        'total_schools': len(df),
        'total_communities': 226,
        'total_healthcare': 2312,
        'total_metro': 540,
        'healthcare_excellent': len(df[df['healthcare_accessibility_tier'] == 'Excellent']),
        'metro_excellent': len(df[df['metro_accessibility_tier'] == 'Excellent']),
        'community_excellent': len(df[df['community_accessibility_tier'] == 'Excellent']),
        'avg_healthcare_distance': round(df['nearest_healthcare_distance_km_x'].mean(), 3),
        'avg_metro_distance': round(df['nearest_metro_distance_km_x'].mean(), 3),
        'avg_community_distance': round(df['nearest_community_distance_km'].mean(), 3),
        'avg_urban_score': round(df['final_urban_score'].mean(), 3)
    }
    
    # Create HTML content
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Dubai Schools Comprehensive Accessibility Dashboard</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 20px;
                background-color: #f5f5f5;
            }}
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                text-align: center;
                padding: 30px;
                margin-bottom: 30px;
                border-radius: 10px;
            }}
            .kpi-container {{
                display: flex;
                justify-content: space-around;
                margin-bottom: 30px;
                flex-wrap: wrap;
            }}
            .kpi-card {{
                background: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                text-align: center;
                margin: 10px;
                min-width: 200px;
            }}
            .kpi-number {{
                font-size: 2.5rem;
                font-weight: bold;
                margin: 0;
            }}
            .kpi-label {{
                font-size: 1.1rem;
                margin: 0;
                color: #666;
            }}
            .chart-container {{
                background: white;
                padding: 20px;
                margin: 20px 0;
                border-radius: 10px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            .chart-title {{
                text-align: center;
                margin-bottom: 20px;
                color: #333;
            }}
            .two-column {{
                display: flex;
                gap: 20px;
                flex-wrap: wrap;
            }}
            .two-column > div {{
                flex: 1;
                min-width: 400px;
            }}
            .insights {{
                background: white;
                padding: 20px;
                margin: 20px 0;
                border-radius: 10px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            .insight-item {{
                margin: 10px 0;
                padding: 10px;
                background: #f8f9fa;
                border-radius: 5px;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🏫 Dubai Schools Comprehensive Accessibility Dashboard</h1>
            <p>Advanced Analytics for Educational Infrastructure Planning</p>
        </div>
        
        <div class="kpi-container">
            <div class="kpi-card">
                <div class="kpi-number" style="color: #007bff;">{insights['total_schools']}</div>
                <div class="kpi-label">Total Schools</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-number" style="color: #28a745;">{insights['total_healthcare']}</div>
                <div class="kpi-label">Healthcare Facilities</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-number" style="color: #17a2b8;">{insights['total_metro']}</div>
                <div class="kpi-label">Metro Stations</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-number" style="color: #ffc107;">{insights['total_communities']}</div>
                <div class="kpi-label">Communities</div>
            </div>
        </div>
        
        <div class="insights">
            <h2>📊 Key Insights</h2>
            <div class="insight-item">
                <strong>Healthcare Access:</strong> {insights['healthcare_excellent']} schools ({round(insights['healthcare_excellent']/insights['total_schools']*100, 1)}%) have excellent access (≤0.5km)
            </div>
            <div class="insight-item">
                <strong>Metro Access:</strong> {insights['metro_excellent']} schools ({round(insights['metro_excellent']/insights['total_schools']*100, 1)}%) have excellent access (≤1km)
            </div>
            <div class="insight-item">
                <strong>Community Access:</strong> {insights['community_excellent']} schools ({round(insights['community_excellent']/insights['total_schools']*100, 1)}%) have excellent access (≤1km)
            </div>
            <div class="insight-item">
                <strong>Average Distances:</strong> Healthcare: {insights['avg_healthcare_distance']}km, Metro: {insights['avg_metro_distance']}km, Community: {insights['avg_community_distance']}km
            </div>
            <div class="insight-item">
                <strong>Average Urban Score:</strong> {insights['avg_urban_score']}/5.0
            </div>
        </div>
    """
    
    # Create charts
    charts = []
    
    # 1. Geographic Map
    map_fig = px.scatter_mapbox(
        df,
        lat='latitude',
        lon='longitude',
        color='comprehensive_accessibility_score',
        size='final_urban_score',
        hover_data=['school_name', 'type_of_school', 'nearest_healthcare_distance_km_x', 'nearest_metro_distance_km_x'],
        title='School Locations and Accessibility Scores',
        mapbox_style='open-street-map',
        zoom=10,
        color_continuous_scale='Viridis'
    )
    map_fig.update_layout(
        title_x=0.5,
        height=600,
        mapbox=dict(center=dict(lat=25.2048, lon=55.2708), zoom=10)
    )
    charts.append(('Geographic Distribution', map_fig))
    
    # 2. Healthcare Analysis
    hc_fig1 = px.histogram(
        df, 
        x='nearest_healthcare_distance_km_x',
        title='Healthcare Distance Distribution',
        labels={'nearest_healthcare_distance_km_x': 'Distance (km)', 'count': 'Number of Schools'},
        color_discrete_sequence=['#2E86AB']
    )
    hc_fig1.update_layout(xaxis_title="Distance to Nearest Healthcare (km)", yaxis_title="Number of Schools", title_x=0.5, height=400)
    
    hc_fig2 = px.pie(
        df['healthcare_accessibility_tier'].value_counts(),
        values=df['healthcare_accessibility_tier'].value_counts().values,
        names=df['healthcare_accessibility_tier'].value_counts().index,
        title='Healthcare Accessibility Tiers',
        color_discrete_sequence=['#28a745', '#ffc107', '#fd7e14', '#dc3545']
    )
    hc_fig2.update_layout(title_x=0.5, height=400)
    
    charts.append(('Healthcare Distance Distribution', hc_fig1))
    charts.append(('Healthcare Accessibility Tiers', hc_fig2))
    
    # 3. Metro Analysis
    metro_fig1 = px.histogram(
        df, 
        x='nearest_metro_distance_km_x',
        title='Metro Distance Distribution',
        labels={'nearest_metro_distance_km_x': 'Distance (km)', 'count': 'Number of Schools'},
        color_discrete_sequence=['#A23B72']
    )
    metro_fig1.update_layout(xaxis_title="Distance to Nearest Metro (km)", yaxis_title="Number of Schools", title_x=0.5, height=400)
    
    metro_fig2 = px.pie(
        df['metro_accessibility_tier'].value_counts(),
        values=df['metro_accessibility_tier'].value_counts().values,
        names=df['metro_accessibility_tier'].value_counts().index,
        title='Metro Accessibility Tiers',
        color_discrete_sequence=['#28a745', '#ffc107', '#fd7e14', '#dc3545']
    )
    metro_fig2.update_layout(title_x=0.5, height=400)
    
    charts.append(('Metro Distance Distribution', metro_fig1))
    charts.append(('Metro Accessibility Tiers', metro_fig2))
    
    # 4. Community Analysis
    comm_fig1 = px.histogram(
        df, 
        x='nearest_community_distance_km',
        title='Community Distance Distribution',
        labels={'nearest_community_distance_km': 'Distance (km)', 'count': 'Number of Schools'},
        color_discrete_sequence=['#F18F01']
    )
    comm_fig1.update_layout(xaxis_title="Distance to Nearest Community (km)", yaxis_title="Number of Schools", title_x=0.5, height=400)
    
    comm_fig2 = px.scatter(
        df,
        x='nearest_community_distance_km',
        y='population_within_1km',
        color='community_accessibility_tier',
        title='Community Distance vs Population',
        labels={'nearest_community_distance_km': 'Distance to Community (km)', 'population_within_1km': 'Population within 1km'}
    )
    comm_fig2.update_layout(title_x=0.5, height=400)
    
    charts.append(('Community Distance Distribution', comm_fig1))
    charts.append(('Community Distance vs Population', comm_fig2))
    
    # 5. Performance Analysis
    perf_fig1 = px.histogram(
        df, 
        x='final_urban_score',
        title='Urban Score Distribution',
        labels={'final_urban_score': 'Urban Score', 'count': 'Number of Schools'},
        color_discrete_sequence=['#6F42C1']
    )
    perf_fig1.update_layout(xaxis_title="Final Urban Score", yaxis_title="Number of Schools", title_x=0.5, height=400)
    
    perf_fig2 = px.pie(
        df['performance_category'].value_counts(),
        values=df['performance_category'].value_counts().values,
        names=df['performance_category'].value_counts().index,
        title='Performance Categories',
        color_discrete_sequence=['#dc3545', '#ffc107', '#28a745', '#007bff']
    )
    perf_fig2.update_layout(title_x=0.5, height=400)
    
    charts.append(('Urban Score Distribution', perf_fig1))
    charts.append(('Performance Categories', perf_fig2))
    
    # 6. Correlation Heatmap
    numeric_cols = [
        'nearest_healthcare_distance_km_x', 'nearest_metro_distance_km_x', 'nearest_community_distance_km',
        'comprehensive_accessibility_score', 'final_urban_score', 'healthcare_within_1km_x',
        'metro_within_1km_x', 'communities_within_1km', 'population_within_1km'
    ]
    corr_matrix = df[numeric_cols].corr()
    
    heatmap_fig = px.imshow(
        corr_matrix,
        text_auto=True,
        aspect="auto",
        title="Correlation Heatmap",
        color_continuous_scale='RdBu_r'
    )
    heatmap_fig.update_layout(title_x=0.5, height=500)
    charts.append(('Correlation Analysis', heatmap_fig))
    
    # Add charts to HTML
    for i, (title, fig) in enumerate(charts):
        if i % 2 == 0:
            html_content += '<div class="two-column">'
        
        html_content += f'''
        <div class="chart-container">
            <div class="chart-title">{title}</div>
            <div id="chart{i}"></div>
        </div>
        '''
        
        if i % 2 == 1 or i == len(charts) - 1:
            html_content += '</div>'
    
    # Add JavaScript for charts
    html_content += '''
    <script>
    '''
    
    for i, (title, fig) in enumerate(charts):
        chart_json = fig.to_json()
        html_content += f'''
        var chart{i} = {chart_json};
        Plotly.newPlot('chart{i}', chart{i}.data, chart{i}.layout);
        '''
    
    html_content += '''
    </script>
    </body>
    </html>
    '''
    
    # Save HTML file
    with open('phase3_dashboard/static_dashboard.html', 'w') as f:
        f.write(html_content)
    
    print("✅ Static HTML dashboard created!")
    print("📁 File saved as: phase3_dashboard/static_dashboard.html")
    print("🌐 Open the file in your browser to view the dashboard")
    
    return html_content

if __name__ == "__main__":
    create_static_dashboard()
