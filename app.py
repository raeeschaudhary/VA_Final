import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
from dash import html, dcc

import plotly.express as px
import plotly.graph_objects as go

import pandas as pd

from urllib.parse import unquote

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server=app.server

def make_empty_fig():
    fig = go.Figure()
    fig.layout.paper_bgcolor = '#E5ECF6'
    fig.layout.plot_bgcolor = '#E5ECF6'
    return fig

main_layout = html.Div([
    html.Div([
    dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Distribution", href="dist")),
        dbc.NavItem(dbc.NavLink("Score Ranges", href="score")),
    ],
    brand="Student Performance - Data Visualization",
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
                    dbc.Label('Differentiating Variable'),
                    html.Br(),
                    dcc.Dropdown(id='diff_dropdown',
                         value='gender', options=[{'label': v, 'value': v} 
                                                  for v in ['gender', 'ethnicity', 'parental_level_of_education', 'lunch', 'test_preparation_course']]),
                ], md=12, lg=4),
                dbc.Col([
                    dbc.Label('Score to Compare'),
                    dcc.Dropdown(id='ques_dropdown',
                         value='math_score',
                         options=[{'label': v, 'value': v}
                                  for v in ['math_score', 'reading_score', 'writing_score', 'overall']]),
                ], md=12, lg=3),
                dbc.Col([
                    dbc.Label('Compare Score Against'),
                    dcc.Dropdown(id='comp_dropdown',
                         value='overall',
                         options=[{'label': v, 'value': v}
                                  for v in ['math_score', 'reading_score', 'writing_score', 'overall']]),
                ], md=12, lg=3),
        ], style={'backgroundColor': '#E5ECF6'}),
        dbc.Row([
        dbc.Col(lg=1),
        dbc.Col([
            dbc.Label('Filter Education of Parents'),
            dcc.Dropdown(id='edu_selector',
                         multi=True,
                         placeholder='Select one or more',
                         options=[{'label': edu, 'value': edu}
                                  for edu in ['parental', '_level', '_of', '_education']]), 
            
            dcc.Graph(id='comparison_graph',
                      figure=make_empty_fig()),
            ], md=12, lg=5),
        dbc.Col([
            dbc.Label('Filter Ethnicity'),
            dcc.Slider(1, 6, step=None, id='ethnicity_slider',
                       marks={
                           1: 'Group A',
                           2: 'Group B',
                           3: 'Group C',
                           4: 'Group D',
                           5: 'Group E',
                           6: "All"
                       },
                       value=6
                      ),
            dcc.Graph(id='heatmap_graph',
                      figure=make_empty_fig()),
            html.Br(),
            ], md=12, lg=5),
        ]),
    dbc.Row([
        dbc.Col(lg=1),
        dbc.Col([
            html.H1('Assignment 5: Interactive Data Visualization with Plotly and Dash'),
            html.Hr(),
            html.H3('Muhammad Raees (mr2714), Ali Khalid (ak5013), Kaleem Nawaz Khan (kk5271)'), 
            html.H3('ISTE-782, Spring 2023'),
            html.Hr(),
            html.Div([
                html.P('In this dashboard, we explored and visualized a dataset'),
                html.A(dbc.Button('View Dataset', id='record-info-btn', 
                      className='btn btn-orange align-middle btn btn-secondary'), 
                       href='http://roycekimmons.com/tools/generated_data/exams'),
                html.P('Dataset contains information about the scores of students in math, reading, ' + 
                       'and writing. Together with the exam results, it also lists the students ' + 
                       'ethnicity or race, gender, the level of education of their parents, and if ' + 
                       'they have access to regular meals and test preparation classes. We examined ' + 
                       'the data in detail in the last assignment, and in this work, we would like to ' + 
                       'provide interactivity features to the users through a Plotly Dashboard to examine, ' + 
                       'evaluate, and interact with the dataset. The interactive features will provide users to ' + 
                       'dynamically select the data, apply filters, analyze, and visually interpret the results. ' + 
                       'The main graph of this interactive dashboard is a scatter plot, which allows users to ' + 
                       'visualize and evaluate the test scores of students and identify patterns. To make the ' + 
                       'graph more interactive, we provided control to the users to dynamically select the scores ' + 
                       'to compare. For instance, a user can compare any type of test score with another type of ' + 
                       'test score (including the overall score which we calculate as an average). ' + 
                       'To add more interactivity, we allow users to compare the scores across various ' + 
                       'differentiating factors like gender, ethnicity, whether they get lunches, practice, etc. ' + 
                       'We provide these options to the users through a set of drop-drop options at the top. ' + 
                       'Additionally, the user can filter out data based on the education level of parents ' + 
                       'with multi-selection in a drop-down. Our data does not inherently contain a range of ' + 
                       'numeric data which might be useful for a slider. However, we use the ethnic background of the ' + 
                       'user on a categorical slider to choose from a set of ethnicities present in the dataset. ' + 
                       'Evidently, we can visualize and interact with data more vividly through the Plotly Dash ' + 
                       'application. We designed the application into multiple pages so that the visualization ' + 
                       'is separated effectively. The second graph on the homepage shows the correlation between each ' + 
                       'type of score. All the graphs are interactive with all the controls provided in the application. ' + 
                       'We also provide the distribution of the data similar to the last assignment. ' + 
                       'The user can navigate to the "Distribution" page from the top of the page to access ' + 
                       'different distributions.'),
                html.H3('Explore the other tabs from the top navigation to learn more about the data through interactive graphs'), 
            ] ,style={'text-align': 'justify'}),

            ], md=12, lg=10),
        dbc.Col([
            
        ], md=12, lg=5),
    ]),
], style={'backgroundColor': '#E5ECF6'})

