from dash import html, dcc, Input, Output, Dash
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go

age = pd.read_csv("AgeGroupDetails.csv")
patients = pd.read_csv("IndividualDetails.csv")
main = pd.read_csv("covid_19_india.csv")

total_patients = patients.shape[0]
active=patients[patients['current_status']=='Hospitalized'].shape[0]
recovered=patients[patients['current_status']=='Recovered'].shape[0]
deaths=patients[patients['current_status']=='Deceased'].shape[0]


main['total']=main['ConfirmedIndianNational'] + main['ConfirmedForeignNational']
main['total']=np.cumsum(main['total'].values)

# external_stylesheets = [
#     {
#         'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
#         'rel': 'stylesheet',
#         'integrity': 'sha384-MCw98SFnGE8fJT3GXwEOngsV7Z2z7NXFoaoApmyYm81iuXOpkFOJwJ8ERdknLPMO',
#         'crossorigin': 'anonymous'
#     }
# ]

# external CSS stylesheet
external_stylesheets = [
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
]

options=[
    {'label':'All', 'value':'All'},
    {'label':'Hospitalized', 'value':'Hospitalized'},
    {'label':'Recovered', 'value':'Recovered'},
    {'label': 'Deceased', 'value':'Deceased'}
]

app = Dash(__name__,external_stylesheets=external_stylesheets)

app.layout = html.Div([
    # Heading
    html.H1(
        'COVID-19 Pandemic Information Dashboard',
        style= {'textAlign':'center','color':'#ffffff'}),


    # 1st row for Cards
    html.Div(
        children=[
            # 1st card
            html.Div([
                html.Div([
                    html.Div([
                        html.H3("Total Cases",className="text-dark"),
                        html.H4(total_patients,className="text-dark")
                    ],className='card-body')
                ],className='card bg-primary')
            ],className="col-md-3"),

            # 2nd card
            html.Div([
                html.Div([
                    html.Div([
                        html.H3("Active Cases",className="text-dark"),
                        html.H4(active,className="text-dark")
                    ],className='card-body')
                ],className='card bg-success')
            ],className="col-md-3"),

            # 3rd card
            html.Div([
                html.Div([
                    html.Div([
                        html.H3("Recovered",className="text-dark"),
                        html.H4(recovered,className="text-dark")
                    ],className='card-body')
                ],className='card bg-danger')
            ],className="col-md-3"),

            # 4th card
            html.Div([
                html.Div([
                    html.Div([
                        html.H3("Deaths",className="text-dark"),
                        html.H4(deaths,className="text-dark")
                    ],className='card-body')
                ],className='card bg-info')
            ],className="col-md-3")
        ],
        className="row" ,style={"marginTop": "50px"}
    ),


    # 2nd row for graphs
    html.Div(
        [
            # Line Plot
            html.Div([
                html.Div([
                    html.Div([
                        dcc.Graph(id='Line Plot',
                                  figure={'data':[go.Scatter(x=main['Date'], y=main['total'],
                                                           mode='lines')],
                                      'layout':go.Layout(title='Day by Day Analysis',
                                                         xaxis={'title':'Date'},
                                                         yaxis={'title':'Number of Cases'})})
                ], className='card-body')
            ],className='card')
        ], className='col-md-8'),

        # Pie plot
        html.Div([
            html.Div([
               html.Div([
                   dcc.Graph(id='pie',
                             figure={'data':[go.Pie(labels=age['AgeGroup'],
                                                    values=age['TotalCases'])],
                                     'layout':go.Layout(title='Age Distribution')})
               ], className='card-body')
            ], className="card")
        ], className='col-md-4')],
        className="row", style={"marginTop": "50px"}
    ),


    # 3rd row for
    html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        dcc.Dropdown(id='picker',options=options,value='All',
                                     className='option-select'),
                        dcc.Graph(id='bar',className='graph-container')
                    ],className="card-body"),
                ],className="card"),
            ],className="col-md-12"),
        ],
        className="row", style={"marginTop": "50px"})
],
className="container")

@app.callback(output=Output('bar','figure'),
              inputs=[Input('picker','value')])
def update_graph(type):
    if type == "All":
        pbar = (patients.groupby('detected_state').count().
                sort_values(by='id',ascending=False)['id'].reset_index())
    else:
        new_df = patients[patients['current_status'] == type]
        pbar = new_df.groupby('detected_state').count().sort_values(by='id',
                                                            ascending=False)['id'].reset_index()

    return {'data': [go.Bar(x=pbar['detected_state'], y=pbar['id'])],
            'layout': go.Layout(title='Bar Chart')}


if __name__ == '__main__':
    app.run(debug=True,port=5000)

