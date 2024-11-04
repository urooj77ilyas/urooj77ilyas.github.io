import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout
app.layout = html.Div([
    html.H1("Medical Decision Support Dashboard", style={'textAlign': 'center'}),
    
    # Input Section
    html.Div([
        html.Div([
            html.H3("Patient Data Input"),
            dcc.Input(id='patient-weight', type='number', placeholder='Patient Weight (kg)'),
            dcc.Dropdown(
                id='drug-selection',
                options=[
                    {'label': 'Drug A', 'value': 'drug_a'},
                    {'label': 'Drug B', 'value': 'drug_b'},
                    {'label': 'Drug C', 'value': 'drug_c'}
                ],
                multi=True,
                placeholder='Select Drugs'
            ),
            dcc.Input(id='procedure-duration', type='number', placeholder='Procedure Duration (min)'),
            html.Button('Calculate', id='calculate-button', n_clicks=0)
        ], style={'width': '30%', 'display': 'inline-block', 'padding': '20px'}),
        
        # Results Section
        html.Div([
            html.H3("Calculated Results"),
            html.Div(id='dosage-recommendation'),
            html.Div(id='risk-assessment')
        ], style={'width': '70%', 'display': 'inline-block', 'padding': '20px'})
    ]),
    
    # Visualization Section
    html.Div([
        # Drug Interaction Graph
        dcc.Graph(id='interaction-graph'),
        
        # Side Effects Comparison
        dcc.Graph(id='side-effects-graph'),
        
        # Environmental Impact
        dcc.Graph(id='environmental-impact')
    ])
])

# Callback for updating visualizations
@app.callback(
    [Output('interaction-graph', 'figure'),
     Output('side-effects-graph', 'figure'),
     Output('environmental-impact', 'figure'),
     Output('dosage-recommendation', 'children'),
     Output('risk-assessment', 'children')],
    [Input('calculate-button', 'n_clicks')],
    [State('patient-weight', 'value'),
     State('drug-selection', 'value'),
     State('procedure-duration', 'value')]
)
def update_graphs(n_clicks, weight, drugs, duration):
    if n_clicks == 0:
        return [go.Figure()] * 3 + ['', '']
    
    # Sample calculations (replace with actual medical models)
    def calculate_optimal_dosage(weight, drug, duration):
        # Placeholder for actual medical calculations
        return weight * 0.1 * duration
    
    def calculate_risk_score(weight, drugs, duration):
        # Placeholder for risk assessment
        return len(drugs) * duration / weight
    
    # Generate visualization data
    drug_interaction = go.Figure(data=[
        go.Scatter(x=[0, duration], y=[calculate_optimal_dosage(weight, drug, duration)], 
                  name=drug) for drug in drugs
    ])
    drug_interaction.update_layout(title='Drug Interaction Over Time',
                                 xaxis_title='Time (minutes)',
                                 yaxis_title='Drug Concentration')
    
    # Side effects comparison
    side_effects = go.Figure(data=[
        go.Bar(x=['Current Practice', 'Optimized Dosage'],
               y=[46, 15],  # Example values
               name='Risk of Delirium (%)')
    ])
    side_effects.update_layout(title='Side Effects Comparison')
    
    # Environmental impact
    environmental = go.Figure(data=[
        go.Bar(x=['Current Usage', 'Optimized Usage'],
               y=[100, 70],  # Example values
               name='Environmental Impact Score')
    ])
    environmental.update_layout(title='Environmental Impact Assessment')
    
    # Generate recommendations
    dosage_rec = html.Div([
        html.H4('Recommended Dosages:'),
        html.Ul([html.Li(f'{drug}: {calculate_optimal_dosage(weight, drug, duration):.2f} mg') 
                for drug in drugs])
    ])
    
    risk_assessment = html.Div([
        html.H4('Risk Assessment:'),
        html.P(f'Risk Score: {calculate_risk_score(weight, drugs, duration):.2f}')
    ])
    
    return drug_interaction, side_effects, environmental, dosage_rec, risk_assessment

if __name__ == '__main__':
    app.run_server(debug=True)
    # Create the dashboard layout
    app.layout = html.Div([
        html.H1('Medical Drug Interaction Dashboard'),
        
        html.Div([
            html.Label('Patient Weight (kg):'),
            dcc.Input(id='weight-input', type='number', value=70),
            
            html.Label('Duration (minutes):'),
            dcc.Input(id='duration-input', type='number', value=60),
            
            html.Label('Select Drugs:'),
            dcc.Dropdown(
                id='drug-selector',
                options=[
                    {'label': 'Drug A', 'value': 'Drug A'},
                    {'label': 'Drug B', 'value': 'Drug B'},
                    {'label': 'Drug C', 'value': 'Drug C'}
                ],
                value=['Drug A'],
                multi=True
            ),
            
            html.Button('Calculate', id='calculate-button')
        ], style={'padding': '20px'}),
        
        html.Div([
            dcc.Graph(id='drug-interaction-plot'),
            dcc.Graph(id='side-effects-plot'),
            dcc.Graph(id='environmental-plot')
        ], style={'display': 'flex', 'flexWrap': 'wrap'}),
        
        html.Div(id='recommendations', style={'padding': '20px'})
    ])
    
    @app.callback(
        [Output('drug-interaction-plot', 'figure'),
         Output('side-effects-plot', 'figure'),
         Output('environmental-plot', 'figure'),
         Output('recommendations', 'children')],
        [Input('calculate-button', 'n_clicks')],
        [State('weight-input', 'value'),
         State('duration-input', 'value'),
         State('drug-selector', 'value')]
    )
    def update_dashboard(n_clicks, weight, duration, drugs):
        if not n_clicks:
            raise PreventUpdate
            
        drug_interaction, side_effects, environmental, dosage_rec, risk_assessment = generate_analysis(
            weight, drugs, duration
        )
        
        return drug_interaction, side_effects, environmental, [dosage_rec, risk_assessment]

if __name__ == '__main__':
    # Run the server on port 8050
    print("Dashboard is running at: http://localhost:8050")
    app.run_server(debug=True, port=8050)