dist_dashboard = html.Div([
    dbc.Row([
        dbc.Col(lg=1),
        dbc.Col([
            dbc.Label('Filter Education of Parents'),
            dcc.Dropdown(id='edu_selector1',
                         multi=True,
                         placeholder='Select one or more',
                         options=[{'label': edu, 'value': edu}
                                  for edu in ['parental', 'level', 'of', 'education']]),
            html.Br(),
            dcc.Graph(id='gender_dist_graph',
                      figure=make_empty_fig()),
            html.Br(),
            dcc.Graph(id='parental_dist_graph',
                      figure=make_empty_fig()),
            html.Br(),
            dcc.Graph(id='test_dist_graph',
                      figure=make_empty_fig()),
            html.Br(),
            dcc.Graph(id='read_dist_graph',
                      figure=make_empty_fig()),
            ], md=12, lg=5),
        dbc.Col([ 
            dbc.Label('Filter Ethnicity'),
            dcc.Slider(1, 6, step=None, id='ethnicity_slider1',
                       marks={
                           1: 'Group A',
                           2: 'Group B',
                           3: 'Group C',
                           4: 'Group D',
                           5: 'Group E',
                           6: "All"
                       },
                       value=6
                      ),
            html.Br(),
            dcc.Graph(id='ethnicity_dist_graph',
                      figure=make_empty_fig()),
            html.Br(),
            dcc.Graph(id='lunch_dist_graph',
                      figure=make_empty_fig()),
            html.Br(),
            dcc.Graph(id='math_dist_graph',
                      figure=make_empty_fig()),
            html.Br(),
            dcc.Graph(id='write_dist_graph',
                      figure=make_empty_fig()),
            ], md=12, lg=5),
            
    ]),
    
], style={'backgroundColor': '#E5ECF6'})

