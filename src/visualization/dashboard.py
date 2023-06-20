import pandas as pd
import numpy as np
import plotly.express as px
import plotly.colors as colors
import plotly.graph_objects as go
import dash
from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from functions.data_managing import *


# ======================================================================================================================
# Import Pandas Dataframe & Initialize APP
# ======================================================================================================================

mb_style = "mapbox://styles/santiagopereda/clinlvecs002d01p73lb45noj"
pickle_loc = "../../data/interim/01_data_processed.pkl"
pickle_loc_2 = "../../data/interim/02_data_processed.pkl"
df = pd.read_pickle(pickle_loc)
df = df.rename(columns=col_name_replace)

df_2 = pd.read_pickle(pickle_loc_2)
df_3_loc = '../../data/raw/countries of the world.csv'

df_3 = pd.read_csv(df_3_loc)

areas = df_3['Area (sq. mi.)']
country_size = np.percentile(areas, np.arange(0, 101, 10))

bar_chart_cols = ['PCT Plastic And Foam', 'PCT Glass Rubber Lumber Metal',
                  'Plastic Beverage Bottles', 'Other Plastic Bottles',
                  'Plastic Bottle Caps', 'Food Containers', 'Buckets Or Crates',
                  'Lighters', 'Other Hard Plastics', 'Plates Bowls Cups',
                  'Personal Care Products', 'Lollipop Stick', 'Bag', 'Wrapper Or Label',
                  'Straws', 'Other Soft Plastics', 'Cigarette Butts', 'String Ring',
                  'Fishing Nets', 'Fishing Lines', 'Fishing Buoys', 'Foam Plastic Debris',
                  'Other Plastic Debris', 'Plastic Straps', 'Fishing Glow Sticks',
                  'Other Fishing Plastic Debris']
item_dropdown_cols = ['PCT Plastic And Foam', 'PCT Glass Rubber Lumber Metal',
                      'Plastic Beverage Bottles', 'Other Plastic Bottles',
                      'Plastic Bottle Caps', 'Food Containers', 'Buckets Or Crates',
                      'Lighters', 'Other Hard Plastics', 'Plates Bowls Cups',
                      'Personal Care Products', 'Lollipop Stick', 'Bag', 'Wrapper Or Label',
                      'Straws', 'Other Soft Plastics', 'Cigarette Butts', 'String Ring',
                      'Fishing Nets', 'Fishing Lines', 'Fishing Buoys', 'Foam Plastic Debris',
                      'Other Plastic Debris', 'Plastic Straps', 'Fishing Glow Sticks',
                      'Other Fishing Plastic Debris', 'Total Pieces Collected']

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

