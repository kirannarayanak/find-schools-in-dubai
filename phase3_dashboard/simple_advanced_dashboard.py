#!/usr/bin/env python3
"""
Simple Advanced Dashboard Creator
Creates the most comprehensive, interactive dashboard using only basic Python libraries
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
from dash import Dash, html, dcc, Input, Output, dash_table
from datetime import datetime
import json
import os

class SimpleAdvancedDashboard:
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
    
    def create_kpi_cards(self):
        """Create KPI cards for the dashboard"""
        return [
            html.Div([
                html.Div([
                    html.H3(f"{self.insights['total_schools']}", style={'color': '#007bff', 'font-size': '2.5rem', 'margin': '0'}),
                    html.P("Total Schools", style={'margin': '0', 'font-size': '1.1rem'})
                ], style={'text-align': 'center', 'padding': '20px', 'background': '#f8f9fa', 'border-radius': '10px', 'box-shadow': '0 2px 4px rgba(0,0,0,0.1)'})
            ], style={'width': '23%', 'display': 'inline-block', 'margin': '1%'}),
            
            html.Div([
                html.Div([
                    html.H3(f"{self.insights['total_healthcare']}", style={'color': '#28a745', 'font-size': '2.5rem', 'margin': '0'}),
                    html.P("Healthcare Facilities", style={'margin': '0', 'font-size': '1.1rem'})
                ], style={'text-align': 'center', 'padding': '20px', 'background': '#f8f9fa', 'border-radius': '10px', 'box-shadow': '0 2px 4px rgba(0,0,0,0.1)'})
            ], style={'width': '23%', 'display': 'inline-block', 'margin': '1%'}),
            
            html.Div([
                html.Div([
                    html.H3(f"{self.insights['total_metro']}", style={'color': '#17a2b8', 'font-size': '2.5rem', 'margin': '0'}),
                    html.P("Metro Stations", style={'margin': '0', 'font-size': '1.1rem'})
                ], style={'text-align': 'center', 'padding': '20px', 'background': '#f8f9fa', 'border-radius': '10px', 'box-shadow': '0 2px 4px rgba(0,0,0,0.1)'})
            ], style={'width': '23%', 'display': 'inline-block', 'margin': '1%'}),
            
            html.Div([
                html.Div([
                    html.H3(f"{self.insights['total_communities']}", style={'color': '#ffc107', 'font-size': '2.5rem', 'margin': '0'}),
                    html.P("Communities", style={'margin': '0', 'font-size': '1.1rem'})
                ], style={'text-align': 'center', 'padding': '20px', 'background': '#f8f9fa', 'border-radius': '10px', 'box-shadow': '0 2px 4px rgba(0,0,0,0.1)'})
            ], style={'width': '23%', 'display': 'inline-block', 'margin': '1%'})
        ]
    
    def create_healthcare_analysis_charts(self):
        """Create healthcare analysis charts"""
        # Distance distribution
        fig1 = px.histogram(
            self.df, 
            x='nearest_healthcare_distance_km_x',
            title='Healthcare Distance Distribution',
            labels={'nearest_healthcare_distance_km_x': 'Distance (km)', 'count': 'Number of Schools'},
            color_discrete_sequence=['#2E86AB']
        )
        fig1.update_layout(
            xaxis_title="Distance to Nearest Healthcare (km)",
            yaxis_title="Number of Schools",
            title_x=0.5,
            height=400,
            showlegend=False
        )
        
        # Accessibility tier pie chart
        tier_counts = self.df['healthcare_accessibility_tier'].value_counts()
        fig2 = px.pie(
            values=tier_counts.values,
            names=tier_counts.index,
            title='Healthcare Accessibility Tiers',
            color_discrete_sequence=['#28a745', '#ffc107', '#fd7e14', '#dc3545']
        )
        fig2.update_layout(title_x=0.5, height=400)
        
        # School type analysis
        school_type_analysis = self.df.groupby('type_of_school').agg({
            'nearest_healthcare_distance_km_x': 'mean'
        }).reset_index()
        
        fig3 = px.bar(
            school_type_analysis,
            x='type_of_school',
            y='nearest_healthcare_distance_km_x',
            title='Average Healthcare Distance by School Type',
            color='nearest_healthcare_distance_km_x',
            color_continuous_scale='RdYlGn_r'
        )
        fig3.update_layout(
            xaxis_title="School Type",
            yaxis_title="Average Distance (km)",
            title_x=0.5,
            height=400,
            showlegend=False
        )
        
        return fig1, fig2, fig3
    
    def create_metro_analysis_charts(self):
        """Create metro analysis charts"""
        # Distance distribution
        fig1 = px.histogram(
            self.df, 
            x='nearest_metro_distance_km_x',
            title='Metro Distance Distribution',
            labels={'nearest_metro_distance_km_x': 'Distance (km)', 'count': 'Number of Schools'},
            color_discrete_sequence=['#A23B72']
        )
        fig1.update_layout(
            xaxis_title="Distance to Nearest Metro (km)",
            yaxis_title="Number of Schools",
            title_x=0.5,
            height=400,
            showlegend=False
        )
        
        # Accessibility tier pie chart
        tier_counts = self.df['metro_accessibility_tier'].value_counts()
        fig2 = px.pie(
            values=tier_counts.values,
            names=tier_counts.index,
            title='Metro Accessibility Tiers',
            color_discrete_sequence=['#28a745', '#ffc107', '#fd7e14', '#dc3545']
        )
        fig2.update_layout(title_x=0.5, height=400)
        
        # Metro access vs healthcare access scatter
        fig3 = px.scatter(
            self.df,
            x='nearest_healthcare_distance_km_x',
            y='nearest_metro_distance_km_x',
            color='comprehensive_accessibility_score',
            size='final_urban_score',
            title='Healthcare vs Metro Access Correlation',
            labels={
                'nearest_healthcare_distance_km_x': 'Healthcare Distance (km)',
                'nearest_metro_distance_km_x': 'Metro Distance (km)',
                'comprehensive_accessibility_score': 'Accessibility Score'
            }
        )
        fig3.update_layout(title_x=0.5, height=400)
        
        return fig1, fig2, fig3
    
    def create_community_analysis_charts(self):
        """Create community analysis charts"""
        # Distance distribution
        fig1 = px.histogram(
            self.df, 
            x='nearest_community_distance_km',
            title='Community Distance Distribution',
            labels={'nearest_community_distance_km': 'Distance (km)', 'count': 'Number of Schools'},
            color_discrete_sequence=['#F18F01']
        )
        fig1.update_layout(
            xaxis_title="Distance to Nearest Community (km)",
            yaxis_title="Number of Schools",
            title_x=0.5,
            height=400,
            showlegend=False
        )
        
        # Population analysis
        fig2 = px.scatter(
            self.df,
            x='nearest_community_distance_km',
            y='population_within_1km',
            color='community_accessibility_tier',
            title='Community Distance vs Population',
            labels={
                'nearest_community_distance_km': 'Distance to Community (km)',
                'population_within_1km': 'Population within 1km'
            }
        )
        fig2.update_layout(title_x=0.5, height=400)
        
        # Community accessibility tier pie chart
        tier_counts = self.df['community_accessibility_tier'].value_counts()
        fig3 = px.pie(
            values=tier_counts.values,
            names=tier_counts.index,
            title='Community Accessibility Tiers',
            color_discrete_sequence=['#28a745', '#ffc107', '#fd7e14', '#dc3545']
        )
        fig3.update_layout(title_x=0.5, height=400)
        
        return fig1, fig2, fig3
    
    def create_performance_analysis_charts(self):
        """Create performance analysis charts"""
        # Urban score distribution
        fig1 = px.histogram(
            self.df, 
            x='final_urban_score',
            title='Urban Score Distribution',
            labels={'final_urban_score': 'Urban Score', 'count': 'Number of Schools'},
            color_discrete_sequence=['#6F42C1']
        )
        fig1.update_layout(
            xaxis_title="Final Urban Score",
            yaxis_title="Number of Schools",
            title_x=0.5,
            height=400,
            showlegend=False
        )
        
        # Performance category pie chart
        perf_counts = self.df['performance_category'].value_counts()
        fig2 = px.pie(
            values=perf_counts.values,
            names=perf_counts.index,
            title='Performance Categories',
            color_discrete_sequence=['#dc3545', '#ffc107', '#28a745', '#007bff']
        )
        fig2.update_layout(title_x=0.5, height=400)
        
        # Accessibility score comparison
        fig3 = px.scatter(
            self.df,
            x='healthcare_accessibility_score',
            y='metro_accessibility_score',
            color='comprehensive_accessibility_score',
            size='final_urban_score',
            title='Accessibility Score Comparison',
            labels={
                'healthcare_accessibility_score': 'Healthcare Accessibility Score',
                'metro_accessibility_score': 'Metro Accessibility Score',
                'comprehensive_accessibility_score': 'Comprehensive Score'
            }
        )
        fig3.update_layout(title_x=0.5, height=400)
        
        return fig1, fig2, fig3
    
    def create_geographic_map(self):
        """Create interactive geographic map"""
        fig = px.scatter_mapbox(
            self.df,
            lat='latitude',
            lon='longitude',
            color='comprehensive_accessibility_score',
            size='final_urban_score',
            hover_data=[
                'school_name', 'type_of_school', 
                'nearest_healthcare_distance_km_x', 
                'nearest_metro_distance_km_x',
                'nearest_community_distance_km'
            ],
            title='School Locations and Accessibility Scores',
            mapbox_style='open-street-map',
            zoom=10,
            color_continuous_scale='Viridis'
        )
        fig.update_layout(
            title_x=0.5,
            height=600,
            mapbox=dict(
                center=dict(lat=25.2048, lon=55.2708),
                zoom=10
            )
        )
        return fig
    
    def create_correlation_heatmap(self):
        """Create correlation heatmap"""
        # Select numeric columns for correlation
        numeric_cols = [
            'nearest_healthcare_distance_km_x',
            'nearest_metro_distance_km_x', 
            'nearest_community_distance_km',
            'comprehensive_accessibility_score',
            'final_urban_score',
            'healthcare_within_1km_x',
            'metro_within_1km_x',
            'communities_within_1km',
            'population_within_1km'
        ]
        
        corr_matrix = self.df[numeric_cols].corr()
        
        fig = px.imshow(
            corr_matrix,
            text_auto=True,
            aspect="auto",
            title="Correlation Heatmap",
            color_continuous_scale='RdBu_r'
        )
        fig.update_layout(title_x=0.5, height=500)
        
        return fig
    
    def create_top_performers_table(self):
        """Create top performers table"""
        top_performers = self.df.nlargest(20, 'final_urban_score')[[
            'school_name', 'type_of_school', 'location',
            'nearest_healthcare_distance_km_x', 'nearest_metro_distance_km_x',
            'nearest_community_distance_km', 'comprehensive_accessibility_score',
            'final_urban_score'
        ]].round(3)
        
        return dash_table.DataTable(
            data=top_performers.to_dict('records'),
            columns=[
                {"name": "School Name", "id": "school_name"},
                {"name": "Type", "id": "type_of_school"},
                {"name": "Location", "id": "location"},
                {"name": "Healthcare Dist (km)", "id": "nearest_healthcare_distance_km_x"},
                {"name": "Metro Dist (km)", "id": "nearest_metro_distance_km_x"},
                {"name": "Community Dist (km)", "id": "nearest_community_distance_km"},
                {"name": "Accessibility Score", "id": "comprehensive_accessibility_score"},
                {"name": "Urban Score", "id": "final_urban_score"}
            ],
            style_cell={'textAlign': 'left', 'fontSize': 12, 'fontFamily': 'Arial'},
            style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'},
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(248, 248, 248)'
                }
            ],
            page_size=10,
            sort_action="native",
            filter_action="native"
        )
    
    def create_dashboard_layout(self):
        """Create the complete dashboard layout"""
        print("🎨 Creating dashboard layout...")
        
        # Load data and create insights
        self.load_data()
        self.create_insights()
        
        # Create charts
        hc_fig1, hc_fig2, hc_fig3 = self.create_healthcare_analysis_charts()
        metro_fig1, metro_fig2, metro_fig3 = self.create_metro_analysis_charts()
        comm_fig1, comm_fig2, comm_fig3 = self.create_community_analysis_charts()
        perf_fig1, perf_fig2, perf_fig3 = self.create_performance_analysis_charts()
        map_fig = self.create_geographic_map()
        heatmap_fig = self.create_correlation_heatmap()
        top_performers_table = self.create_top_performers_table()
        
        # Create KPI cards
        kpi_cards = self.create_kpi_cards()
        
        layout = html.Div([
            # Header
            html.Div([
                html.H1("🏫 Dubai Schools Comprehensive Accessibility Dashboard", 
                       style={'text-align': 'center', 'color': 'white', 'margin': '0', 'padding': '20px'}),
                html.P("Advanced Analytics for Educational Infrastructure Planning", 
                      style={'text-align': 'center', 'color': 'white', 'margin': '0', 'padding-bottom': '20px'})
            ], style={'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', 'margin-bottom': '30px'}),
            
            # Main content
            html.Div([
                # KPI Cards Row
                html.Div(kpi_cards, style={'margin-bottom': '30px'}),
                
                # Tabs
                dcc.Tabs([
                    # Overview Tab
                    dcc.Tab(label="Overview", children=[
                        html.Div([
                            html.H3("Geographic Distribution", style={'text-align': 'center', 'margin-bottom': '20px'}),
                            dcc.Graph(figure=map_fig)
                        ], style={'margin-bottom': '30px'}),
                        
                        html.Div([
                            html.H3("Correlation Analysis", style={'text-align': 'center', 'margin-bottom': '20px'}),
                            dcc.Graph(figure=heatmap_fig)
                        ])
                    ]),
                    
                    # Healthcare Tab
                    dcc.Tab(label="Healthcare Analysis", children=[
                        html.Div([
                            html.Div([
                                html.H4("Distance Distribution", style={'text-align': 'center', 'margin-bottom': '20px'}),
                                dcc.Graph(figure=hc_fig1)
                            ], style={'width': '50%', 'display': 'inline-block'}),
                            html.Div([
                                html.H4("Accessibility Tiers", style={'text-align': 'center', 'margin-bottom': '20px'}),
                                dcc.Graph(figure=hc_fig2)
                            ], style={'width': '50%', 'display': 'inline-block'})
                        ], style={'margin-bottom': '30px'}),
                        
                        html.Div([
                            html.H4("School Type Analysis", style={'text-align': 'center', 'margin-bottom': '20px'}),
                            dcc.Graph(figure=hc_fig3)
                        ])
                    ]),
                    
                    # Metro Tab
                    dcc.Tab(label="Metro Analysis", children=[
                        html.Div([
                            html.Div([
                                html.H4("Distance Distribution", style={'text-align': 'center', 'margin-bottom': '20px'}),
                                dcc.Graph(figure=metro_fig1)
                            ], style={'width': '50%', 'display': 'inline-block'}),
                            html.Div([
                                html.H4("Accessibility Tiers", style={'text-align': 'center', 'margin-bottom': '20px'}),
                                dcc.Graph(figure=metro_fig2)
                            ], style={'width': '50%', 'display': 'inline-block'})
                        ], style={'margin-bottom': '30px'}),
                        
                        html.Div([
                            html.H4("Healthcare vs Metro Correlation", style={'text-align': 'center', 'margin-bottom': '20px'}),
                            dcc.Graph(figure=metro_fig3)
                        ])
                    ]),
                    
                    # Community Tab
                    dcc.Tab(label="Community Analysis", children=[
                        html.Div([
                            html.Div([
                                html.H4("Distance Distribution", style={'text-align': 'center', 'margin-bottom': '20px'}),
                                dcc.Graph(figure=comm_fig1)
                            ], style={'width': '50%', 'display': 'inline-block'}),
                            html.Div([
                                html.H4("Accessibility Tiers", style={'text-align': 'center', 'margin-bottom': '20px'}),
                                dcc.Graph(figure=comm_fig3)
                            ], style={'width': '50%', 'display': 'inline-block'})
                        ], style={'margin-bottom': '30px'}),
                        
                        html.Div([
                            html.H4("Distance vs Population", style={'text-align': 'center', 'margin-bottom': '20px'}),
                            dcc.Graph(figure=comm_fig2)
                        ])
                    ]),
                    
                    # Performance Tab
                    dcc.Tab(label="Performance Analysis", children=[
                        html.Div([
                            html.Div([
                                html.H4("Urban Score Distribution", style={'text-align': 'center', 'margin-bottom': '20px'}),
                                dcc.Graph(figure=perf_fig1)
                            ], style={'width': '50%', 'display': 'inline-block'}),
                            html.Div([
                                html.H4("Performance Categories", style={'text-align': 'center', 'margin-bottom': '20px'}),
                                dcc.Graph(figure=perf_fig2)
                            ], style={'width': '50%', 'display': 'inline-block'})
                        ], style={'margin-bottom': '30px'}),
                        
                        html.Div([
                            html.H4("Accessibility Score Comparison", style={'text-align': 'center', 'margin-bottom': '20px'}),
                            dcc.Graph(figure=perf_fig3)
                        ])
                    ]),
                    
                    # Top Performers Tab
                    dcc.Tab(label="Top Performers", children=[
                        html.Div([
                            html.H4("Top 20 Performing Schools", style={'text-align': 'center', 'margin-bottom': '20px'}),
                            top_performers_table
                        ])
                    ])
                    
                ], style={'margin-top': '20px'})
                
            ], style={'padding': '0 20px'})
        ])
        
        return layout
    
    def create_dashboard_app(self):
        """Create and configure the Dash app"""
        print("🚀 Creating advanced web dashboard...")
        
        # Initialize Dash app
        self.app = Dash(__name__)
        
        # Set app title
        self.app.title = "Dubai Schools Accessibility Dashboard"
        
        # Create layout
        self.app.layout = self.create_dashboard_layout()
        
        print("✅ Dashboard app created!")
        return self.app
    
    def run_dashboard(self, debug=True, port=8050):
        """Run the dashboard"""
        print("🌐 Starting dashboard server...")
        print(f"📱 Dashboard will be available at: http://localhost:{port}")
        print("🛑 Press Ctrl+C to stop the server")
        
        self.app.run(debug=debug, port=port)

def main():
    """Main execution function"""
    print("🚀 PHASE 3: ADVANCED WEB DASHBOARD CREATION")
    print("=" * 60)
    
    # Initialize dashboard creator
    dashboard_creator = SimpleAdvancedDashboard(
        'phase2_integration/phase2_integration/comprehensive_results/comprehensive_school_profiles_all_datasets.csv'
    )
    
    # Create and run dashboard
    app = dashboard_creator.create_dashboard_app()
    dashboard_creator.run_dashboard()

if __name__ == "__main__":
    main()
