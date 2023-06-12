import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from functions.data_managing import *


# ======================================================================================================================
# Import Pandas Dataframe & Initialize APP
# ======================================================================================================================
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

token = "pk.eyJ1Ijoic2FudGlhZ29wZXJlZGEiLCJhIjoiY2xpbm1wZG9qMDAyZTNtbGJsZDJjYWN2NyJ9.i66XD8Qd9IF3tjhRAV5oNg"
pickle_loc = "../../data/interim/01_data_processed.pkl"
pickle_loc_2 = "../../data/interim/02_data_processed.pkl"
df = pd.read_pickle(pickle_loc)
df_2 = pd.read_pickle(pickle_loc_2)


country_dropdown_options = df_2.index.get_level_values(0).unique()

# ======================================================================================================================
# App layout
# ======================================================================================================================
app.layout = dbc.Container([
    dbc.Row([
        html.Div([
            html.H5("Global Earth Challenge Report",
                style={'text-left': 'center', 'color': 'white'})
        ])
    ]),
    dbc.Row([
        dbc.Col([
            html.Div(id='output_container', children=[]),
            html.Br(),
            html.Div([
                html.Link(
                    rel='stylesheet',
                    href='/assets/styles.css'
                    ),
                dcc.Dropdown(
                    options=[{'label': option, 'value': option} for option in df_2.index.get_level_values(0).unique()],
                    id="country-dropdown",
                    placeholder="Select a Country",
                    multi=True, 
                    maxHeight=200,
                    style={"background-color":'transparent','fontSize': '16px','border': '1px solid gray',},
                    className='my-dropdown'
                    ),
                html.Div(
                    id='pandas-output-container-1',
                    children=[],
                    style={'display': 'none'}
                    )
            ])
        ]),
        dbc.Col([
            dcc.Graph(id='eac_map', figure={}),
            dcc.RangeSlider(
                id='slct_year',
                min=df.index.year.min(),
                max=df.index.year.max(),
                step=1,
                value=[df.index.year.min(), (df.index.year.max()+1)],
                marks=None,
                # marks = {i: f'{i}' for i in range(df.index.year.min(), (df.index.year.max()+1))},
                allowCross=False,
                tooltip={"placement": "bottom", "always_visible": True},
                )
        ]),
        dbc.Col([
            
        ])
    ]),
    dbc.Row([
        dbc.Col(
            [
            dcc.Graph(id='bar_table', figure={})  
            ]
        ),
    ])
    
], fluid=True)

# ======================================================================================================================
# Connect the Plotly graphs with Dash Components
# ======================================================================================================================


@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='eac_map', component_property='figure')],
    [Input(component_id='slct_year', component_property='value'),
     Input(component_id="country-dropdown", component_property='value')]
)
def update_graph(option_slctd, dropdown_value):

    start_year, end_year = option_slctd[0], option_slctd[1]
    dff = df.copy()
    filtered_data = dff[str(start_year):str(end_year)]

    if dropdown_value == None or len(dropdown_value) < 1:
        filtered_data
    else:    
        filtered_data = filtered_data.loc[filtered_data["COUNTRY"].isin(dropdown_value)]
    
    container = ["There are {} values in this range".format(
        len(filtered_data))]

    fig = px.scatter_mapbox(
        filtered_data,
        lat='Latitude1',
        lon='Longitude1',
        hover_name="Location",
        hover_data=['DateStandardized', 'Organization'],
        color_discrete_sequence=["lightgreen"],
        zoom=1,  # Set the initial zoom level
        center=dict(lat=20, lon=15),  # Set the initial center location
        width=800,
        height=300,
        opacity=0.85
    )
    fig.update_layout(
        mapbox_style="mapbox://styles/santiagopereda/clinlvecs002d01p73lb45noj",
        mapbox_accesstoken=token,
        uirevision="Don't change",
        paper_bgcolor="#242424",
        autosize=True,
        margin=go.layout.Margin(l=0, r=0, t=0,  b=0),
        showlegend=False
    )

    return container, fig

@app.callback(
    [Output(component_id='pandas-output-container-1', component_property='children'),
     Output(component_id='bar_table', component_property='figure')],
    [Input(component_id='slct_year', component_property='value'),
     Input(component_id="country-dropdown", component_property='value')]
)
def update_output(option_slctd, dropdown_value):

    filled_list = list(range(min(option_slctd), max(option_slctd)+1))
    
    dff_2 = df_2.copy()
    
    if dropdown_value == None or len(dropdown_value) < 1:
        level_one_slice = slice(None)
    else:
        level_one_slice = dropdown_value
        
    level_two_slice = slice(None)
    
    if option_slctd == None or len(option_slctd) < 1:
        level_three_slice = slice(None)
    else:
        level_three_slice = filled_list
    
    sliced_df = slice_multi_index_dataframe(dff_2, level_one_slice,
                                            level_two_slice, level_three_slice)

    bar_chart_cols = ['SUM_Soft_CigaretteButts', 'SUM_Hard_Lighter',
                    'SUM_Soft_Straw', 'SUM_Hard_PlasticBeverageBottle',
                    'SUM_Hard_OtherPlasticBottle', 'SUM_HardOrSoft_PlasticBottleCap',
                    'SUM_PlasticOrFoamPlatesBowlsCup', 'SUM_PlasticOrFoamFoodContainer',
                    'SUM_HardSoftLollipopStick_EarBu', 'SUM_Soft_Bag',
                    'SUM_Hard_BucketOrCrate', 'SUM_Soft_WrapperOrLabel',
                    'SUM_HardSoft_PersonalCareProduc', 'SUM_Soft_StringRingRibbon',
                    'PCT_PlasticAndFoam', 'Soft_Sheets2', 'PCT_Glass_Rubber_Lumber_Metal',
                    'SUM_FishingLineLureRope', 'Fishing_Net', 'Fishing_BuoysAndFloats',
                    'FishingGlowSticks2', 'FishingOtherPlasticDebris2',
                    'SUM_Soft_OtherPlastic', 'SUM_Foam_OtherPlasticDebris',
                    'SUM_OtherPlasticDebris', 'SUM_OtherHardPlastic']

    filtered_dff2 = dynamic_barchart(sliced_df, bar_chart_cols)
    
    # Create the bar chart using Plotly Express
    fig_2 = px.bar(filtered_dff2, 
                x=filtered_dff2.index,
                # Exclude 'SUM' and 'cumulative_sum' columns
                y=filtered_dff2.columns[:-2],
                width=800, 
                height=400
                )

    # Update the layout of the bar chart
    fig_2.update_layout(barmode='stack', 
                    xaxis={'categoryorder': 'total descending'},
                    paper_bgcolor="rgba(0,0,0,0)",
                    xaxis_tickangle=0,
                    font=dict(color='white'),   # Set the text color to white
                    legend=dict(
                        orientation='v',  # Set the legend orientation to horizontal (top)
                        yanchor='top',
                        y=0.8,  # Adjust the position of the legend
                        xanchor='center',
                        x=1.07
                        ),  
                    xaxis_title=None,
                    yaxis_title="Number of plastic pieces found"
                    )
    
    return dropdown_value, fig_2

# ======================================================================================================================
# Run Dashboard
# ======================================================================================================================
if __name__ == '__main__':
    app.run_server(debug=True, port=8049)