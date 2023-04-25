#venv\Scripts\activate
import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
from dash import html, dcc

import plotly.express as px
import plotly.graph_objects as go

import json
import pandas as pd
import plotly.express as px
import geopandas as gpd
import plotly.graph_objects as go

from urllib.parse import unquote

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
server=app.server

mc1_data = pd.read_csv('mc1-reports-data.csv')
df_hourly = pd.read_csv('df_hourly.csv')
df_hourly_avg = pd.read_csv('hourly_avg.csv')

locations_dict = {
     "ALL": "St. Himark",
    "1": "Palace Hills",
    "2": "Northwest",
    "3": "Old Town",
    "4": "Safe Town",
    "5": "Southwest",
    "6": "Downtown",
    "7": "Wilson Forest",
    "8": "Scenic Vista",
    "9": "Broadview",
    "10": "Chapparal",
    "11": "Terrapin Springs",
    "12": "Pepper Mill",
    "13": "Cheddarford",
    "14": "Easton",
    "15": "Weston",
    "16": "Southton",
    "17": "Oak Willow",
    "18": "East Parton",
    "19": "West Parton"
}

with open('StHimark.geojson') as f:
    counties = json.load(f)
counties["features"]
geojson = counties
gdf = gpd.GeoDataFrame.from_features(geojson)
point = (-119.8454307, 0.135351852)

def make_empty_fig():
    fig = go.Figure()
    fig.layout.paper_bgcolor = '#E5ECF6'
    fig.layout.plot_bgcolor = '#E5ECF6'
    return fig

main_layout = html.Div([
    html.Div([
    dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Time Sense", href="sen")),
        dbc.NavItem(dbc.NavLink("Social", href="soc")),
    ],
    brand="Disaster at St. Himark!",
    brand_href="/",
    color="primary",
    dark=True,
    ),
    dbc.NavbarSimple([
        ]),
    dcc.Location(id='location'),
    html.Div(id='main_content'),
    html.Br(),
]),
    html.Br(),
],  style={'backgroundColor': '#E5ECF6'})

main_dashboard = html.Div([
        dbc.Row([
            dbc.Col(lg=1),
            dbc.Col([
                html.Div(
                    id='city-name',
                    children='No city selected'
                    ),
                    #dbc.Label('Select City'),
                    dcc.Dropdown(id='diff_dropdown',  style={ 'display': 'none' },
                         value='s1', options=[{'label': v, 'value': v}
                                  for v in ['s1', 's2']]  ),
                    html.Br(),
                ], md=12, lg=5),
                dbc.Col([
                    #dbc.Label('Some thing other'),
                    #dcc.Dropdown(id='ques_dropdown',
                    #     value='math_score',
                    #     options=[{'label': v, 'value': v}
                    #              for v in ['s1', 's2', 's3', 's4']]),
                    #html.Br(),
                ], md=12, lg=5),
                
        ], style={'backgroundColor': '#E5ECF6'}),
        dbc.Row([
        dbc.Col(lg=1),
        dbc.Col([
            #dbc.Label('Filter Education of Parents'),
            #dcc.Dropdown(id='edu_selector',
            #             multi=True,
            #             placeholder='Select one or more',
            #             options=[{'label': edu, 'value': edu}
            #                      for edu in ['parental', '_level', '_of', '_education']]), 
            
            dcc.Graph(id='map_graph',
                      figure=make_empty_fig()),
            html.Br(),
            dcc.Graph(id='rate_graph',
                      figure=make_empty_fig()),
            ], md=12, lg=5),
        dbc.Col([
            #dbc.Label('Filter Ethnicity'),
            #dcc.Slider(1, 6, step=None, id='ethnicity_slider',
            #           marks={
            #               1: 'Group A',
            #               2: 'Group B',
            #               3: 'Group C',
            #               4: 'Group D',
            #               5: 'Group E',
            #               6: "All"
            #           },
            #           value=6
            #          ),
            dcc.Graph(id='shake_line_graph',
                      figure=make_empty_fig()),
            html.Br(),
            dcc.Graph(id='utility_graph',
                      figure=make_empty_fig()),
            html.Br(),
            ], md=12, lg=5),
        ]),
    dbc.Row([
        dbc.Col(lg=1),
        
      
        dbc.Col([
   
            
        ], md=12, lg=5),
    ]),
], style={'backgroundColor': '#E5ECF6'})