# ======================================================================================================================
# App layout
# ======================================================================================================================
app.layout = dbc.Container([
    html.Div(children=[
        dbc.Row([
            html.Div([
                dbc.Row([
                    dbc.Col(
                        html.H5("Global Earth Challenge Report",
                                style={'text-left': 'center', 'color': 'white', "margin-top": "5px"})
                    ),
                    dbc.Col(
                        html.Div([
                            html.Link(
                                rel='stylesheet',
                                href='/assets/styles.css'
                            ),
                            dcc.Dropdown(
                                options=[{'label': option, 'value': option}
                                         for option in item_dropdown_cols],

                                id="items-dropdown",
                                placeholder="Select Item",
                                maxHeight=200,
                                style={"background-color": 'transparent',
                                       'fontSize': '16px', "margin-top": "5px"},
                            ),
                        ])
                    ),
                    dbc.Col(
                        html.Div([
                            html.Link(
                                rel='stylesheet',
                                href='/assets/styles.css'
                            ),
                            dcc.Dropdown(
                                options=[{'label': option, 'value': option}
                                         for option in df_2.index.get_level_values(0).unique()],
                                id="continent-dropdown",
                                placeholder="Select a Continent",
                                maxHeight=200,
                                style={"background-color": 'transparent',
                                       'fontSize': '16px', "margin-top": "5px"},
                            ),
                        ])

                    ),
                    dbc.Col(
                        html.Div([
                            html.Link(
                                rel='stylesheet',
                                href='/assets/styles.css'
                            ),
                            dcc.Dropdown(
                                id="country-dropdown",
                                placeholder="Select Country",
                                maxHeight=200
                            ),
                        ])
                    ),
                    dbc.Col(
                        html.Div([
                            html.Link(
                                rel='stylesheet',
                                href='/assets/styles.css'
                            ),
                            dcc.Dropdown(
                                id="subdivision-dropdown",
                                placeholder="Select State",
                                maxHeight=200
                            ),
                        ])

                    ),
                ])
            ], className='my-dropdown'),
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader("Organizations"),
                            dbc.CardBody([
                                html.Div(id='organization_count'),
                                html.Div([
                                    dbc.Button("Go somewhere",
                                               color="primary", size="sm"),
                                ])
                            ]),
                        ], className="mb-3",
                        ),
                    ]),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader("Participants"),
                            dbc.CardBody([
                                html.Div(id='partcipant_count'),
                                html.Div([
                                    dbc.Button("Go somewhere",
                                               color="primary", size="sm"),
                                ])
                            ]),
                        ], className="mb-3",
                        ),
                    ]),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader("Items Collected"),
                            dbc.CardBody([
                                html.Div(id='item_count'),
                                html.Div([
                                    dbc.Button("Go somewhere",
                                               color="primary", size="sm"),
                                ])
                            ]),
                        ], className="mb-3",
                        ),
                    ]),

                ]),
                dbc.Row(
                    dbc.Col([
                        html.Div([
                            dcc.Graph(id='sunburst_chart', figure={}),
                        ]),
                    ])
                ),
                dbc.Row(

                )
            ], width=6),

            dbc.Col([
                dbc.Stack([
                    html.Div([
                        dcc.Graph(id='eac_map', figure={})
                    ]),
                    html.Br(),
                    html.Div([
                        dcc.RangeSlider(
                            id='year_slice',
                            min=df.index.year.min(),
                            max=df.index.year.max(),
                            step=1,
                            value=[df.index.year.min(), (df.index.year.max())],
                            marks=None,
                            allowCross=False,
                            tooltip={"placement": "bottom",
                                     "always_visible": True},
                        )
                    ]),
                    html.Div(
                        id='output_container_1',
                        children=[],
                        style={'display': 'none'},
                    ),
                    html.Div(
                        id='output_container_2',
                        children=[],
                        style={'display': 'none'},
                    ),
                ], gap=3)
            ], width=6)
        ], justify="center")
    ]),
], style={"height": "100vh"}, fluid=True)

# ======================================================================================================================
# Connect the Plotly graphs with Dash Components
# ======================================================================================================================


