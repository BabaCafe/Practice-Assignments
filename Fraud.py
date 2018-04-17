import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

colnames=['Status of existing checking account','Duration in month ','Credit history ','Purpose','Credit amount','Savings account/bonds ','Present employment since','Installment rate in percentage of disposable income','Personal status and sex','Other debtors / guarantors','Present residence since','Property','Age in years','Other installment plans','Housing','Number of existing credits at this bank','Job','Number of people being liable to provide maintenance for','Telephone','foreign worker','Fraud Classification']
data = pd.read_table('german.data',delim_whitespace=True,names=colnames,header=None,index_col=False)

app = dash.Dash()
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Fraud Attributes',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='Credit Card Data.', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    dcc.Graph(
        id='Fraud_Attributes',
        figure={
            'data': [
                go.Histogram(x=data[i].astype('category').cat.codes,name=i)
                for i in data.columns

            ],
            'layout': go.Layout(
                xaxis={'autorange':'True','title': 'Attributes'},
                yaxis={'autorange':'True','title': 'Count'},

                hovermode='closest')



            }

    )
])

if __name__ == '__main__':
    app.run_server(debug=True)