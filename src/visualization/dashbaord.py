import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc


# ======================================================================================================================
# Import Pandas Dataframe & Initialize APP
# ======================================================================================================================
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

token = "pk.eyJ1Ijoic2FudGlhZ29wZXJlZGEiLCJhIjoiY2xpbm1wZG9qMDAyZTNtbGJsZDJjYWN2NyJ9.i66XD8Qd9IF3tjhRAV5oNg"
pickle_loc = "../../data/interim/01_data_processed.pkl"
df = pd.read_pickle(pickle_loc)

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
        dbc.Col([dcc.RangeSlider(
                id='slct_year',
                min=df.index.year.min(),
                max=df.index.year.max(),
                step=1,
                value=[df.index.year.min(), (df.index.year.max()+1)],
                marks=None,
                # marks = {i: f'{i}' for i in range(df.index.year.min(), (df.index.year.max()+1))},
                allowCross=False,
                tooltip={"placement": "bottom", "always_visible": True},
                className='dark-mode'),

            html.Div(id='output_container', children=[]),

            html.Br(),
        ]),
        dbc.Col([
            dcc.Graph(id='eac_map', figure={})
        ]),
        dbc.Col([

        ])
    ]),
    dbc.Row([
        dbc.Col(html.H1("Plastic Waste Collected for Earth Day Challenge",
                        style={'text-align': 'center', 'color': 'white'})),
    ])
], fluid=True,)

# ======================================================================================================================
# Connect the Plotly graphs with Dash Components
# ======================================================================================================================


@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='eac_map', component_property='figure')],
    [Input(component_id='slct_year', component_property='value')]
)
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    start_year, end_year = option_slctd[0], option_slctd[1]
    dff = df.copy()
    filtered_data = dff[str(start_year):str(end_year)]

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
        height=400,
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


# ======================================================================================================================
# Run Dashboard
# ======================================================================================================================
if __name__ == '__main__':
    app.run_server(debug=True, port=8049)