@app.callback(
    [Output(component_id='eac_map', component_property='figure'),
     Output(component_id='sunburst_chart', component_property='figure'),
     Output(component_id='output_container_1', component_property='children'),
     Output(component_id='output_container_2', component_property='children'),
     Output(component_id='country-dropdown', component_property='options'),
     Output(component_id='country-dropdown', component_property='style'),
     Output(component_id='country-dropdown', component_property='value'),
     Output(component_id='subdivision-dropdown', component_property='options'),
     Output(component_id='subdivision-dropdown', component_property='style'),
     Output(component_id='subdivision-dropdown', component_property='value'),
     Output(component_id='organization_count', component_property='children'),
     Output(component_id='partcipant_count', component_property='children'),
     Output(component_id='item_count', component_property='children')],
    [Input(component_id='year_slice', component_property='value'),
     Input(component_id="continent-dropdown", component_property='value'),
     Input(component_id="country-dropdown", component_property='value'),
     Input(component_id="subdivision-dropdown", component_property='value'),
     Input(component_id="items-dropdown", component_property='value')]
)
# ======================================================================================================================
# Function to update Graphs in Dahsboard
# ======================================================================================================================
def update_graph(year_slice, continent_dropdown_value, country_dropdown_value, subdivision_dropdown_value, item_dropdown_value):

    # ======================================================================================================================
    # Date and Location filtering
    # ======================================================================================================================
    dff = df.copy()

    start_year, end_year = year_slice[0], year_slice[1]

    filtered_data = dff.loc[str(start_year):str(end_year)]

    country_list = sorted(
        filtered_data.loc[filtered_data["Continent"] == continent_dropdown_value, 'Country'].unique())

    subdivisions_list = sorted(
        filtered_data.loc[filtered_data["Country"] == country_dropdown_value, 'State'].unique())

    if continent_dropdown_value is None and country_dropdown_value is None and subdivision_dropdown_value is None:
        country_options = []
        country_style = {'display': 'none'}
        subdivision_options = []
        subdivision_style = {'display': 'none'}
        filtered_data = dff.loc[str(start_year):str(end_year)]
        country_center = dict(lat=20, lon=15)

    elif continent_dropdown_value is not None and (country_dropdown_value is None or len(country_dropdown_value) < 1):
        country_options = [{'label': country, 'value': country}
                           for country in country_list]
        country_style = {"background-color": 'transparent',
                         'fontSize': '16px', "margin-top": "5px"}
        subdivision_options = []
        subdivision_style = {'display': 'none'}
        filtered_data = filtered_data.loc[(
            filtered_data["Continent"] == continent_dropdown_value)]
        country_center = dict(lat=20, lon=15)

    elif continent_dropdown_value is not None and country_dropdown_value is not None and (subdivision_dropdown_value is None or len(subdivision_dropdown_value) < 1):
        country_options = [{'label': country, 'value': country}
                           for country in country_list]
        country_style = {"background-color": 'transparent',
                         'fontSize': '16px', "margin-top": "5px"}
        subdivision_options = [{'label': subdivision, 'value': subdivision}
                               for subdivision in subdivisions_list]
        subdivision_style = {"background-color": 'transparent',
                             'fontSize': '16px', "margin-top": "5px"}
        filtered_data = filtered_data.loc[(
            filtered_data["Continent"] == continent_dropdown_value) &
            (filtered_data["Country"] == country_dropdown_value)]
        country_center = dict(lat=(filtered_data['Country_Latitude'].unique()[
                              0]), lon=(filtered_data['Country_Longitude'].unique()[0]))

    elif continent_dropdown_value is None and (country_dropdown_value is not None or subdivision_dropdown_value is not None):
        country_dropdown_value = None
        subdivision_dropdown_value = None
        country_options = []
        country_style = {'display': 'none'}
        subdivision_options = []
        subdivision_style = {'display': 'none'}
        filtered_data = dff.loc[str(start_year):str(end_year)]
        country_center = dict(lat=20, lon=15)

    else:
        country_options = [{'label': country, 'value': country}
                           for country in country_list]
        country_style = {"background-color": 'transparent',
                         'fontSize': '16px', "margin-top": "5px"}
        subdivision_options = [{'label': subdivision, 'value': subdivision}
                               for subdivision in subdivisions_list]
        subdivision_style = {"background-color": 'transparent',
                             'fontSize': '16px', "margin-top": "5px"}
        filtered_data = filtered_data.loc[(
            filtered_data["Continent"] == continent_dropdown_value) & (filtered_data["Country"] == country_dropdown_value) &
            (filtered_data["State"] == subdivision_dropdown_value)]
        country_center = dict(lat=(filtered_data['Country_Latitude'].unique()[
                              0]), lon=(filtered_data['Country_Longitude'].unique()[0]))

    sunburst_data = filtered_data.copy()
    sunburst_data['Total Pieces Collected'] = filtered_data[bar_chart_cols].sum(
        axis=1)

    container_1 = ["There are {} values in this range".format(
        len(filtered_data))]

    container_2 = ["There are {} values in this range".format(
        len(subdivisions_list))]

