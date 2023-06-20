# --------------------------------------------------------------
# Load data
# --------------------------------------------------------------
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from functions.data_managing import *


pickle_loc = "../../data/interim/01_data_processed.pkl"

df = pd.read_pickle(pickle_loc)


df_2_loc = '../../data/raw/countries of the world.csv'
df_2 = pd.read_csv(df_2_loc)
df_2.columns
df_2.Country.unique()

df_2.describe()

df_3_location = '../../data/raw/country_coordinates.csv'
df_3 = pd.read_csv(df_3_location)
# --------------------------------------------------------------
# Data Group Parameters
# --------------------------------------------------------------
level_one = "CONTINENT"
level_two = "COUNTRY"
level_three = 'NAME'
date_level = df.index.year
agg_params = {'UniqueID': 'count', 'Location': 'nunique', 'Organization': 'nunique',
              'TotalVolunteers': 'sum', 'Totalltems_EventRecord': 'sum',
              'SUM_Soft_CigaretteButts': 'sum', 'SUM_Hard_Lighter': 'sum', 'SUM_Soft_Straw': 'sum',
              'SUM_Hard_PlasticBeverageBottle': 'sum', 'SUM_Hard_OtherPlasticBottle': 'sum',
              'SUM_HardOrSoft_PlasticBottleCap': 'sum', 'SUM_PlasticOrFoamPlatesBowlsCup': 'sum',
              'SUM_PlasticOrFoamFoodContainer': 'sum', 'SUM_HardSoftLollipopStick_EarBu': 'sum',
              'SUM_Soft_Bag': 'sum', 'SUM_Hard_BucketOrCrate': 'sum',
              'SUM_Soft_WrapperOrLabel': 'sum', 'SUM_HardSoft_PersonalCareProduc': 'sum',
              'SUM_Soft_StringRingRibbon': 'sum', 'PCT_PlasticAndFoam': 'sum',
              'Soft_Sheets2': 'sum', 'PCT_Glass_Rubber_Lumber_Metal': 'sum',
              'SUM_FishingLineLureRope': 'sum', 'Fishing_Net': 'sum',
              'Fishing_BuoysAndFloats': 'sum', 'FishingGlowSticks2': 'sum',
              'FishingOtherPlasticDebris2': 'sum', 'FishingGlowSticks2': 'sum',
              'SUM_Soft_OtherPlastic': 'sum', 'SUM_Foam_OtherPlasticDebris': 'sum',
              'SUM_OtherPlasticDebris': 'sum', 'SUM_OtherHardPlastic': 'sum'
              }
grp_df = df.groupby([level_one, level_two, level_three, date_level]).agg(agg_params)


# --------------------------------------------------------------
# Mapbox
# --------------------------------------------------------------
fig_1 = px.scatter_mapbox(
    df,
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
    mapbox_style="carto-positron",
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
year_slice = slice(None)

sliced_df = slice_multi_index_dataframe(grp_df, level_one_slice,
                            level_two_slice, level_three_slice, year_slice)

sliced_df.index.get_level_values(0).unique()

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

filtered_df = yearly_filtered_data(sliced_df, bar_chart_cols, True)

# --------------------------------------------------------------
# Adjust plot settings
# --------------------------------------------------------------

yearly_filtered_data(sliced_df, ['Organization','TotalVolunteers','UniqueID'], False)

# --------------------------------------------------------------
# Compare medium vs. heavy sets
# --------------------------------------------------------------
level_one_slice = slice(None)
level_two_slice = slice(None)
level_three_slice= slice(None)
year_slice = slice(None)

filtered_location = location_filter(df, level_one_slice, level_two_slice, level_three_slice)


fig = px.pie(filtered_location, values='SUM', names=filtered_location.index)

fig.update_traces(textposition='inside',insidetextorientation='radial')

fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color='white'),   # Set the text color to white
                showlegend=True,
                uniformtext_minsize=10, 
                uniformtext_mode='hide',
                legend=dict(
                    orientation='h',  # Set the legend orientation to horizontal (top)
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

fig.show()

dff = df.copy()
dff['Total Pieces Collected'] = df[bar_chart_cols].sum(axis=1)

fig_2 = px.sunburst(dff,  path=['Cotinent','Country','State'], values='Total Pieces Collected')

fig_2.update_traces(insidetextorientation='radial')

fig_2.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color='white'),   # Set the text color to white
                showlegend=True,
                uniformtext_minsize=10, 
                uniformtext_mode='hide',
                legend=dict(
                    orientation='h',  # Set the legend orientation to horizontal (top)
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
fig.show()


df.info()