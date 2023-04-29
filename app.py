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
     "ALL": "St. Himark", "1": "Palace Hills", "2": "Northwest", "3": "Old Town", "4": "Safe Town", "5": "Southwest", "6": "Downtown", "7": "Wilson Forest", "8": "Scenic Vista", "9": "Broadview", 
     "10": "Chapparal", "11": "Terrapin Springs", "12": "Pepper Mill", "13": "Cheddarford", "14": "Easton", "15": "Weston", "16": "Southton", "17": "Oak Willow", "18": "East Parton",  "19": "West Parton" }

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
        dbc.NavItem(dbc.NavLink("Shake Sense", href="sen")),
        dbc.NavItem(dbc.NavLink("Social", href="soc")),
    ],
    brand="HimarkDash - Dashboad",
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
                ], md=12, lg=5),
                
        ], style={'backgroundColor': '#E5ECF6'}),
        dbc.Row([
        dbc.Col(lg=1),
        dbc.Col([
            
            dcc.Graph(id='map_graph',
                      figure=make_empty_fig()),
            html.Br(),
            dcc.Graph(id='rate_graph',
                      figure=make_empty_fig()),
            ], md=12, lg=5),
        dbc.Col([
            dcc.Graph(id='shake_line_graph',
                      figure=make_empty_fig()),
            html.Br(),
            dcc.Graph(id='utility_graph',
                      figure=make_empty_fig()),
            html.Br(),
            ], md=12, lg=5),
        ]),
    
], style={'backgroundColor': '#E5ECF6'})

sen_dashboard = html.Div([
    dbc.Row([
        dbc.Col(lg=1),
        dbc.Col([
            dcc.Dropdown(id='diff3_dropdown',  style={ 'display': 'none' },
                         value='s1', options=[{'label': v, 'value': v}
                                  for v in ['s1', 's2']]  ),
            dcc.Graph(id='heatmap_graph',
                           figure=make_empty_fig()),
             ], md=12, lg=10),
            
    ]),
    
], style={'backgroundColor': '#E5ECF6'})

soc_dashboard = html.Div([
    dbc.Row([
            dbc.Col(lg=1),
            dbc.Col([
                html.Div(
                    id='city-name1',
                    children='No city selected'
                    ),
                    #dbc.Label('Select City'),
                    dcc.Dropdown(id='diff2_dropdown',  style={ 'display': 'none' },
                         value='s1', options=[{'label': v, 'value': v}
                                  for v in ['s1', 's2']]  ),
                    html.Br(),
                ], md=12, lg=5),
                dbc.Col([
                ], md=12, lg=5),
                
        ], style={'backgroundColor': '#E5ECF6'}),
        dbc.Row([
        dbc.Col(lg=1),
        dbc.Col([
            
            dcc.Graph(id='map1_graph',
                      figure=make_empty_fig()),
            html.Br(),
            dcc.Graph(id='user_graph',
                      figure=make_empty_fig()),
            ], md=12, lg=5),
        dbc.Col([
            dcc.Graph(id='tweet_time_graph',
                           figure=make_empty_fig()),
            html.Br(),
            dcc.Graph(id='tweet_graph',
                           figure=make_empty_fig()),
            ], md=12, lg=5),
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

@app.callback(Output('map1_graph', 'figure'),
              Input('diff2_dropdown', 'value'),
            )
def display_main1(diff):
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
@app.callback(Output('city-name1', 'children'),
              Output('tweet_graph', 'figure'),
              Output('tweet_time_graph', 'figure'),
              Output('user_graph', 'figure'),
              [Input('map1_graph', 'clickData')]
              )
def display_dist(click_data):
    location = 'ALL'
    tweets = pd.read_csv("tweets.csv")
    result = pd.read_csv('tweets_time.csv')
    fig1 = px.scatter(tweets, x="time", y="location", color='location', hover_name="account", height=600, hover_data=['time', 'message'])
    
    if click_data is not None:
        location = click_data['points'][0]['location']
        location = locations_dict[str(location)]
        tweets = filter_data(location, tweets)
        result = filter_data(location, result)
        #return f"City selected: {dataframe.shape}"
    
    fig2 = px.scatter(result, x='timestamp', y="message", hover_data={"location", 'timestamp', 'message'})
    fig2.update_layout(title='Hourly Social Media Activity - ' + location, xaxis_title="Date", yaxis_title="Messages")
    fig2.update_xaxes(rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1d", step="day", stepmode="backward"),
                dict(count=2, label="2d", step="day", stepmode="backward"),
                dict(count=3, label="3d", step="day", stepmode="backward"),
                dict(step="all")
                ])
            )
        )
    dfg = tweets.groupby([tweets['location'], tweets['account']]).size().to_frame().sort_values([0], ascending = False).head(10).reset_index()
    fig3 = px.histogram(dfg, x='account', y=0, labels={'account':'Account'},  height=600)
    fig3.update_layout(title='Top Active Accounts - ' + location, yaxis_title="Messages")
    
    return f"Location: {location}", fig1, fig2, fig3


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