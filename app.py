import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

import plotly.graph_objs as go
import plotly.express as px

external_stylesheets = ["https://cdn.jsdelivr.net/npm/picnic"]
    # 'https://codepen.io/chriddyp/pen/bWLwgP.css']

# 1. Launch the app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# 2. Import & set the data
df_case = pd.read_csv('./data/Case.csv')
dict_num_cases = dict(df_case['infection_case'].value_counts())
dict_total_confirmed = dict(df_case[['infection_case', 'confirmed']].groupby('infection_case').sum()['confirmed'])

df_region = pd.read_csv('.data/Region.csv')
df_coord = df_region[['code','province','latitude', 'longitude']]

# 3. Create a plotly figure
fig = px.choropleth_mapbox(geojson=counties, locations='fips', color='unemp',
                           color_continuous_scale="Viridis",
                           range_color=(0, 12),
                           mapbox_style="carto-positron",
                           zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
                           opacity=0.5,
                           labels={'unemp':'unemployment rate'}
                          )
# trace_1 = go.Choropleth(locationmode='ISO-3', locations=['KOR'])
# layout = go.Layout(title = 'Map of South Korea',
#                    hovermode = 'closest')
# fig = go.Figure(data = [trace_1], layout = layout)

# 4. Set the layout
app.layout = html.Div(children=[
    html.H1(children='South Korea COVID Data'),

    dcc.Graph(id = 'plot', figure = fig),
    
    dcc.Graph(
        id='num-cases-bar',
        figure={
            'data': [dict(
                    x=list(df_case['infection_case'].unique()),
                    y=list(dict_num_cases.values()),
                    text=list(df_case['infection_case'].unique()),
                    type='bar',
                    name='Number of Cases')],
            'layout': {'title': 'Number of Infection Cases'}
            }
        ),

    dcc.Graph(
        id='total-confirmed-bar',
        figure={
            'data': [dict(
                    x=list(df_case['infection_case'].unique()),
                    y=list(dict_total_confirmed.values()),
                    text=list(df_case['infection_case'].unique()),
                    type='bar',
                    name='Total Confirmed')],
            'layout': {
                'title': 'Total Confirmed Per Infection Cases',
                    }
            }
        )
])

if __name__ == '__main__':
    app.run_server(debug=True)