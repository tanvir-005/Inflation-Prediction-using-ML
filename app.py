import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd

# Load the data
data = pd.read_csv('global_inflation_data.csv')

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Inflation Prediction Model'),
    dcc.Graph(id='predictions-graph'),
    html.Div([
        html.Label('Select Country:'),
        dcc.Dropdown(
            id='country-dropdown',
            options=[{'label': country, 'value': country} for country in data['country_name'].unique()],
            value=data['country_name'].unique()[0]
        )
    ]),
    html.Div([
        html.Label('Select Year:'),
        dcc.Dropdown(
            id='year-dropdown',
            options=[{'label': year, 'value': year} for year in data.columns[3:]],
            value=data.columns[3][-4:]  # default to last year
        )
    ])
])

@app.callback(
    Output('predictions-graph', 'figure'),
    [Input('country-dropdown', 'value'),
     Input('year-dropdown', 'value')]
)
def update_graph(selected_country, selected_year):
    country_data = data[data['country_name'] == selected_country]
    if selected_year in country_data.columns:
        actual_values = country_data[selected_year]
        predicted_values = country_data.get(f'{selected_year}_predicted', pd.Series([]))
        
        return {
            'data': [
                {'x': range(len(actual_values)), 'y': actual_values, 'name': 'Actual Values'},
                {'x': range(len(predicted_values)), 'y': predicted_values, 'name': 'Predicted Values'}
            ],
            'layout': {
                'title': f'Actual vs Predicted Values for {selected_country} in {selected_year}',
                'xaxis': {'title': 'Index'},
                'yaxis': {'title': 'Values'}
            }
        }
    else:
        return {'data': [], 'layout': {'title': f'No data available for {selected_country} in {selected_year}'}}

if __name__ == '__main__':
    app.run(debug=True)