# ======================================================================================================================
# Cards
# ======================================================================================================================

    total_participants = format(sum(sunburst_data['Volunteers']), ',')
    total_organizations = format(sunburst_data['Organization'].nunique(), ',')
    
    if item_dropdown_value is None:
        item_dropdown_value = 'Pieces Collected'
        total_items_colected = format(
            sum(sunburst_data[item_dropdown_value]), ',')
        highlighted_locations = sunburst_data.sort_values(
            by=item_dropdown_value, ascending=False)['UniqueID'].unique()[:10]
    else:
        total_items_colected = format(
            sum(sunburst_data[item_dropdown_value]), ',')
        highlighted_locations = sunburst_data.sort_values(
            by=item_dropdown_value, ascending=False)['UniqueID'].unique()[:10]
# ======================================================================================================================
# Location ScatterMap
# ======================================================================================================================
    country_zoom = 1
    country_area = 0

    if country_dropdown_value is not None and country_dropdown_value in df_3['Country'].astype(str).values:
        df_3['Area (sq. mi.)'] = pd.to_numeric(
            df_3['Area (sq. mi.)'], errors='coerce')
        print(df_3['Country'].dtype)
        country_area = df_3.loc[df_3['Country'] == str(
            country_dropdown_value), 'Area (sq. mi.)'].values[0]

        if country_area < country_size[1]:
            country_zoom = 8
        elif country_size[1] <= country_area < country_size[3]:
            country_zoom = 7
        elif country_size[3] <= country_area < country_size[5]:
            country_zoom = 6
        elif country_size[5] <= country_area < country_size[6]:
            country_zoom = 5
        elif country_size[6] <= country_area < country_size[8]:
            country_zoom = 4
        elif country_size[8] <= country_area < country_size[9]:
            country_zoom = 4
        elif country_size[9] <= country_area < country_size[10]:
            country_zoom = 3
        elif country_area >= country_size[9]:
            country_zoom = 2
    else:
        country_zoom = 1

    sunburst_data['Top 10 Collector'] = sunburst_data['UniqueID'].isin(
        highlighted_locations)
    highlight_color = 'red'
    non_highlight_color = 'lightgreen'

    fig = px.scatter_mapbox(
        sunburst_data[sunburst_data[item_dropdown_value] > 0],
        lat='Latitude',
        lon='Longitude',
        hover_name="Location",
        hover_data=['Date', 'Country', 'Organization',
                    'Volunteers', item_dropdown_value],
        color='Top 10 Collector',
        color_discrete_map={True: highlight_color, False: non_highlight_color},
        zoom=country_zoom,  # Set the initial zoom level
        center=country_center,  # Set the initial center location
        width=700,
        height=550,
        opacity=0.85,
    )
    fig.update_layout(
        mapbox_style="carto-positron",
        uirevision="Don't change",
        paper_bgcolor="#242424",
        autosize=True,
        margin=go.layout.Margin(l=0, r=0, t=0,  b=0),
        showlegend=False,
    )

# ======================================================================================================================
# Sunburst Chart
# ======================================================================================================================

    fig_2 = px.sunburst(sunburst_data,  path=[
                        'Continent', 'Country', 'State', 'Location'], values=item_dropdown_value)

    fig_2.update_traces(insidetextorientation='radial')

    fig_2.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color='white'),   # Set the text color to white
        showlegend=True,
        uniformtext_minsize=10,
        uniformtext_mode='hide',
        legend=dict(
            # Set the legend orientation to horizontal (top)
            orientation='h',
            yanchor='bottom',
            y=-5,  # Adjust the position of the legend
            xanchor='left',
            x=0.1,
            font=dict(size=12)
        ),
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=50,
            pad=0
        )
    )

# ======================================================================================================================
# Cards
# ======================================================================================================================


# ======================================================================================================================
# Function Return
# ======================================================================================================================

    return fig,  fig_2, container_1, container_2, country_options, country_style, country_dropdown_value, subdivision_options, subdivision_style, subdivision_dropdown_value, html.P(f'{total_organizations}'), html.P(f'{format(total_participants)}'), html.P([f'{total_items_colected}', html.Br(), f'{item_dropdown_value}'])


# ======================================================================================================================
# Run Dashboard
# ======================================================================================================================
if __name__ == '__main__':
    app.run_server(debug=True, port=8049)
