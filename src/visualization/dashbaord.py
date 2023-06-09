import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output


# ======================================================================================================================
# Import Pandas Dataframe & Initialize APP
# ======================================================================================================================
app = Dash(__name__)

token = "pk.eyJ1Ijoic2FudGlhZ29wZXJlZGEiLCJhIjoiY2xpbm1wZG9qMDAyZTNtbGJsZDJjYWN2NyJ9.i66XD8Qd9IF3tjhRAV5oNg"
pickle_loc = "../../data/interim/01_data_processed.pkl"
df = pd.read_pickle(pickle_loc)

# ======================================================================================================================
# App layout
# ======================================================================================================================
app.layout = html.Div([
    html.Div([
        html.Div([
            html.Div([
                html.H1("Plastic Waste Collected for Earth Day Challenge",
                        style={'text-align': 'center', 'color': 'white'}),
            ]),
        ], className="six column", id="title")
    ], id="header", className="row flex-display", style={"margin-bottom": "25px"}),

    html.Div([
        html.Div([
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
                className='dark-mode'
            ),
        ], className="create_container 12 columns"),
    ], className="row flex-display"),

    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='eac_map', figure={})
],
    className='dark-mode-container'
)

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

    fig = px.scatter_mapbox(filtered_data, lat='Latitude1', lon='Longitude1', hover_name="Location",
                            hover_data=['DateStandardized', 'Organization'],
                            color_discrete_sequence=["lightgreen"], zoom=1, height=300, opacity=0.85)
    fig.update_layout(
        mapbox_style="mapbox://styles/santiagopereda/clinlvecs002d01p73lb45noj", mapbox_accesstoken=token)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return container, fig


# ======================================================================================================================
# Run Dashboard
# ======================================================================================================================
if __name__ == '__main__':
    app.run_server(debug=True, port=8049, use_reloader=False)
