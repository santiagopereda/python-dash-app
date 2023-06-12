# --------------------------------------------------------------
# Load data
# --------------------------------------------------------------
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
from functions.data_managing import *


pickle_loc_1 = "../../data/interim/01_data_processed.pkl"
pickle_loc_2 = "../../data/interim/02_data_processed.pkl"

df_1 = pd.read_pickle(pickle_loc_1)
df_2 = pd.read_pickle(pickle_loc_2)
token = "pk.eyJ1Ijoic2FudGlhZ29wZXJlZGEiLCJhIjoiY2xpbm1wZG9qMDAyZTNtbGJsZDJjYWN2NyJ9.i66XD8Qd9IF3tjhRAV5oNg"


df_1[df_1["COUNTRY"]==["Argentina","Venezuela"]]

df_1.loc[df_1["COUNTRY"].isin(["Argentina","Venezuela"])]

# --------------------------------------------------------------
# Mapbox
# --------------------------------------------------------------
fig_1 = px.scatter_mapbox(
    df_1,
    lat='Latitude1',
    lon='Longitude1',
    hover_name="Location",
    hover_data=['DateStandardized', 'Organization'],
    color_discrete_sequence=["lightgreen"],
    zoom=1,  # Set the initial zoom level
    center=dict(lat=15, lon=15),  # Set the initial center location
    width=800,
    height=400,
    opacity=0.85
)

fig_1.update_layout(
    mapbox_style="mapbox://styles/santiagopereda/clinlvecs002d01p73lb45noj",
    mapbox_accesstoken=token,
    uirevision="Don't change",
    paper_bgcolor="#242424",
    autosize=True,
    margin=go.layout.Margin(l=0, r=0, t=0,  b=0),
    showlegend=False
)
fig_1.show()
# --------------------------------------------------------------
# Pie Charts
# --------------------------------------------------------------

level_one_slice = slice(None)
level_two_slice = slice(None)
level_three_slice = slice(None)

sliced_df = slice_multi_index_dataframe(df_2, level_one_slice,
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

filtered_df = dynamic_barchart(sliced_df, bar_chart_cols)
# --------------------------------------------------------------
# Adjust plot settings
# --------------------------------------------------------------


# --------------------------------------------------------------
# Compare medium vs. heavy sets
# --------------------------------------------------------------


# --------------------------------------------------------------
# Compare participants
# --------------------------------------------------------------


# --------------------------------------------------------------
# Plot multiple axis
# --------------------------------------------------------------


# --------------------------------------------------------------
# Create a loop to plot all combinations per sensor
# --------------------------------------------------------------


# --------------------------------------------------------------
# Combine plots in one figure
# --------------------------------------------------------------


# --------------------------------------------------------------
# Loop over all combinations and export for both sensors
# --------------------------------------------------------------
