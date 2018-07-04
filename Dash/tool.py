# -*- coding: utf-8 -*-
"""
Created on Thu Jun 28 02:30:45 2018

@author: ratanond
"""
import pandas as pd
import dash 
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

app = dash.Dash()

wilson = pd.read_csv('./final_data/wilson_final.csv')
babolat = pd.read_csv('./final_data/babolat_final.csv')
head = pd.read_csv('./final_data/head_final.csv')
yonex = pd.read_csv('./final_data/yonex_final.csv')

df = pd.concat([wilson,babolat,head,yonex],ignore_index=True)

app.layout = html.Div(children=[
    html.Div([html.B(children='Choose your swing speed')]),
    dcc.Dropdown(
        id = 'swingspeed',
        options = [
            {'label': 'Fast, Long', 'value':'Fast, Long'},
            {'label': 'Medium, Moderate', 'value':'Medium, Moderate'},
            {'label': 'Slow, Compact', 'value':'Slow, Compact'}
        ],
        value = 'Fast, Long',
        #multi =True
    ),
    html.Br(),
    html.Br(),
    html.Div([html.B(children='Choose your desired power')]),
    dcc.Dropdown(
        id = 'power',
        options = [
            {'label': 'High', 'value':'High'},
            {'label': 'Medium', 'value':'Medium'},
            {'label': 'Low', 'value':'Low'}
        ],
        value = 'Low'
    ),
    html.Br(),
    html.Br(),
    html.Div([html.B(children='Horizontal axis')]),
    dcc.Dropdown(
        id = 'x_axis',
        options = [
            {'label': 'Swingweight', 'value':'Swingweight (g.)'},
            {'label': 'Flex', 'value':'Flex'},
            {'label': 'Head Size', 'value':'Head_Size (in.^2)'},
            {'label': 'Price', 'value':'Price($)'} 
        ],
        value = 'Swingweight (g.)'
    ),
    html.Br(),
    html.Br(),
    html.Div([html.B(children='Vertical axis')]),
    dcc.Dropdown(
        id = 'y_axis',
        options = [
            {'label': 'Swingweight', 'value':'Swingweight (g.)'},
            {'label': 'Flex', 'value':'Flex'},
            {'label': 'Head Size', 'value':'Head_Size (in.^2)'},
            {'label': 'Price', 'value':'Price($)'}
        ],
        value = 'Flex'
    ),
    html.Br(),
    html.Br(),
    html.Div([html.B(children='Choose racket balance')]),
    dcc.RadioItems(
        id = 'balance',
        options = [
            {'label':'Head Light (HL)','value':'HL'},
            {'label':'Head Heavy (HH)','value':'HH'}
        ],
        value = 'HL'
    ),
    html.Br(),
    html.Br(),
    html.Div([html.B(children='Choose HH/HL level')]),
    dcc.Slider(
        id = 'balance_point',
        marks = {i: '{}'.format(i) for i in range(14)},
        #count = 1,
        min = 0,
        max = 13,
        #step = 1,
        value = 7
    ),
    html.Br(),
    html.Br(),
    html.Div([html.B(children='Results')]),
    dcc.Graph(id = 'comparison plot')
])

@app.callback(
    dash.dependencies.Output('comparison plot','figure'),
    [dash.dependencies.Input('swingspeed','value'),
     dash.dependencies.Input('power','value'),
     dash.dependencies.Input('x_axis','value'),
     dash.dependencies.Input('y_axis','value'),
     dash.dependencies.Input('balance','value'),
     dash.dependencies.Input('balance_point','value')])
def update_graph(swing_speed,racket_power,x_axis,y_axis,balance,balance_point):
    dff = df[df['Swing_speed']==swing_speed]
    dff = dff[dff['Power_Level']==racket_power]
    dff['Balance_Points']=dff['Balance_Points'].astype('int64')

    return{
        'data': [go.Scatter(
            x = dff[(dff['Balance_Type']==balance) & (dff['Balance_Points']==balance_point)][x_axis],    
            y = dff[(dff['Balance_Type']==balance) & (dff['Balance_Points']==balance_point)][y_axis],
            
            mode = 'markers',
            text = dff['Racket_Name'],
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
            
        )],
        'layout':go.Layout(
            xaxis = {
                'title':x_axis
            },
            yaxis = {
                'title':y_axis
            },
            #margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
            
        
        )            
    }

if __name__ == '__main__':
    app.run_server(debug=True)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    