sen_dashboard = html.Div([
    dbc.Row([
        dbc.Col(lg=1),
        # dcc.RadioItems(
        # id='days_list',
        # options=[
        #     {'label': 'Day 1', 'value': '2020-04-06'},
        #     {'label': 'Day 2', 'value': '2020-04-07'},
        #     {'label': 'Day 3', 'value': '2020-04-08'},
        #     {'label': 'Day 4', 'value': '2020-04-09'},
        #     {'label': 'Day 5', 'value': '2020-04-10'},
        # ],
        #     value='4/6/2020'
        # ),
        # html.Br(),
        # dcc.RadioItems(
        # id='hours_list',
        # options=[
        #     {'label': '12 AM', 'value': '00'},
        #     {'label': '1 AM', 'value': '01'},
        #     {'label': '2 AM', 'value': '02'},
        #     {'label': '3 AM', 'value': '03'},
        #     {'label': '4 AM', 'value': '04'},
        #     {'label': '5 AM', 'value': '05'},
        #     {'label': '6 AM', 'value': '06'},
        #     {'label': '7 AM', 'value': '07'},
        #     {'label': '8 AM', 'value': '08'},
        #     {'label': '9 AM', 'value': '09'},
        #     {'label': '10 AM', 'value': '10'},
        #     {'label': '11 AM', 'value': '11'},
        #     {'label': '12 PM', 'value': '12'},
        #     {'label': '1 PM', 'value': '13'},
        #     {'label': '2 PM', 'value': '14'},
        #     {'label': '3 PM', 'value': '15'},
        #     {'label': '4 PM', 'value': '16'},
        #     {'label': '5 PM', 'value': '17'},
        #     {'label': '6 PM', 'value': '18'},
        #     {'label': '7 PM', 'value': '19'},
        #     {'label': '8 PM', 'value': '20'},
        #     {'label': '9 PM', 'value': '21'},
        #     {'label': '10 PM', 'value': '22'},
        #     {'label': '11 PM', 'value': '23'},
            
        # ],
        #     value='00'
        # ),
        
        dbc.Col([
            dcc.Dropdown(id='diff3_dropdown',  style={ 'display': 'none' },
                         value='s1', options=[{'label': v, 'value': v}
                                  for v in ['s1', 's2']]  ),
            dcc.Graph(id='heatmap_graph',
                           figure=make_empty_fig()),
        
        
        
        
        #     html.Br(),
        #     dcc.Graph(id='lunch_dist_graph',
        #               figure=make_empty_fig()),
        #     html.Br(),
        #     dcc.Graph(id='math_dist_graph',
        #               figure=make_empty_fig()),
        #     html.Br(),
        #     dcc.Graph(id='write_dist_graph',
        #               figure=make_empty_fig()),
             ], md=12, lg=10),
            
    ]),
    
], style={'backgroundColor': '#E5ECF6'})

soc_dashboard = html.Div([
     dbc.Row([
         dbc.Col(lg=1),
         dbc.Col([
            dcc.Dropdown(id='diff2_dropdown',  style={ 'display': 'none' },
                         value='s1', options=[{'label': v, 'value': v}
                                  for v in ['s1', 's2']]  ),
             dcc.Graph(id='tweet_graph',
                           figure=make_empty_fig()),
    #         html.Br(),
    #         dcc.Graph(id='ethnicity_score_graph',
    #                       figure=make_empty_fig()),
    #         html.Br(),
    #         dcc.Graph(id='parental_score_graph',
    #                       figure=make_empty_fig()),
    #         html.Br(),
    #         dcc.Graph(id='lunch_score_graph',
    #                       figure=make_empty_fig()),
    #         dcc.Graph(id='test_score_graph',
    #                       figure=make_empty_fig()),
                 ], md=12, lg=10),
         ]),
    
], style={'backgroundColor': '#E5ECF6'})

app.validation_layout = html.Div([
    main_layout,
    main_dashboard,
    sen_dashboard,
    soc_dashboard,
])


app.layout = main_layout

def filter_data(location, filtered):
    
    if location is not None:
        filtered = filtered[filtered['location'] == location]
    else:
        location = 0
    return filtered

#this method updates the layout to order and main 
@app.callback(Output('main_content', 'children'),
              Input('location', 'pathname'))
def display_content(pathname):
    if unquote(pathname[1:]) in ['sen']:
        return sen_dashboard
    elif unquote(pathname[1:]) in ['soc']:
        return soc_dashboard
    else:
        return main_dashboard
    
