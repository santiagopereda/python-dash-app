# --------------------------------------------------------------
# Load data
# --------------------------------------------------------------
import pandas as pd
import plotly.express as px

pickle_loc = "../../data/interim/01_data_processed.pkl"
df = pd.read_pickle(pickle_loc)
df.columns
token = "pk.eyJ1Ijoic2FudGlhZ29wZXJlZGEiLCJhIjoiY2xpbm1wZG9qMDAyZTNtbGJsZDJjYWN2NyJ9.i66XD8Qd9IF3tjhRAV5oNg"
# --------------------------------------------------------------
# Plot single columns
# --------------------------------------------------------------
fig = px.scatter_mapbox(df, lat='Latitude1', lon='Longitude1', hover_name="Location",
                        hover_data=['DateStandardized', 'Organization', 'EventType'],
                        color_discrete_sequence=["blue"], zoom=3, height=300)
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
