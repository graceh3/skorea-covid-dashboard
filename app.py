import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


df_case = pd.read_csv('./data/Case.csv')
dict_num_cases = dict(df_case['infection_case'].value_counts())
dict_total_confirmed = dict(df_case[['infection_case', 'confirmed']].groupby('infection_case').sum()['confirmed'])

app.layout = html.Div(children=[
    html.H1(children='South Korea COVID Data'),

    dcc.Graph(
        id='num-cases-bar',
        figure={
            'data': [dict(
                    x=list(df_case['infection_case'].unique()),
                    y=list(dict_num_cases.values()),
                    text=list(df_case['infection_case'].unique()),
                    type='bar',
                    name=list(df_case['infection_case'].unique())
                )
                    ],
            'layout': {
                'title': 'Number of Cases by Infection Case'
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)