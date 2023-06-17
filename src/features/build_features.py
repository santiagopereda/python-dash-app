from functions.data_managing import *
import pandas as pd
pd.set_option('display.max_columns', 2100)
pd.set_option('display.max_rows', 2100)

# --------------------------------------------------------------
# Load data
# --------------------------------------------------------------
pickle_loc = "../../data/interim/01_data_processed.pkl"
df = pd.read_pickle(pickle_loc)
df.index = pd.to_datetime(df.index)
df.index.name = "Year"

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
# Data Slice Parameters
# --------------------------------------------------------------
level_one_slice = slice(None)
level_two_slice = slice(None)
level_three_slice = slice(None)

sliced_df = slice_multi_index_dataframe(grp_df, level_one_slice,
                            level_two_slice, level_three_slice)




sliced_df.sort_values(by=('TotalVolunteers'), ascending=False).head(10)

sorted(df[df["COUNTRY"]=="United States"]["NAME"].unique())
# --------------------------------------------------------------
# Export Data
# --------------------------------------------------------------
grp_df.to_pickle("../../data/interim/02_data_processed.pkl")