#!/usr/bin/env python3
"""
Futuristic Advanced Dashboard Creator
Creates the most modern, interactive, and visually stunning dashboard
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

class FuturisticDashboard:
    def __init__(self, data_path):
        self.data_path = data_path
        self.df = None
        self.app = None
        self.insights = {}
        
    def load_data(self):
        """Load comprehensive integrated data"""
        print("📊 Loading comprehensive integrated data...")
        self.df = pd.read_csv(self.data_path)
        print(f"✅ Loaded {len(self.df)} schools with complete profiles")
        
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
        print("🧠 Creating comprehensive insights...")
        
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
        
        print("✅ Insights created!")
        return self.insights
    
    def create_futuristic_kpi_cards(self):
        """Create futuristic KPI cards"""
        return [
            html.Div([
                html.Div([
                    html.Div([
                        html.I(className="fas fa-school", style={'font-size': '2rem', 'color': '#00d4ff', 'margin-bottom': '10px'}),
                        html.H2(f"{self.insights['total_schools']}", style={'color': '#00d4ff', 'font-size': '3rem', 'margin': '0', 'font-weight': '700', 'text-shadow': '0 0 20px rgba(0, 212, 255, 0.5)'}),
                        html.P("Total Schools", style={'margin': '0', 'font-size': '1.2rem', 'color': '#b0b0b0', 'font-weight': '300'})
                    ], style={'text-align': 'center', 'padding': '30px'})
                ], style={
                    'background': 'linear-gradient(135deg, rgba(0, 212, 255, 0.1) 0%, rgba(0, 100, 200, 0.1) 100%)',
                    'border': '1px solid rgba(0, 212, 255, 0.3)',
                    'border-radius': '20px',
                    'box-shadow': '0 8px 32px rgba(0, 212, 255, 0.2)',
                    'backdrop-filter': 'blur(10px)',
                    'position': 'relative',
                    'overflow': 'hidden'
                })
            ], style={'width': '23%', 'display': 'inline-block', 'margin': '1%'}),
            
            html.Div([
                html.Div([
                    html.Div([
                        html.I(className="fas fa-hospital", style={'font-size': '2rem', 'color': '#00ff88', 'margin-bottom': '10px'}),
                        html.H2(f"{self.insights['total_healthcare']}", style={'color': '#00ff88', 'font-size': '3rem', 'margin': '0', 'font-weight': '700', 'text-shadow': '0 0 20px rgba(0, 255, 136, 0.5)'}),
                        html.P("Healthcare Facilities", style={'margin': '0', 'font-size': '1.2rem', 'color': '#b0b0b0', 'font-weight': '300'})
                    ], style={'text-align': 'center', 'padding': '30px'})
                ], style={
                    'background': 'linear-gradient(135deg, rgba(0, 255, 136, 0.1) 0%, rgba(0, 200, 100, 0.1) 100%)',
                    'border': '1px solid rgba(0, 255, 136, 0.3)',
                    'border-radius': '20px',
                    'box-shadow': '0 8px 32px rgba(0, 255, 136, 0.2)',
                    'backdrop-filter': 'blur(10px)',
                    'position': 'relative',
                    'overflow': 'hidden'
                })
            ], style={'width': '23%', 'display': 'inline-block', 'margin': '1%'}),
            
            html.Div([
                html.Div([
                    html.Div([
                        html.I(className="fas fa-subway", style={'font-size': '2rem', 'color': '#ff6b6b', 'margin-bottom': '10px'}),
                        html.H2(f"{self.insights['total_metro']}", style={'color': '#ff6b6b', 'font-size': '3rem', 'margin': '0', 'font-weight': '700', 'text-shadow': '0 0 20px rgba(255, 107, 107, 0.5)'}),
                        html.P("Metro Stations", style={'margin': '0', 'font-size': '1.2rem', 'color': '#b0b0b0', 'font-weight': '300'})
                    ], style={'text-align': 'center', 'padding': '30px'})
                ], style={
                    'background': 'linear-gradient(135deg, rgba(255, 107, 107, 0.1) 0%, rgba(200, 50, 50, 0.1) 100%)',
                    'border': '1px solid rgba(255, 107, 107, 0.3)',
                    'border-radius': '20px',
                    'box-shadow': '0 8px 32px rgba(255, 107, 107, 0.2)',
                    'backdrop-filter': 'blur(10px)',
                    'position': 'relative',
                    'overflow': 'hidden'
                })
            ], style={'width': '23%', 'display': 'inline-block', 'margin': '1%'}),
            
            html.Div([
                html.Div([
                    html.Div([
                        html.I(className="fas fa-users", style={'font-size': '2rem', 'color': '#ffd93d', 'margin-bottom': '10px'}),
                        html.H2(f"{self.insights['total_communities']}", style={'color': '#ffd93d', 'font-size': '3rem', 'margin': '0', 'font-weight': '700', 'text-shadow': '0 0 20px rgba(255, 217, 61, 0.5)'}),
                        html.P("Communities", style={'margin': '0', 'font-size': '1.2rem', 'color': '#b0b0b0', 'font-weight': '300'})
                    ], style={'text-align': 'center', 'padding': '30px'})
                ], style={
                    'background': 'linear-gradient(135deg, rgba(255, 217, 61, 0.1) 0%, rgba(200, 150, 0, 0.1) 100%)',
                    'border': '1px solid rgba(255, 217, 61, 0.3)',
                    'border-radius': '20px',
                    'box-shadow': '0 8px 32px rgba(255, 217, 61, 0.2)',
                    'backdrop-filter': 'blur(10px)',
                    'position': 'relative',
                    'overflow': 'hidden'
                })
            ], style={'width': '23%', 'display': 'inline-block', 'margin': '1%'})
        ]
    
    def create_advanced_filters(self):
        """Create advanced filtering controls"""
        return html.Div([
            html.Div([
                html.H4("🔍 Advanced Filters", style={'color': '#00d4ff', 'margin-bottom': '20px', 'font-weight': '600'}),
                
                # School Type Filter
                html.Div([
                    html.Label("School Type:", style={'color': '#ffffff', 'font-weight': '500', 'margin-bottom': '5px'}),
                    dcc.Dropdown(
                        id='school-type-filter',
                        options=[{'label': 'All Types', 'value': 'All'}] + 
                               [{'label': school_type, 'value': school_type} for school_type in sorted(self.df['type_of_school'].unique())],
                        value='All',
                        style={'background-color': 'rgba(255, 255, 255, 0.1)', 'border': '1px solid rgba(0, 212, 255, 0.3)'}
                    )
                ], style={'margin-bottom': '15px'}),
                
                # Performance Category Filter
                html.Div([
                    html.Label("Performance Category:", style={'color': '#ffffff', 'font-weight': '500', 'margin-bottom': '5px'}),
                    dcc.Dropdown(
                        id='performance-filter',
                        options=[{'label': 'All Categories', 'value': 'All'}] + 
                               [{'label': cat, 'value': cat} for cat in sorted(self.df['performance_category'].unique())],
                        value='All',
                        style={'background-color': 'rgba(255, 255, 255, 0.1)', 'border': '1px solid rgba(0, 212, 255, 0.3)'}
                    )
                ], style={'margin-bottom': '15px'}),
                
                # Geographic Cluster Filter
                html.Div([
                    html.Label("Geographic Cluster:", style={'color': '#ffffff', 'font-weight': '500', 'margin-bottom': '5px'}),
                    dcc.Dropdown(
                        id='cluster-filter',
                        options=[{'label': 'All Clusters', 'value': 'All'}] + 
                               [{'label': cluster, 'value': cluster} for cluster in sorted(self.df['geographic_cluster_label'].unique())],
                        value='All',
                        style={'background-color': 'rgba(255, 255, 255, 0.1)', 'border': '1px solid rgba(0, 212, 255, 0.3)'}
                    )
                ], style={'margin-bottom': '15px'}),
                
                # Distance Range Filters
                html.Div([
                    html.Label("Healthcare Distance Range (km):", style={'color': '#ffffff', 'font-weight': '500', 'margin-bottom': '5px'}),
                    dcc.RangeSlider(
                        id='healthcare-distance-slider',
                        min=0,
                        max=5,
                        step=0.1,
                        value=[0, 5],
                        marks={i: f'{i}km' for i in range(0, 6)},
                        tooltip={"placement": "bottom", "always_visible": True}
                    )
                ], style={'margin-bottom': '15px'}),
                
                html.Div([
                    html.Label("Metro Distance Range (km):", style={'color': '#ffffff', 'font-weight': '500', 'margin-bottom': '5px'}),
                    dcc.RangeSlider(
                        id='metro-distance-slider',
                        min=0,
                        max=15,
                        step=0.5,
                        value=[0, 15],
                        marks={i: f'{i}km' for i in range(0, 16, 3)},
                        tooltip={"placement": "bottom", "always_visible": True}
                    )
                ], style={'margin-bottom': '15px'}),
                
                # Urban Score Range
                html.Div([
                    html.Label("Urban Score Range:", style={'color': '#ffffff', 'font-weight': '500', 'margin-bottom': '5px'}),
                    dcc.RangeSlider(
                        id='urban-score-slider',
                        min=0,
                        max=5,
                        step=0.1,
                        value=[0, 5],
                        marks={i: f'{i}' for i in range(0, 6)},
                        tooltip={"placement": "bottom", "always_visible": True}
                    )
                ], style={'margin-bottom': '20px'}),
                
                # Reset Button
                html.Button(
                    "🔄 Reset Filters",
                    id="reset-filters",
                    style={
                        'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                        'color': 'white',
                        'border': 'none',
                        'padding': '10px 20px',
                        'border-radius': '25px',
                        'cursor': 'pointer',
                        'font-weight': '600',
                        'width': '100%'
                    }
                )
                
            ], style={
                'background': 'rgba(0, 0, 0, 0.3)',
                'padding': '25px',
                'border-radius': '15px',
                'border': '1px solid rgba(0, 212, 255, 0.2)',
                'backdrop-filter': 'blur(10px)'
            })
        ], style={'width': '25%', 'display': 'inline-block', 'vertical-align': 'top', 'margin-right': '20px'})
    
    def create_advanced_map(self):
        """Create highly interactive advanced map"""
        # Create base map
        fig = go.Figure()
        
        # Add school locations with advanced styling
        fig.add_trace(go.Scattermapbox(
            lat=self.df['latitude'],
            lon=self.df['longitude'],
            mode='markers',
            marker=dict(
                size=self.df['final_urban_score'] * 8 + 10,
                color=self.df['comprehensive_accessibility_score'],
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(
                    title="Accessibility Score",
                    tickmode="array",
                    tickvals=[4, 4.2, 4.4, 4.6, 4.8, 5.0],
                    ticktext=["4.0", "4.2", "4.4", "4.6", "4.8", "5.0"]
                ),
                opacity=0.8
            ),
            text=self.df['school_name'],
            hovertemplate='<b>%{text}</b><br>' +
                         'Type: ' + self.df['type_of_school'] + '<br>' +
                         'Healthcare: %{customdata[0]:.2f}km<br>' +
                         'Metro: %{customdata[1]:.2f}km<br>' +
                         'Community: %{customdata[2]:.2f}km<br>' +
                         'Urban Score: %{customdata[3]:.2f}<br>' +
                         '<extra></extra>',
            customdata=list(zip(
                self.df['nearest_healthcare_distance_km_x'],
                self.df['nearest_metro_distance_km_x'],
                self.df['nearest_community_distance_km'],
                self.df['final_urban_score']
            )),
            name="Schools"
        ))
        
        # Update layout with futuristic styling
        fig.update_layout(
            mapbox=dict(
                style="open-street-map",
                center=dict(lat=25.2048, lon=55.2708),
                zoom=10
            ),
            title=dict(
                text="🏫 Interactive School Locations & Accessibility Analysis",
                font=dict(size=24, color='#00d4ff'),
                x=0.5
            ),
            height=700,
            margin=dict(l=0, r=0, t=60, b=0),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter, sans-serif", color="white")
        )
        
        return fig
    
    def create_advanced_charts(self):
        """Create advanced interactive charts"""
        charts = {}
        
        # 1. Healthcare Analysis
        hc_fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Distance Distribution', 'Accessibility Tiers', 'School Type Analysis', 'Performance by Tier'),
            specs=[[{"type": "histogram"}, {"type": "pie"}],
                   [{"type": "bar"}, {"type": "bar"}]]
        )
        
        # Distance distribution
        hc_fig.add_trace(
            go.Histogram(
                x=self.df['nearest_healthcare_distance_km_x'],
                name='Healthcare Distance',
                marker_color='#00ff88',
                opacity=0.8
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
                marker_colors=['#00ff88', '#ffd93d', '#ff6b6b', '#ff4757']
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
            title="🏥 Advanced Healthcare Analysis",
            height=600,
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter, sans-serif", color="white")
        )
        
        charts['healthcare'] = hc_fig
        
        # 2. Metro Analysis
        metro_fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Distance Distribution', 'Accessibility Tiers', 'Correlation Analysis', 'Performance by Tier'),
            specs=[[{"type": "histogram"}, {"type": "pie"}],
                   [{"type": "scatter"}, {"type": "bar"}]]
        )
        
        # Distance distribution
        metro_fig.add_trace(
            go.Histogram(
                x=self.df['nearest_metro_distance_km_x'],
                name='Metro Distance',
                marker_color='#ff6b6b',
                opacity=0.8
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
                marker_colors=['#ff6b6b', '#ffd93d', '#ffa726', '#ff5722']
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
            title="🚇 Advanced Metro Analysis",
            height=600,
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter, sans-serif", color="white")
        )
        
        charts['metro'] = metro_fig
        
        # 3. Performance Analysis
        perf_fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Urban Score Distribution', 'Performance Categories', 'Accessibility Correlation', 'Geographic Clusters'),
            specs=[[{"type": "histogram"}, {"type": "pie"}],
                   [{"type": "scatter"}, {"type": "bar"}]]
        )
        
        # Urban score distribution
        perf_fig.add_trace(
            go.Histogram(
                x=self.df['final_urban_score'],
                name='Urban Score',
                marker_color='#ffd93d',
                opacity=0.8
            ),
            row=1, col=1
        )
        
        # Performance categories pie
        perf_counts = self.df['performance_category'].value_counts()
        perf_fig.add_trace(
            go.Pie(
                labels=perf_counts.index,
                values=perf_counts.values,
                name="Performance Categories",
                marker_colors=['#ff4757', '#ffd93d', '#00ff88', '#00d4ff']
            ),
            row=1, col=2
        )
        
        # Accessibility correlation
        perf_fig.add_trace(
            go.Scatter(
                x=self.df['healthcare_accessibility_score'],
                y=self.df['metro_accessibility_score'],
                mode='markers',
                marker=dict(
                    color=self.df['final_urban_score'],
                    colorscale='Viridis',
                    size=10,
                    opacity=0.7
                ),
                name='Accessibility Correlation',
                text=self.df['school_name'],
                hovertemplate='<b>%{text}</b><br>Healthcare Score: %{x}<br>Metro Score: %{y}<br>Urban Score: %{marker.color}<extra></extra>'
            ),
            row=2, col=1
        )
        
        # Geographic clusters
        cluster_perf = self.df.groupby('geographic_cluster_label')['final_urban_score'].mean().sort_values(ascending=False)
        perf_fig.add_trace(
            go.Bar(
                x=cluster_perf.index,
                y=cluster_perf.values,
                name='Performance by Cluster',
                marker_color='#ff6b6b',
                opacity=0.8
            ),
            row=2, col=2
        )
        
        perf_fig.update_layout(
            title="🎯 Advanced Performance Analysis",
            height=600,
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter, sans-serif", color="white")
        )
        
        charts['performance'] = perf_fig
        
        return charts
    
    def create_dashboard_layout(self):
        """Create the futuristic dashboard layout"""
        print("🎨 Creating futuristic dashboard layout...")
        
        # Load data and create insights
        self.load_data()
        self.create_insights()
        
        # Create components
        kpi_cards = self.create_futuristic_kpi_cards()
        filters = self.create_advanced_filters()
        map_fig = self.create_advanced_map()
        charts = self.create_advanced_charts()
        
        layout = html.Div([
            # Custom CSS
            html.Link(
                rel="stylesheet",
                href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"
            ),
            html.Link(
                rel="stylesheet",
                href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap"
            ),
            
            # Header
            html.Div([
                html.Div([
                    html.H1("🏫 Dubai Schools Comprehensive Accessibility Dashboard", 
                           style={'color': '#00d4ff', 'margin': '0', 'font-size': '2.5rem', 'font-weight': '700', 'text-shadow': '0 0 30px rgba(0, 212, 255, 0.5)'}),
                    html.P("Advanced Analytics for Educational Infrastructure Planning", 
                          style={'color': '#b0b0b0', 'margin': '10px 0 0 0', 'font-size': '1.2rem', 'font-weight': '300'})
                ], style={'text-align': 'center', 'padding': '40px 20px'})
            ], style={
                'background': 'linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 50%, #16213e 100%)',
                'margin-bottom': '30px',
                'border-radius': '0 0 30px 30px',
                'box-shadow': '0 10px 40px rgba(0, 0, 0, 0.5)'
            }),
            
            # Main content
            html.Div([
                # KPI Cards
                html.Div(kpi_cards, style={'margin-bottom': '40px'}),
                
                # Filters and Map Row
                html.Div([
                    filters,
                    html.Div([
                        dcc.Graph(
                            id='main-map',
                            figure=map_fig,
                            style={'height': '700px', 'border-radius': '15px', 'overflow': 'hidden'}
                        )
                    ], style={'width': '73%', 'display': 'inline-block'})
                ], style={'margin-bottom': '40px'}),
                
                # Advanced Analytics Tabs
                dcc.Tabs([
                    dcc.Tab(
                        label="🏥 Healthcare Analysis",
                        children=[
                            dcc.Graph(
                                id='healthcare-charts',
                                figure=charts['healthcare'],
                                style={'height': '600px', 'border-radius': '15px', 'overflow': 'hidden'}
                            )
                        ],
                        style={'background': 'rgba(0, 255, 136, 0.1)', 'border-radius': '10px', 'margin': '5px'},
                        selected_style={'background': 'rgba(0, 255, 136, 0.2)', 'border-radius': '10px', 'margin': '5px'}
                    ),
                    dcc.Tab(
                        label="🚇 Metro Analysis",
                        children=[
                            dcc.Graph(
                                id='metro-charts',
                                figure=charts['metro'],
                                style={'height': '600px', 'border-radius': '15px', 'overflow': 'hidden'}
                            )
                        ],
                        style={'background': 'rgba(255, 107, 107, 0.1)', 'border-radius': '10px', 'margin': '5px'},
                        selected_style={'background': 'rgba(255, 107, 107, 0.2)', 'border-radius': '10px', 'margin': '5px'}
                    ),
                    dcc.Tab(
                        label="🎯 Performance Analysis",
                        children=[
                            dcc.Graph(
                                id='performance-charts',
                                figure=charts['performance'],
                                style={'height': '600px', 'border-radius': '15px', 'overflow': 'hidden'}
                            )
                        ],
                        style={'background': 'rgba(255, 217, 61, 0.1)', 'border-radius': '10px', 'margin': '5px'},
                        selected_style={'background': 'rgba(255, 217, 61, 0.2)', 'border-radius': '10px', 'margin': '5px'}
                    )
                ], style={'margin-top': '20px'})
                
            ], style={'padding': '0 20px', 'max-width': '1400px', 'margin': '0 auto'})
            
        ], style={
            'background': 'linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 50%, #16213e 100%)',
            'min-height': '100vh',
            'font-family': 'Inter, sans-serif',
            'color': 'white'
        })
        
        return layout
    
    def create_dashboard_app(self):
        """Create and configure the futuristic Dash app"""
        print("🚀 Creating futuristic web dashboard...")
        
        # Initialize Dash app
        self.app = Dash(__name__)
        
        # Set app title
        self.app.title = "Dubai Schools Futuristic Dashboard"
        
        # Create layout
        self.app.layout = self.create_dashboard_layout()
        
        # Add callbacks for interactivity
        self.add_callbacks()
        
        print("✅ Futuristic dashboard app created!")
        return self.app
    
    def add_callbacks(self):
        """Add interactive callbacks"""
        @self.app.callback(
            [Output('main-map', 'figure'),
             Output('healthcare-charts', 'figure'),
             Output('metro-charts', 'figure'),
             Output('performance-charts', 'figure')],
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
            map_fig = self.create_advanced_map()
            if len(filtered_df) > 0:
                map_fig.data[0].lat = filtered_df['latitude']
                map_fig.data[0].lon = filtered_df['longitude']
                map_fig.data[0].marker.size = filtered_df['final_urban_score'] * 8 + 10
                map_fig.data[0].marker.color = filtered_df['comprehensive_accessibility_score']
                map_fig.data[0].text = filtered_df['school_name']
                map_fig.data[0].customdata = list(zip(
                    filtered_df['nearest_healthcare_distance_km_x'],
                    filtered_df['nearest_metro_distance_km_x'],
                    filtered_df['nearest_community_distance_km'],
                    filtered_df['final_urban_score']
                ))
            
            # Update charts (simplified for now)
            charts = self.create_advanced_charts()
            
            return map_fig, charts['healthcare'], charts['metro'], charts['performance']
    
    def run_dashboard(self, debug=True, port=8051):
        """Run the dashboard"""
        print("🌐 Starting futuristic dashboard server...")
        print(f"📱 Dashboard will be available at: http://localhost:{port}")
        print("🛑 Press Ctrl+C to stop the server")
        
        self.app.run(debug=debug, port=port)

def main():
    """Main execution function"""
    print("🚀 PHASE 3: FUTURISTIC DASHBOARD CREATION")
    print("=" * 60)
    
    # Initialize dashboard creator
    dashboard_creator = FuturisticDashboard(
        'phase2_integration/phase2_integration/comprehensive_results/comprehensive_school_profiles_all_datasets.csv'
    )
    
    # Create and run dashboard
    app = dashboard_creator.create_dashboard_app()
    dashboard_creator.run_dashboard()

if __name__ == "__main__":
    main()
