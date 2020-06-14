import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import json
import plotly.graph_objs as go
import plotly.express as px

# 0. Set the stylesheet
external_stylesheets = ["https://cdn.jsdelivr.net/npm/picnic"]
    # 'https://codepen.io/chriddyp/pen/bWLwgP.css']

# 1. Launch the app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# 2. Import & set the data
df_case = pd.read_csv('./data/Case.csv')
dict_num_cases = dict(df_case['infection_case'].value_counts())
dict_total_confirmed = dict(df_case[['infection_case', 'confirmed']].groupby('infection_case').sum()['confirmed'])

df_patients = pd.read_csv('./data/PatientInfo.csv')
# df_region_count = df_patients[['province', 'patient_id']].groupby('province', as_index=False).count()
df_region = pd.read_csv('./data/Region.csv')
# df_coord = df_region[['code','province','latitude', 'longitude']]

with open("data/KOR_adm_shp/KOR_adm1.geojson", "r", encoding="utf8") as read_file:
    geojson_1 = json.load(read_file)

# 3. Create a plotly figure
fig = px.choropleth_mapbox(df_patients, geojson=geojson_1, color="patient_id",
                           locations="province", featureidkey="properties.NAME_1",
                           center={"lat": 37.566953, "lon": 126.977977},
                           mapbox_style="carto-positron", zoom=6)

# fig.update_layout(mapbox_style="carto-positron",
#                   mapbox_zoom=6,
#                   mapbox_center = {"lat": 37.566953, "lon": 126.977977})
                #   margin=dict(l=10, r=500, t=0, b=0))

                  	

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
                'title': 'Total Confirmed By Case',
                    }
            }
        )
])

# 5. Set the executable command
if __name__ == '__main__':
    app.run_server(debug=True)