#This method plots the main figures with input from user
@app.callback(Output('map_graph', 'figure'),
              Input('diff_dropdown', 'value'),
            )
def display_main(diff):
    #map figure with boxes
    fig1 = px.choropleth_mapbox(gdf, geojson=gdf.geometry, locations=gdf.Id,
                           color="Nbrhood", center={"lat": point[1], "lon": point[0]},
                           mapbox_style="open-street-map", zoom=10)    

    return fig1

@app.callback(    
    Output('city-name', 'children'),
    Output('shake_line_graph', 'figure'),
    Output('rate_graph', 'figure'),
    Output('utility_graph', 'figure'),
    [Input('map_graph', 'clickData')]
)
def update_city_details(click_data):
    location = 'ALL'
    dataframe = df_hourly
    if click_data is not None:
        location = click_data['points'][0]['location']
        dataframe = filter_data(location, df_hourly_avg)
        #return f"City selected: {dataframe.shape}"
    else:
        dataframe = df_hourly
    
    fig4 = px.line(dataframe, x='timestamp', y='shake_intensity')

    # Set the title and axis labels
    fig4.update_layout(title='Hourly Average Shake Intensity - ' + locations_dict[str(location)], xaxis_title="Date", yaxis_title="Intensity")
    fig4.update_xaxes(rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1d", step="day", stepmode="backward"),
            dict(count=2, label="2d", step="day", stepmode="backward"),
            dict(count=3, label="3d", step="day", stepmode="backward"),
            dict(step="all")
            ])
        )
    )

    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=dataframe['timestamp'], y=dataframe['roads_and_bridges'], name='Roads and Bridges'))
    fig3.add_trace(go.Scatter(x=dataframe['timestamp'], y=dataframe['medical'], name='Medical'))
    fig3.add_trace(go.Scatter(x=dataframe['timestamp'], y=dataframe['buildings'], name='Buildings'))
    fig3.update_layout(
        title='Average Ratings of Infrastructure - ' + locations_dict[str(location)],
        height=600, xaxis_title="Date")

    fig3.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1d", step="day", stepmode="backward"),
                dict(count=2, label="2d", step="day", stepmode="backward"),
                dict(count=3, label="3d", step="day", stepmode="backward"),
                dict(step="all")
            ])
        )
    )

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=dataframe['timestamp'], y=dataframe['sewer_and_water'], name='Sewer and Water'))
    fig2.add_trace(go.Scatter(x=dataframe['timestamp'], y=dataframe['power'], name='Power'))
    fig2.update_layout(
        title='Average Ratings of Utilities - ' + locations_dict[str(location)],
        height=600, xaxis_title="Date")

    fig2.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1d", step="day", stepmode="backward"),
                dict(count=2, label="2d", step="day", stepmode="backward"),
                dict(count=3, label="3d", step="day", stepmode="backward"),
                dict(step="all")
            ])
        )
    )
    return f"Location: {locations_dict[str(location)]}", fig4, fig3, fig2


#This method plots the main figures with input from user
@app.callback(Output('tweet_graph', 'figure'),
               Input('diff2_dropdown', 'value'),
              )
def display_dist(ethnicity):
    tweets = pd.read_csv("tweets.csv")
    fig1 = px.scatter(tweets, x="time", y="location", color='location', hover_name="account", height=800, hover_data=['time', 'message'])
    
    return fig1


#This method plots the main figures with input from user
@app.callback(Output('heatmap_graph', 'figure'),
               Input('diff3_dropdown', 'value'),
              )
def display_scores_box(ethnicity):
    fig2 = go.Figure(data=go.Heatmap(
        z=mc1_data['shake_intensity'],
        x=pd.to_datetime(mc1_data['time']),
        y=mc1_data['location'],
        hovertemplate=
        "<b>%{y}</b><br><br>" +
        "Shake Intesity: %{z:,.1f}<br>" +
        "Time: %{x}<br>",
        colorscale='Viridis'))

    fig2.update_layout(
        title='Shake Intensity ', height=800,
        xaxis_title="Date")

    fig2.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1d", step="day", stepmode="backward"),
                dict(count=2, label="2d", step="day", stepmode="backward"),
                dict(count=3, label="3d", step="day", stepmode="backward"),
                dict(step="all")
                ])
            )
        )    
    return fig2

    
if __name__ == '__main__':
    app.run_server(debug=True)