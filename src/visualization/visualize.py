# --------------------------------------------------------------
# Load data
# --------------------------------------------------------------
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

pickle_loc = "../../data/interim/01_data_processed.pkl"
df = pd.read_pickle(pickle_loc)
df.columns
token = "pk.eyJ1Ijoic2FudGlhZ29wZXJlZGEiLCJhIjoiY2xpbm1wZG9qMDAyZTNtbGJsZDJjYWN2NyJ9.i66XD8Qd9IF3tjhRAV5oNg"
# --------------------------------------------------------------
# Plot single columns
# --------------------------------------------------------------
fig = px.scatter_mapbox(df, lat='Latitude1', lon='Longitude1', hover_name="Location",
                        hover_data=['DateStandardized', 'Organization'],
                        color_discrete_sequence=["lightcoral"], zoom=1, height=300, opacity = 0.85)
fig.update_layout(mapbox_style="mapbox://styles/santiagopereda/clinlvecs002d01p73lb45noj", mapbox_accesstoken=token)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()
# --------------------------------------------------------------
# Plot all exercises
# --------------------------------------------------------------


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
