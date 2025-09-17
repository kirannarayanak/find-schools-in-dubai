#!/usr/bin/env python3
"""
Advanced Dubai Map Dashboard Creator
Creates the most sophisticated, interactive Dubai-focused dashboard with proper map styling
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
from dash import Dash, html, dcc, Input, Output, dash_table, State, callback
from datetime import datetime
import json
import os

class AdvancedDubaiMapDashboard:
    def __init__(self, data_path):
        self.data_path = data_path
        self.df = None
        self.app = None
        self.insights = {}
        
    def load_data(self):
        """Load comprehensive integrated data"""
        print("Loading comprehensive integrated data...")
        self.df = pd.read_csv(self.data_path)
        print(f"Loaded {len(self.df)} schools with complete profiles")
        
        # Create enhanced data structure
        self.df['healthcare_accessibility_tier'] = pd.cut(
            self.df['nearest_healthcare_distance_km_x'],
            bins=[0, 0.5, 1.0, 2.0, float('inf')],
            labels=['Excellent', 'Good', 'Moderate', 'Poor']
        )
        
        self.df['metro_accessibility_tier'] = pd.cut(
            self.df['nearest_metro_distance_km_x'],
            bins=[0, 1.0, 2.0, 5.0, float('inf')],
            labels=['Excellent', 'Good', 'Moderate', 'Poor']
        )
        
        self.df['community_accessibility_tier'] = pd.cut(
            self.df['nearest_community_distance_km'],
            bins=[0, 1.0, 2.0, 5.0, float('inf')],
            labels=['Excellent', 'Good', 'Moderate', 'Poor']
        )
        
        self.df['performance_category'] = pd.cut(
            self.df['final_urban_score'],
            bins=[0, 2.0, 3.0, 4.0, 5.0],
            labels=['Low', 'Medium', 'High', 'Excellent']
        )
        
        # Add geographic clusters
        from sklearn.cluster import KMeans
        coords = self.df[['latitude', 'longitude']].dropna()
        if len(coords) > 0:
            kmeans = KMeans(n_clusters=5, random_state=42)
            clusters = kmeans.fit_predict(coords)
            self.df['geographic_cluster'] = clusters
            self.df['geographic_cluster_label'] = self.df['geographic_cluster'].map({
                0: 'Northern Cluster',
                1: 'Central Cluster', 
                2: 'Southern Cluster',
                3: 'Eastern Cluster',
                4: 'Western Cluster'
            })
        
        return self.df
    
    def create_insights(self):
        """Create comprehensive insights"""
        print("Creating comprehensive insights...")
        
        self.insights = {
            'total_schools': len(self.df),
            'total_communities': 226,
            'total_healthcare': 2312,
            'total_metro': 540,
            
            'healthcare_stats': {
                'mean_distance': round(self.df['nearest_healthcare_distance_km_x'].mean(), 3),
                'excellent_access': len(self.df[self.df['healthcare_accessibility_tier'] == 'Excellent']),
                'good_access': len(self.df[self.df['healthcare_accessibility_tier'] == 'Good']),
                'moderate_access': len(self.df[self.df['healthcare_accessibility_tier'] == 'Moderate']),
                'poor_access': len(self.df[self.df['healthcare_accessibility_tier'] == 'Poor'])
            },
            
            'metro_stats': {
                'mean_distance': round(self.df['nearest_metro_distance_km_x'].mean(), 3),
                'excellent_access': len(self.df[self.df['metro_accessibility_tier'] == 'Excellent']),
                'good_access': len(self.df[self.df['metro_accessibility_tier'] == 'Good']),
                'moderate_access': len(self.df[self.df['metro_accessibility_tier'] == 'Moderate']),
                'poor_access': len(self.df[self.df['metro_accessibility_tier'] == 'Poor'])
            },
            
            'community_stats': {
                'mean_distance': round(self.df['nearest_community_distance_km'].mean(), 3),
                'excellent_access': len(self.df[self.df['community_accessibility_tier'] == 'Excellent']),
                'good_access': len(self.df[self.df['community_accessibility_tier'] == 'Good']),
                'moderate_access': len(self.df[self.df['community_accessibility_tier'] == 'Moderate']),
                'poor_access': len(self.df[self.df['community_accessibility_tier'] == 'Poor'])
            },
            
            'performance_stats': {
                'mean_urban_score': round(self.df['final_urban_score'].mean(), 3),
                'mean_accessibility_score': round(self.df['comprehensive_accessibility_score'].mean(), 3),
                'excellent_performance': len(self.df[self.df['performance_category'] == 'Excellent']),
                'high_performance': len(self.df[self.df['performance_category'] == 'High']),
                'medium_performance': len(self.df[self.df['performance_category'] == 'Medium']),
                'low_performance': len(self.df[self.df['performance_category'] == 'Low'])
            }
        }
        
        print("Insights created!")
        return self.insights
    
    def create_modern_kpi_cards(self):
        """Create modern KPI cards with better styling"""
        return [
            html.Div([
                html.Div([
                    html.Div([
                        html.I(className="fas fa-school", style={'font-size': '2.5rem', 'color': '#00d4ff', 'margin-bottom': '15px'}),
                        html.H2(f"{self.insights['total_schools']}", style={'color': '#00d4ff', 'font-size': '3.5rem', 'margin': '0', 'font-weight': '800', 'text-shadow': '0 0 30px rgba(0, 212, 255, 0.6)'}),
                        html.P("Total Schools", style={'margin': '0', 'font-size': '1.3rem', 'color': '#e0e0e0', 'font-weight': '400'})
                    ], style={'text-align': 'center', 'padding': '35px'})
                ], style={
                    'background': 'linear-gradient(135deg, rgba(0, 212, 255, 0.15) 0%, rgba(0, 100, 200, 0.15) 100%)',
                    'border': '2px solid rgba(0, 212, 255, 0.4)',
                    'border-radius': '25px',
                    'box-shadow': '0 15px 40px rgba(0, 212, 255, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.2)',
                    'backdrop-filter': 'blur(15px)',
                    'position': 'relative',
                    'overflow': 'hidden',
                    'transition': 'all 0.3s ease'
                })
            ], style={'width': '23%', 'display': 'inline-block', 'margin': '1%'}),
            
            html.Div([
                html.Div([
                    html.Div([
                        html.I(className="fas fa-hospital", style={'font-size': '2.5rem', 'color': '#00ff88', 'margin-bottom': '15px'}),
                        html.H2(f"{self.insights['total_healthcare']}", style={'color': '#00ff88', 'font-size': '3.5rem', 'margin': '0', 'font-weight': '800', 'text-shadow': '0 0 30px rgba(0, 255, 136, 0.6)'}),
                        html.P("Healthcare Facilities", style={'margin': '0', 'font-size': '1.3rem', 'color': '#e0e0e0', 'font-weight': '400'})
                    ], style={'text-align': 'center', 'padding': '35px'})
                ], style={
                    'background': 'linear-gradient(135deg, rgba(0, 255, 136, 0.15) 0%, rgba(0, 200, 100, 0.15) 100%)',
                    'border': '2px solid rgba(0, 255, 136, 0.4)',
                    'border-radius': '25px',
                    'box-shadow': '0 15px 40px rgba(0, 255, 136, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.2)',
                    'backdrop-filter': 'blur(15px)',
                    'position': 'relative',
                    'overflow': 'hidden',
                    'transition': 'all 0.3s ease'
                })
            ], style={'width': '23%', 'display': 'inline-block', 'margin': '1%'}),
            
            html.Div([
                html.Div([
                    html.Div([
                        html.I(className="fas fa-subway", style={'font-size': '2.5rem', 'color': '#ff6b6b', 'margin-bottom': '15px'}),
                        html.H2(f"{self.insights['total_metro']}", style={'color': '#ff6b6b', 'font-size': '3.5rem', 'margin': '0', 'font-weight': '800', 'text-shadow': '0 0 30px rgba(255, 107, 107, 0.6)'}),
                        html.P("Metro Stations", style={'margin': '0', 'font-size': '1.3rem', 'color': '#e0e0e0', 'font-weight': '400'})
                    ], style={'text-align': 'center', 'padding': '35px'})
                ], style={
                    'background': 'linear-gradient(135deg, rgba(255, 107, 107, 0.15) 0%, rgba(200, 50, 50, 0.15) 100%)',
                    'border': '2px solid rgba(255, 107, 107, 0.4)',
                    'border-radius': '25px',
                    'box-shadow': '0 15px 40px rgba(255, 107, 107, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.2)',
                    'backdrop-filter': 'blur(15px)',
                    'position': 'relative',
                    'overflow': 'hidden',
                    'transition': 'all 0.3s ease'
                })
            ], style={'width': '23%', 'display': 'inline-block', 'margin': '1%'}),
            
            html.Div([
                html.Div([
                    html.Div([
                        html.I(className="fas fa-users", style={'font-size': '2.5rem', 'color': '#ffd93d', 'margin-bottom': '15px'}),
                        html.H2(f"{self.insights['total_communities']}", style={'color': '#ffd93d', 'font-size': '3.5rem', 'margin': '0', 'font-weight': '800', 'text-shadow': '0 0 30px rgba(255, 217, 61, 0.6)'}),
                        html.P("Communities", style={'margin': '0', 'font-size': '1.3rem', 'color': '#e0e0e0', 'font-weight': '400'})
                    ], style={'text-align': 'center', 'padding': '35px'})
                ], style={
                    'background': 'linear-gradient(135deg, rgba(255, 217, 61, 0.15) 0%, rgba(200, 150, 0, 0.15) 100%)',
                    'border': '2px solid rgba(255, 217, 61, 0.4)',
                    'border-radius': '25px',
                    'box-shadow': '0 15px 40px rgba(255, 217, 61, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.2)',
                    'backdrop-filter': 'blur(15px)',
                    'position': 'relative',
                    'overflow': 'hidden',
                    'transition': 'all 0.3s ease'
                })
            ], style={'width': '23%', 'display': 'inline-block', 'margin': '1%'})
        ]
    
    def create_advanced_filters(self):
        """Create advanced filtering controls with better styling"""
        return html.Div([
            html.Div([
                html.H4("🔍 Advanced Filters", style={'color': '#00d4ff', 'margin-bottom': '25px', 'font-weight': '700', 'font-size': '1.4rem'}),
                
                # School Type Filter
                html.Div([
                    html.Label("School Type:", style={'color': '#ffffff', 'font-weight': '600', 'margin-bottom': '8px', 'font-size': '1.1rem'}),
                    dcc.Dropdown(
                        id='school-type-filter',
                        options=[{'label': 'All Types', 'value': 'All'}] + 
                               [{'label': school_type, 'value': school_type} for school_type in sorted(self.df['type_of_school'].unique())],
                        value='All',
                        style={
                            'background-color': 'rgba(255, 255, 255, 0.1)', 
                            'border': '2px solid rgba(0, 212, 255, 0.3)',
                            'border-radius': '10px',
                            'color': 'white'
                        }
                    )
                ], style={'margin-bottom': '20px'}),
                
                # Performance Category Filter
                html.Div([
                    html.Label("Performance Category:", style={'color': '#ffffff', 'font-weight': '600', 'margin-bottom': '8px', 'font-size': '1.1rem'}),
                    dcc.Dropdown(
                        id='performance-filter',
                        options=[{'label': 'All Categories', 'value': 'All'}] + 
                               [{'label': cat, 'value': cat} for cat in sorted(self.df['performance_category'].unique())],
                        value='All',
                        style={
                            'background-color': 'rgba(255, 255, 255, 0.1)', 
                            'border': '2px solid rgba(0, 212, 255, 0.3)',
                            'border-radius': '10px',
                            'color': 'white'
                        }
                    )
                ], style={'margin-bottom': '20px'}),
                
                # Geographic Cluster Filter
                html.Div([
                    html.Label("Geographic Cluster:", style={'color': '#ffffff', 'font-weight': '600', 'margin-bottom': '8px', 'font-size': '1.1rem'}),
                    dcc.Dropdown(
                        id='cluster-filter',
                        options=[{'label': 'All Clusters', 'value': 'All'}] + 
                               [{'label': cluster, 'value': cluster} for cluster in sorted(self.df['geographic_cluster_label'].unique())],
                        value='All',
                        style={
                            'background-color': 'rgba(255, 255, 255, 0.1)', 
                            'border': '2px solid rgba(0, 212, 255, 0.3)',
                            'border-radius': '10px',
                            'color': 'white'
                        }
                    )
                ], style={'margin-bottom': '20px'}),
                
                # Distance Range Filters
                html.Div([
                    html.Label("Healthcare Distance Range (km):", style={'color': '#ffffff', 'font-weight': '600', 'margin-bottom': '8px', 'font-size': '1.1rem'}),
                    dcc.RangeSlider(
                        id='healthcare-distance-slider',
                        min=0,
                        max=5,
                        step=0.1,
                        value=[0, 5],
                        marks={i: f'{i}km' for i in range(0, 6)},
                        tooltip={"placement": "bottom", "always_visible": True},
                        className="custom-slider"
                    )
                ], style={'margin-bottom': '20px'}),
                
                html.Div([
                    html.Label("Metro Distance Range (km):", style={'color': '#ffffff', 'font-weight': '600', 'margin-bottom': '8px', 'font-size': '1.1rem'}),
                    dcc.RangeSlider(
                        id='metro-distance-slider',
                        min=0,
                        max=15,
                        step=0.5,
                        value=[0, 15],
                        marks={i: f'{i}km' for i in range(0, 16, 3)},
                        tooltip={"placement": "bottom", "always_visible": True},
                        className="custom-slider"
                    )
                ], style={'margin-bottom': '20px'}),
                
                # Urban Score Range
                html.Div([
                    html.Label("Urban Score Range:", style={'color': '#ffffff', 'font-weight': '600', 'margin-bottom': '8px', 'font-size': '1.1rem'}),
                    dcc.RangeSlider(
                        id='urban-score-slider',
                        min=0,
                        max=5,
                        step=0.1,
                        value=[0, 5],
                        marks={i: f'{i}' for i in range(0, 6)},
                        tooltip={"placement": "bottom", "always_visible": True},
                        className="custom-slider"
                    )
                ], style={'margin-bottom': '25px'}),
                
                # Reset Button
                html.Button(
                    "Reset Filters",
                    id="reset-filters",
                    style={
                        'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                        'color': 'white',
                        'border': 'none',
                        'padding': '15px 25px',
                        'border-radius': '30px',
                        'cursor': 'pointer',
                        'font-weight': '700',
                        'width': '100%',
                        'font-size': '1.1rem',
                        'box-shadow': '0 8px 25px rgba(102, 126, 234, 0.4)',
                        'transition': 'all 0.3s ease'
                    }
                )
                
            ], style={
                'background': 'rgba(0, 0, 0, 0.4)',
                'padding': '30px',
                'border-radius': '20px',
                'border': '2px solid rgba(0, 212, 255, 0.3)',
                'backdrop-filter': 'blur(20px)',
                'box-shadow': '0 20px 50px rgba(0, 0, 0, 0.3)'
            })
        ], style={'width': '25%', 'display': 'inline-block', 'vertical-align': 'top', 'margin-right': '25px'})
    
    def create_sophisticated_dubai_map(self):
        """Create a sophisticated Dubai-focused map with proper styling"""
        # Create base map with Dubai-specific styling
        fig = go.Figure()
        
        # Add Dubai boundary polygon to highlight Dubai area
        dubai_boundary = [
            [24.8, 54.8], [24.8, 55.6], [25.4, 55.6], [25.4, 54.8], [24.8, 54.8]
        ]
        
        # Add Dubai boundary as a filled area to highlight Dubai
        fig.add_trace(go.Scattermapbox(
            lat=[point[0] for point in dubai_boundary],
            lon=[point[1] for point in dubai_boundary],
            mode='lines',
            line=dict(color='rgba(255, 255, 255, 0.8)', width=2),
            fill='toself',
            fillcolor='rgba(255, 255, 255, 0.1)',
            name='Dubai Area',
            showlegend=False
        ))
        
        # Add school locations with sophisticated styling
        fig.add_trace(go.Scattermapbox(
            lat=self.df['latitude'],
            lon=self.df['longitude'],
            mode='markers',
            marker=dict(
                size=self.df['final_urban_score'] * 3 + 4,  # Much smaller, refined markers
                color=self.df['comprehensive_accessibility_score'],
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(
                    title=dict(
                        text="Accessibility Score",
                        font=dict(size=14, color='white')
                    ),
                    tickmode="array",
                    tickvals=[4, 4.2, 4.4, 4.6, 4.8, 5.0],
                    ticktext=["4.0", "4.2", "4.4", "4.6", "4.8", "5.0"],
                    tickfont=dict(color='white', size=12),
                    bgcolor='rgba(0, 0, 0, 0.5)',
                    bordercolor='rgba(255, 255, 255, 0.3)',
                    borderwidth=1
                ),
                opacity=0.85,
                symbol='circle'
            ),
            text=self.df['school_name'],
            hovertemplate='<b>%{text}</b><br>' +
                         'Type: ' + self.df['type_of_school'] + '<br>' +
                         'Healthcare: %{customdata[0]:.2f}km<br>' +
                         'Metro: %{customdata[1]:.2f}km<br>' +
                         'Community: %{customdata[2]:.2f}km<br>' +
                         'Urban Score: %{customdata[3]:.2f}<br>' +
                         'Accessibility: %{marker.color:.2f}<br>' +
                         '<extra></extra>',
            customdata=list(zip(
                self.df['nearest_healthcare_distance_km_x'],
                self.df['nearest_metro_distance_km_x'],
                self.df['nearest_community_distance_km'],
                self.df['final_urban_score']
            )),
            name="Schools",
            showlegend=False
        ))
        
        # Add metro stations
        metro_locations = [
            {'lat': 25.2048, 'lon': 55.2708, 'name': 'Dubai Mall'},
            {'lat': 25.1972, 'lon': 55.2744, 'name': 'Burj Khalifa/Dubai Mall'},
            {'lat': 25.1889, 'lon': 55.2744, 'name': 'Business Bay'},
            {'lat': 25.1806, 'lon': 55.2744, 'name': 'Noor Bank'},
            {'lat': 25.1722, 'lon': 55.2744, 'name': 'First Abu Dhabi Bank'},
            {'lat': 25.1639, 'lon': 55.2744, 'name': 'Sharaf DG'},
            {'lat': 25.1556, 'lon': 55.2744, 'name': 'Oud Metha'},
            {'lat': 25.1472, 'lon': 55.2744, 'name': 'Dubai Healthcare City'},
            {'lat': 25.1389, 'lon': 55.2744, 'name': 'Al Jadaf'},
            {'lat': 25.1306, 'lon': 55.2744, 'name': 'Creek'},
        ]
        
        fig.add_trace(go.Scattermapbox(
            lat=[station['lat'] for station in metro_locations],
            lon=[station['lon'] for station in metro_locations],
            mode='markers',
            marker=dict(
                size=8,
                color='#ff6b6b',
                symbol='rail',
                opacity=0.8
            ),
            text=[station['name'] for station in metro_locations],
            hovertemplate='<b>%{text}</b><br>Metro Station<extra></extra>',
            name="Metro Stations",
            showlegend=False
        ))
        
        # Update layout with dark theme - Dubai highlighted, rest black
        fig.update_layout(
            mapbox=dict(
                style="dark",  # Dark theme - areas outside Dubai will be black
                center=dict(lat=25.2048, lon=55.2708),
                zoom=10.5,
                bearing=0,
                pitch=0,
                accesstoken="pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw"  # Public token for interactivity
            ),
            title=dict(
                text="Dubai Schools Interactive Accessibility Map",
                font=dict(size=28, color='#00d4ff', family='Inter'),
                x=0.5,
                y=0.95
            ),
            height=750,
            margin=dict(l=0, r=0, t=80, b=0),
            paper_bgcolor='black',  # Black background
            plot_bgcolor='black',   # Black background
            font=dict(family="Inter, sans-serif", color="white"),
            showlegend=False
        )
        
        return fig
    
    def create_advanced_charts(self):
        """Create advanced interactive charts with better styling"""
        charts = {}
        
        # 1. Healthcare Analysis with modern styling
        hc_fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Distance Distribution', 'Accessibility Tiers', 'School Type Analysis', 'Performance by Tier'),
            specs=[[{"type": "histogram"}, {"type": "pie"}],
                   [{"type": "bar"}, {"type": "bar"}]],
            vertical_spacing=0.12,
            horizontal_spacing=0.1
        )
        
        # Distance distribution
        hc_fig.add_trace(
            go.Histogram(
                x=self.df['nearest_healthcare_distance_km_x'],
                name='Healthcare Distance',
                marker_color='#00ff88',
                opacity=0.8,
                nbinsx=20
            ),
            row=1, col=1
        )
        
        # Accessibility tiers pie
        tier_counts = self.df['healthcare_accessibility_tier'].value_counts()
        hc_fig.add_trace(
            go.Pie(
                labels=tier_counts.index,
                values=tier_counts.values,
                name="Healthcare Tiers",
                marker_colors=['#00ff88', '#ffd93d', '#ff6b6b', '#ff4757'],
                textinfo='label+percent',
                textfont_size=12
            ),
            row=1, col=2
        )
        
        # School type analysis
        school_type_analysis = self.df.groupby('type_of_school')['nearest_healthcare_distance_km_x'].mean().sort_values()
        hc_fig.add_trace(
            go.Bar(
                x=school_type_analysis.index,
                y=school_type_analysis.values,
                name='Avg Distance by Type',
                marker_color='#00d4ff',
                opacity=0.8
            ),
            row=2, col=1
        )
        
        # Performance by tier
        perf_by_tier = self.df.groupby('healthcare_accessibility_tier')['final_urban_score'].mean()
        hc_fig.add_trace(
            go.Bar(
                x=perf_by_tier.index,
                y=perf_by_tier.values,
                name='Urban Score by Tier',
                marker_color='#ff6b6b',
                opacity=0.8
            ),
            row=2, col=2
        )
        
        hc_fig.update_layout(
            title=dict(
                text="🏥 Advanced Healthcare Analysis",
                font=dict(size=24, color='#00ff88', family='Inter'),
                x=0.5
            ),
            height=650,
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter, sans-serif", color="white", size=12)
        )
        
        charts['healthcare'] = hc_fig
        
        # 2. Metro Analysis
        metro_fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Distance Distribution', 'Accessibility Tiers', 'Correlation Analysis', 'Performance by Tier'),
            specs=[[{"type": "histogram"}, {"type": "pie"}],
                   [{"type": "scatter"}, {"type": "bar"}]],
            vertical_spacing=0.12,
            horizontal_spacing=0.1
        )
        
        # Distance distribution
        metro_fig.add_trace(
            go.Histogram(
                x=self.df['nearest_metro_distance_km_x'],
                name='Metro Distance',
                marker_color='#ff6b6b',
                opacity=0.8,
                nbinsx=20
            ),
            row=1, col=1
        )
        
        # Accessibility tiers pie
        metro_tier_counts = self.df['metro_accessibility_tier'].value_counts()
        metro_fig.add_trace(
            go.Pie(
                labels=metro_tier_counts.index,
                values=metro_tier_counts.values,
                name="Metro Tiers",
                marker_colors=['#ff6b6b', '#ffd93d', '#ffa726', '#ff5722'],
                textinfo='label+percent',
                textfont_size=12
            ),
            row=1, col=2
        )
        
        # Correlation scatter
        metro_fig.add_trace(
            go.Scatter(
                x=self.df['nearest_healthcare_distance_km_x'],
                y=self.df['nearest_metro_distance_km_x'],
                mode='markers',
                marker=dict(
                    color=self.df['comprehensive_accessibility_score'],
                    colorscale='Viridis',
                    size=8,
                    opacity=0.7
                ),
                name='Healthcare vs Metro',
                text=self.df['school_name'],
                hovertemplate='<b>%{text}</b><br>Healthcare: %{x:.2f}km<br>Metro: %{y:.2f}km<extra></extra>'
            ),
            row=2, col=1
        )
        
        # Performance by tier
        metro_perf_by_tier = self.df.groupby('metro_accessibility_tier')['final_urban_score'].mean()
        metro_fig.add_trace(
            go.Bar(
                x=metro_perf_by_tier.index,
                y=metro_perf_by_tier.values,
                name='Urban Score by Metro Tier',
                marker_color='#00d4ff',
                opacity=0.8
            ),
            row=2, col=2
        )
        
        metro_fig.update_layout(
            title=dict(
                text="🚇 Advanced Metro Analysis",
                font=dict(size=24, color='#ff6b6b', family='Inter'),
                x=0.5
            ),
            height=650,
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter, sans-serif", color="white", size=12)
        )
        
        charts['metro'] = metro_fig
        
        return charts
    
    def create_dashboard_layout(self):
        """Create the sophisticated dashboard layout"""
        print("Creating sophisticated dashboard layout...")
        
        # Load data and create insights
        self.load_data()
        self.create_insights()
        
        # Create components
        kpi_cards = self.create_modern_kpi_cards()
        filters = self.create_advanced_filters()
        map_fig = self.create_sophisticated_dubai_map()
        charts = self.create_advanced_charts()
        
        layout = html.Div([
            # Custom CSS
            html.Link(
                rel="stylesheet",
                href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"
            ),
            html.Link(
                rel="stylesheet",
                href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap"
            ),
            
            
            # Header
            html.Div([
                html.Div([
                    html.H1("🏫 Dubai Schools Advanced Accessibility Dashboard", 
                           style={'color': '#00d4ff', 'margin': '0', 'font-size': '3rem', 'font-weight': '800', 'text-shadow': '0 0 40px rgba(0, 212, 255, 0.6)'}),
                    html.P("Sophisticated Analytics for Educational Infrastructure Planning", 
                          style={'color': '#b0b0b0', 'margin': '15px 0 0 0', 'font-size': '1.4rem', 'font-weight': '400'})
                ], style={'text-align': 'center', 'padding': '50px 20px'})
            ], style={
                'background': 'linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 50%, #16213e 100%)',
                'margin-bottom': '40px',
                'border-radius': '0 0 40px 40px',
                'box-shadow': '0 15px 50px rgba(0, 0, 0, 0.6)'
            }),
            
            # Main content
            html.Div([
                # KPI Cards
                html.Div(kpi_cards, style={'margin-bottom': '50px'}),
                
                # Filters and Map Row
                html.Div([
                    filters,
                    html.Div([
                        dcc.Graph(
                            id='main-map',
                            figure=map_fig,
                            style={'height': '750px', 'border-radius': '20px', 'overflow': 'hidden', 'box-shadow': '0 20px 60px rgba(0, 0, 0, 0.4)'}
                        )
                    ], style={'width': '73%', 'display': 'inline-block'})
                ], style={'margin-bottom': '50px'}),
                
                # Advanced Analytics Tabs
                dcc.Tabs([
                    dcc.Tab(
                        label="🏥 Healthcare Analysis",
                        children=[
                            dcc.Graph(
                                id='healthcare-charts',
                                figure=charts['healthcare'],
                                style={'height': '650px', 'border-radius': '20px', 'overflow': 'hidden', 'box-shadow': '0 15px 40px rgba(0, 0, 0, 0.3)'}
                            )
                        ],
                        style={'background': 'rgba(0, 255, 136, 0.1)', 'border-radius': '15px', 'margin': '8px'},
                        selected_style={'background': 'rgba(0, 255, 136, 0.2)', 'border-radius': '15px', 'margin': '8px'}
                    ),
                    dcc.Tab(
                        label="🚇 Metro Analysis",
                        children=[
                            dcc.Graph(
                                id='metro-charts',
                                figure=charts['metro'],
                                style={'height': '650px', 'border-radius': '20px', 'overflow': 'hidden', 'box-shadow': '0 15px 40px rgba(0, 0, 0, 0.3)'}
                            )
                        ],
                        style={'background': 'rgba(255, 107, 107, 0.1)', 'border-radius': '15px', 'margin': '8px'},
                        selected_style={'background': 'rgba(255, 107, 107, 0.2)', 'border-radius': '15px', 'margin': '8px'}
                    )
                ], style={'margin-top': '30px'})
                
            ], style={'padding': '0 25px', 'max-width': '1600px', 'margin': '0 auto'})
            
        ], style={
            'background': 'linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 50%, #16213e 100%)',
            'min-height': '100vh',
            'font-family': 'Inter, sans-serif',
            'color': 'white'
        })
        
        return layout
    
    def create_dashboard_app(self):
        """Create and configure the sophisticated Dash app"""
        print("Creating sophisticated Dubai map dashboard...")
        
        # Initialize Dash app
        self.app = Dash(__name__)
        
        # Set app title
        self.app.title = "Dubai Schools Advanced Map Dashboard"
        
        # Create layout
        self.app.layout = self.create_dashboard_layout()
        
        # Add callbacks for interactivity
        self.add_callbacks()
        
        print("Sophisticated dashboard app created!")
        return self.app
    
    def add_callbacks(self):
        """Add interactive callbacks"""
        @self.app.callback(
            [Output('main-map', 'figure'),
             Output('healthcare-charts', 'figure'),
             Output('metro-charts', 'figure')],
            [Input('school-type-filter', 'value'),
             Input('performance-filter', 'value'),
             Input('cluster-filter', 'value'),
             Input('healthcare-distance-slider', 'value'),
             Input('metro-distance-slider', 'value'),
             Input('urban-score-slider', 'value'),
             Input('reset-filters', 'n_clicks')]
        )
        def update_dashboard(school_type, performance, cluster, hc_distance, metro_distance, urban_score, reset_clicks):
            # Filter data based on inputs
            filtered_df = self.df.copy()
            
            if school_type != 'All':
                filtered_df = filtered_df[filtered_df['type_of_school'] == school_type]
            
            if performance != 'All':
                filtered_df = filtered_df[filtered_df['performance_category'] == performance]
            
            if cluster != 'All':
                filtered_df = filtered_df[filtered_df['geographic_cluster_label'] == cluster]
            
            # Distance filters
            filtered_df = filtered_df[
                (filtered_df['nearest_healthcare_distance_km_x'] >= hc_distance[0]) &
                (filtered_df['nearest_healthcare_distance_km_x'] <= hc_distance[1]) &
                (filtered_df['nearest_metro_distance_km_x'] >= metro_distance[0]) &
                (filtered_df['nearest_metro_distance_km_x'] <= metro_distance[1]) &
                (filtered_df['final_urban_score'] >= urban_score[0]) &
                (filtered_df['final_urban_score'] <= urban_score[1])
            ]
            
            # Update map
            map_fig = self.create_sophisticated_dubai_map()
            if len(filtered_df) > 0:
                map_fig.data[1].lat = filtered_df['latitude']
                map_fig.data[1].lon = filtered_df['longitude']
                map_fig.data[1].marker.size = filtered_df['final_urban_score'] * 3 + 4
                map_fig.data[1].marker.color = filtered_df['comprehensive_accessibility_score']
                map_fig.data[1].text = filtered_df['school_name']
                map_fig.data[1].customdata = list(zip(
                    filtered_df['nearest_healthcare_distance_km_x'],
                    filtered_df['nearest_metro_distance_km_x'],
                    filtered_df['nearest_community_distance_km'],
                    filtered_df['final_urban_score']
                ))
            
            # Update charts
            charts = self.create_advanced_charts()
            
            return map_fig, charts['healthcare'], charts['metro']
    
    def run_dashboard(self, debug=True, port=8053):
        """Run the dashboard"""
        print("Starting sophisticated Dubai map dashboard server...")
        print(f"Dashboard will be available at: http://localhost:{port}")
        print("Press Ctrl+C to stop the server")
        
        self.app.run(debug=debug, port=port)

def main():
    """Main execution function"""
    print("PHASE 3: SOPHISTICATED DUBAI MAP DASHBOARD CREATION")
    print("=" * 60)
    
    # Initialize dashboard creator
    dashboard_creator = AdvancedDubaiMapDashboard(
        'phase2_integration/phase2_integration/comprehensive_results/comprehensive_school_profiles_all_datasets.csv'
    )
    
    # Create and run dashboard
    app = dashboard_creator.create_dashboard_app()
    dashboard_creator.run_dashboard()

if __name__ == "__main__":
    main()
