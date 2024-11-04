import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

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

# Mock data generation functions
def generate_drug_timeline(duration, drugs):
    times = np.linspace(0, duration, 100)
    data = {}
    for drug in drugs:
        if drug == 'drug_a':  # Propofol
            data[drug] = 2 * np.exp(-times/30) + np.random.normal(0, 0.1, len(times))
        elif drug == 'drug_b':  # Remifentanil
            data[drug] = 1.5 * np.exp(-times/20) + np.random.normal(0, 0.05, len(times))
        else:  # Rocuronium
            data[drug] = np.exp(-times/40) + np.random.normal(0, 0.08, len(times))
    return times, data

def calculate_environmental_impact(drugs, duration):
    base_impact = {'drug_a': 8.5, 'drug_b': 6.2, 'drug_c': 9.1}
    return {drug: base_impact[drug] * duration/60 for drug in drugs}

@app.callback(
    [Output('interaction-graph', 'figure'),
     Output('side-effects-graph', 'figure'),
     Output('environmental-impact', 'figure'),
     Output('dosage-comparison', 'figure'),
     Output('cost-savings', 'figure'),
     Output('optimization-metrics', 'children')],
    [Input('calculate-button', 'n_clicks')],
    [State('patient-weight', 'value'),
     State('patient-age', 'value'),
     State('asa-score', 'value'),
     State('drug-selection', 'value'),
     State('procedure-duration', 'value')]
)
def update_dashboard(n_clicks, weight, age, asa, drugs, duration):
    if not n_clicks or not all([weight, age, asa, drugs, duration]):
        raise dash.exceptions.PreventUpdate

    # 1. Drug Interaction Timeline
    times, drug_data = generate_drug_timeline(duration, drugs)
    interaction_fig = go.Figure()
    drug_names = {'drug_a': 'Propofol', 'drug_b': 'Remifentanil', 'drug_c': 'Rocuronium'}
    
    for drug in drugs:
        interaction_fig.add_trace(go.Scatter(
            x=times, 
            y=drug_data[drug],
            name=drug_names[drug],
            mode='lines'
        ))
    interaction_fig.update_layout(
        title='Drug Interaction Timeline',
        xaxis_title='Time (minutes)',
        yaxis_title='Drug Concentration',
        hovermode='x unified'
    )

    # 2. Side Effects Risk Analysis
    risk_categories = ['Delirium', 'PONV', 'Respiratory Depression', 'Delayed Recovery']
    current_risks = np.random.uniform(0.3, 0.6, len(risk_categories))
    optimized_risks = current_risks * 0.6  # 40% reduction with optimization

    side_effects_fig = go.Figure(data=[
        go.Bar(name='Current Practice', x=risk_categories, y=current_risks * 100),
        go.Bar(name='Optimized Protocol', x=risk_categories, y=optimized_risks * 100)
    ])
    side_effects_fig.update_layout(
        title='Side Effects Risk Comparison',
        yaxis_title='Risk Percentage (%)',
        barmode='group'
    )

    # 3. Environmental Impact
    impact_data = calculate_environmental_impact(drugs, duration)
    env_fig = go.Figure(data=[
        go.Bar(
            x=list(drug_names[d] for d in impact_data.keys()),
            y=list(impact_data.values()),
            text=list(f'{v:.1f} kg CO2e' for v in impact_data.values()),
            textposition='auto',
        )
    ])
    env_fig.update_layout(
        title='Environmental Impact (CO2 Equivalent)',
        yaxis_title='kg CO2e'
    )

    # 4. Dosage Comparison
    dosage_fig = go.Figure()
    for drug in drugs:
        current_dosage = np.random.uniform(0.8, 1.2)  # Simulated current practice
        optimal_dosage = 1.0  # Reference point
        dosage_fig.add_trace(go.Bar(
            x=['Current Practice', 'Optimal Dosage'],
            y=[current_dosage, optimal_dosage],
            name=drug_names[drug]
        ))
    dosage_fig.update_layout(
        title='Dosage Comparison (Relative to Optimal)',
        yaxis_title='Relative Dosage'
    )

    # 5. Cost Savings Analysis
    savings_categories = ['Drug Cost', 'Recovery Time', 'Complications', 'Environmental']
    baseline_costs = np.random.uniform(1000, 5000, len(savings_categories))
    optimized_costs = baseline_costs * 0.7  # 30% reduction
    savings = baseline_costs - optimized_costs

    cost_fig = go.Figure(data=[
        go.Bar(
            x=savings_categories,
            y=savings,
            text=[f'${s:,.0f}' for s in savings],
            textposition='auto',
        )
    ])
    cost_fig.update_layout(
        title='Potential Cost Savings',
        yaxis_title='Savings ($)'
    )

    # 6. Optimization Metrics Summary
    metrics_html = html.Div([
        html.H4('Optimization Summary'),
        html.P(f'Total Potential Savings: ${sum(savings):,.2f}'),
        html.P(f'Risk Reduction: {((1 - np.mean(optimized_risks)/np.mean(current_risks)) * 100):.1f}%'),
        html.P(f'Environmental Impact Reduction: {(sum(impact_data.values())):.1f} kg CO2e')
    ])

    return interaction_fig, side_effects_fig, env_fig, dosage_fig, cost_fig, metrics_html

if __name__ == '__main__':
    app.run_server(debug=True)

