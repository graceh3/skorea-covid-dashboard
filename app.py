import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import json
import plotly.graph_objs as go
import plotly.express as px

######################################
# 0. SET STYLESHEET
external_stylesheets = ["https://cdn.jsdelivr.net/npm/picnic"]
    # 'https://codepen.io/chriddyp/pen/bWLwgP.css']

######################################
# 1. LAUNCH APP
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

######################################
# 2. IMPORT & SET DATA
df_case = pd.read_csv('./data/Case.csv')
df_patients = pd.read_csv('./data/PatientInfo.csv')
df_patients['province'].replace({'Jeju-do', 'Jeju'}, inplace=True) # normalize value for Jeju
df_region = pd.read_csv('./data/Region.csv')
with open("data/KOR_adm_shp/KOR_adm1.geojson", "r", encoding="utf8") as read_file:
    geojson_1 = json.load(read_file)

# 2a. Daily Confirmed
df_daily_confirmed = df_patients[['patient_id','confirmed_date']].groupby('confirmed_date', as_index=False).count()
df_daily_confirmed.rename(columns={'patient_id':'num_confirmed'}, inplace=True)

# 2b. Quick Statistics
total_number_infected = f'{df_patients.shape[0]:,}'
percent_released = str(round((df_patients[df_patients['state']=='released']['patient_id'].count()/df_patients.shape[0]) * 100,1)) + '%'
percent_isolated = str(round((df_patients[df_patients['state']=='isolated']['patient_id'].count()/df_patients.shape[0]) * 100,1)) + '%'
percent_deceased = str(round((df_patients[df_patients['state']=='deceased']['patient_id'].count()/df_patients.shape[0]) * 100,1)) + '%'
avg_daily_confirmed = round(df_daily_confirmed['num_confirmed'].mean())
stat_names = ['Total Number Confirmed', 'Percent Released', 'Percent Isolated', 'Percent Deceased', 'Average Daily Confirmed']
stat_values = [total_number_infected,percent_released,percent_isolated,percent_deceased,avg_daily_confirmed]

data_quickstats = []
for i, stat in enumerate(stat_names):
    data_quickstats.append({'Statistic': stat, 'Value': stat_values[i]})

# 2c. Case Statistics
df_confirmed_by_case = df_case[['infection_case', 'confirmed']].groupby('infection_case', as_index=False).sum()
df_confirmed_by_case.rename(columns={'confirmed':'total_confirmed'},inplace=True)

# 2d. Choropleth Map
df_prov_patients = df_patients[['province', 'patient_id']].groupby('province', as_index=False).count()
df_prov_patients = df_prov_patients.rename(columns={'patient_id':'Number of Patients'})

# 2e. Gender & State
df_gender_state = df_patients[['state','sex','patient_id']].groupby(['state','sex'], as_index=False).count().sort_values(by='patient_id', ascending=False)
df_gender_state = df_gender_state.rename(columns={'patient_id':'Number of Patients'})

######################################
# 3. CREATE PLOTLY FIGURES

fig_1 = px.choropleth_mapbox(df_prov_patients, geojson=geojson_1, color="Number of Patients",
                           color_continuous_scale='amp',
                           locations="province", featureidkey="properties.NAME_1",
                           center={"lat": 36.7331489, "lon": 128.1328623},
                           mapbox_style="carto-positron", zoom=5, opacity=.33)


######################################
# 4. SET LAYOUT
app.layout = html.Div(children=[
    html.H1(children='South Korea COVID-19 Dashboard'),
    html.H2(children='Data as of 2020-05-31'),

    dash_table.DataTable(id='quick-stats'
                        ,columns=[{"name": i, "id": i} for i in ['Statistic', 'Value']]
                        ,data=data_quickstats
                        ,style_header={'fontWeight':'bold', 'backgroundColor':'grey'}
                        ,style_cell={'padding':'5px'}
                        ,style_cell_conditional=[
                                    {'if': {'column_id': 'Statistic'},
                                            'width': '50%',  'textAlign':'left'},
                                    {'if': {'column_id': 'Value'},
                                            'width': '30%',  'textAlign':'left'},
                                                ]
                        ,style_as_list_view=True
                        ),

    dcc.Graph(
        id='daily-confirmed-trend',
        figure=px.line(df_daily_confirmed, x="confirmed_date", y="num_confirmed", title='Daily Trend - Total Confirmed')
        ),
    
    dcc.Graph(id ='map', figure = fig_1),

    dcc.Graph(
        id='total-confirmed-cases',
        figure=px.bar(df_confirmed_by_case.sort_values(by=['total_confirmed'], ascending=True), x="total_confirmed", y="infection_case", orientation='h', height=1000,
             title='Total Confirmed by Infection Case')
        ),

    dcc.Graph(
        id='state-gender',
        figure=px.bar(df_gender_state, x="state", y="Number of Patients", color='sex', barmode='group',
             height=500, title='State of Patients by Gender')
    )
    

])

# 5. Set the executable command
if __name__ == '__main__':
    app.run_server(debug=True)