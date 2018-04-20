import psycopg2 as pg
import pandas.io.sql as psql
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

#from sqlalchemy import create_engine
#engine = create_engine('postgresql://postgres:peacebro@10.0.2.115:5432/frauddb')

connection = pg.connect("dbname=frauddb user=postgres password=peacebro host=10.0.2.115 port=5432")
data=psql.read_sql('SELECT * FROM "Fraud_Attributes" ',con=connection )

a=[{'label': 'good', 'value': i} if i == 1 else {'label': 'bad', 'value': i} for i in
                 data['Fraud Classification'].unique()]
a.extend([{'label': 'all', 'value': 3}])
app = dash.Dash()

app.layout = html.Div([

dcc.Graph(id='graph-with-slider'),
dcc.Slider(
        id='month-slider',
        min=data['Duration in month'].min(),
        max=data['Duration in month'].max(),
        value=data['Duration in month'].min(),
        step=None,
        marks={str(month): str(month) for month in data['Duration in month'].unique()}
    ),
    dcc.Graph(id='pie-graph'),

    html.Label('Radio Items'),
    dcc.RadioItems(
        id='good/bad',
        options=a,
        value=1,
        labelStyle={'display': 'inline-block'}
    ),

    html.Label('Checkboxes'),
    dcc.Checklist(
            id='attribute',
            options=[
                {'label': i, 'value': i} for i in data.columns
            ],
            values=['Credit history']
        ),
    dcc.Dropdown(
        id='attribute_pie',
        options=[
                {'label': i, 'value': i} for i in data.columns
            ],
            value='Purpose')
], style={'columnCount': 2})

@app.callback(
    dash.dependencies.Output('graph-with-slider', 'figure'),
    [dash.dependencies.Input('month-slider', 'value'),
     dash.dependencies.Input('good/bad','value'),
     dash.dependencies.Input('attribute', 'values')])
def update_figure(selected_month,fd,att):
    filtered_df =psql.read_sql('SELECT * FROM "Fraud_Attributes" WHERE "Duration in month"= %(int)s ',params={'int':selected_month},con=connection )
    if fd<3:
        selected_df=psql.read_sql('SELECT * FROM "Fraud_Attributes" WHERE "Duration in month"= %(int)s AND "Fraud Classification"=%(int1)s ',params={'int':selected_month,'int1':fd},con=connection )
    else:
        selected_df=filtered_df
    traces=[go.Histogram(x=selected_df[i],name=i) for i in att]

    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={ 'autorange':'True','title': 'Attributes'},
            yaxis={ 'autorange':'True','title': 'Count'},
            hovermode='closest')}
@app.callback(
    dash.dependencies.Output('pie-graph', 'figure'),
    [dash.dependencies.Input('month-slider', 'value'),
     dash.dependencies.Input('good/bad', 'value'),
     dash.dependencies.Input('attribute_pie', 'value')
     ])
def pie_graph(selected_month,fd,att):
    filtered_df = psql.read_sql('SELECT * FROM "Fraud_Attributes" WHERE "Duration in month"= %(int)s ',params={'int':selected_month},con=connection )
    if fd<3:
        selected_df=psql.read_sql('SELECT * FROM "Fraud_Attributes" WHERE "Duration in month"= %(int)s AND "Fraud Classification"=%(int1)s ',params={'int':selected_month,'int1':fd},con=connection )
    else:
        selected_df=filtered_df

    df = selected_df[att].value_counts()
    data1=[
        {'labels': list(df.index.values),
         'values': list(df.values),
         'type': 'pie'
         }]
    return {'data':data1}


if __name__ == '__main__':
    app.run_server(debug=True)