score_dashboard = html.Div([
    dbc.Row([
        dbc.Col(lg=1),
        dbc.Col([
            dbc.Label('Filter Education of Parents'),
            dcc.Dropdown(id='edu_selector2',
                         multi=True,
                         placeholder='Select one or more',
                         options=[{'label': edu, 'value': edu}
                                  for edu in ['parental_level_of_education']]),
            html.Br(),
            ], md=12, lg=5),
        dbc.Col([ 
            dbc.Label('Filter Ethnicity'),
            dcc.Slider(1, 6, step=None, id='ethnicity_slider2',
                       marks={
                           1: 'Group A',
                           2: 'Group B',
                           3: 'Group C',
                           4: 'Group D',
                           5: 'Group E',
                           6: "All"
                       },
                       value=6
                      ),
            ], md=12, lg=5),
        ]),
    dbc.Row([
        dbc.Col(lg=1),
        dbc.Col([
            dcc.Graph(id='gender_score_graph',
                          figure=make_empty_fig()),
            html.Br(),
            dcc.Graph(id='ethnicity_score_graph',
                          figure=make_empty_fig()),
            html.Br(),
            dcc.Graph(id='parental_score_graph',
                          figure=make_empty_fig()),
            html.Br(),
            dcc.Graph(id='lunch_score_graph',
                          figure=make_empty_fig()),
            dcc.Graph(id='test_score_graph',
                          figure=make_empty_fig()),
                ], md=12, lg=10),
        ]),
    
], style={'backgroundColor': '#E5ECF6'})

app.validation_layout = html.Div([
    main_layout,
    main_dashboard,
    dist_dashboard,
    score_dashboard,
])


app.layout = main_layout

def filter_data(edu_levels, ethnicity, filtered):
    group = ""
    if edu_levels:
        filtered = filtered[filtered['parental_level_of_education'].isin(edu_levels)]
    if ethnicity == 1:
        group = 'group A'
        filtered = filtered[filtered['ethnicity'] == group]
    elif ethnicity == 2:
        group = "group B"
        filtered = filtered[filtered['ethnicity'] == group]
    elif ethnicity == 3:
        group = "group C"
        filtered = filtered[filtered['ethnicity'] == group]
    elif ethnicity == 4:
        group = "group D"
        filtered = filtered[filtered['ethnicity'] == group]
    elif ethnicity == 5:
        group = "group E"
        filtered = filtered[filtered['ethnicity'] == group]
    else:
        group = ""
    return filtered

#this method updates the layout to order and main 
@app.callback(Output('main_content', 'children'),
              Input('location', 'pathname'))
def display_content(pathname):
    if unquote(pathname[1:]) in ['dist']:
        return dist_dashboard
    elif unquote(pathname[1:]) in ['score']:
        return score_dashboard
    else:
        return main_dashboard
    


#This method plots the main figures with input from user
@app.callback(Output('gender_dist_graph', 'figure'),
              Output('ethnicity_dist_graph', 'figure'),
              Output('parental_dist_graph', 'figure'),
              Output('lunch_dist_graph', 'figure'),
              Output('test_dist_graph', 'figure'),
              Output('math_dist_graph', 'figure'),
              Output('read_dist_graph', 'figure'),
              Output('write_dist_graph', 'figure'),
              Input('edu_selector1', 'value'),
              Input('ethnicity_slider1', 'value'),
             )
def display_dist(edu_levels, ethnicity):
    
    
    return make_empty_fig, make_empty_fig, make_empty_fig, make_empty_fig, make_empty_fig, make_empty_fig, make_empty_fig, make_empty_fig


#This method plots the main figures with input from user
@app.callback(Output('gender_score_graph', 'figure'),
              Output('ethnicity_score_graph', 'figure'),
              Output('parental_score_graph', 'figure'),
              Output('lunch_score_graph', 'figure'),
              Output('test_score_graph', 'figure'),
              Input('edu_selector2', 'value'),
              Input('ethnicity_slider2', 'value'),
             )
def display_scores_box(edu_levels, ethnicity):
    
    
    return make_empty_fig, make_empty_fig, make_empty_fig, make_empty_fig, make_empty_fig

    
if __name__ == '__main__':
    app.run_server(debug=True)