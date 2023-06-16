import pandas as pd

# --------------------------------------------------------------
# Data Slice Parameters
# --------------------------------------------------------------


def slice_multi_index_dataframe(df: pd.DataFrame, level_one_slice=slice(None), level_two_slice=slice(None), level_three_slice=slice(None)) -> pd.DataFrame:
    """
    Slices a DataFrame with a multi-level index based on the provided level slices.
    Parameters:
        df (pd.DataFrame): The input DataFrame with a multi-level index.
        level_one_slice (slice): Slice for the first level of the multi-level index. Default is slice(None).
        level_two_slice (slice): Slice for the second level of the multi-level index. Default is slice(None).
        level_three_slice (slice): Slice for the third level of the multi-level index. Default is slice(None).
    Returns:
        pd.DataFrame: The sliced DataFrame based on the provided level slices.
    """
    # Create the pd.IndexSlice object
    idx = pd.IndexSlice

    # Use .loc accessor and pd.IndexSlice to slice the DataFrame
    sliced_df = df.loc[idx[level_one_slice,
                           level_two_slice, level_three_slice], :]

    return sliced_df


# --------------------------------------------------------------
# Get Country and Subdivision coordinates
# --------------------------------------------------------------
col_name_replace = {'Longitude1': 'Longitude',
                    'Latitude1': 'Latitude',
                    'TotalLength_m': 'Total Length',
                    'EventType': 'Event Type',
                    'TotalVolunteers': 'Volunteers',
                    'DateStandardized': 'Date',
                    'Totalltems_EventRecord': 'Total ltems',
                    'TotalClassifiedItems_EC2020': 'Total Classified Items',
                    'PCT_PlasticAndFoam': 'PCT Plastic And Foam',
                    'PCT_Glass_Rubber_Lumber_Metal': 'PCT Glass Rubber Lumber Metal',
                    'SUM_Hard_PlasticBeverageBottle': 'Plastic Beverage Bottles',
                    'SUM_Hard_OtherPlasticBottle': 'Other Plastic Bottles',
                    'SUM_HardOrSoft_PlasticBottleCap': 'Plastic Bottle Caps',
                    'SUM_PlasticOrFoamFoodContainer': 'Food Containers',
                    'SUM_Hard_BucketOrCrate': 'Buckets Or Crates',
                    'SUM_Hard_Lighter': 'Lighters',
                    'SUM_OtherHardPlastic': 'Other Hard Plastics',
                    'SUM_PlasticOrFoamPlatesBowlsCup': 'Plates Bowls Cups',
                    'SUM_HardSoft_PersonalCareProduc': 'Personal Care Products',
                    'SUM_HardSoftLollipopStick_EarBu': 'Lollipop Stick',
                    'SUM_Soft_Bag': 'Bag',
                    'SUM_Soft_WrapperOrLabel': 'Wrapper Or Label',
                    'SUM_Soft_Straw': 'Straws',
                    'SUM_Soft_OtherPlastic': 'Other Soft Plastics',
                    'SUM_Soft_CigaretteButts': 'Cigarette Butts',
                    'SUM_Soft_StringRingRibbon': 'String Ring',
                    'Fishing_Net': 'Fishing Nets',
                    'SUM_FishingLineLureRope': 'Fishing Lines',
                    'Fishing_BuoysAndFloats': 'Fishing Buoys',
                    'SUM_Foam_OtherPlasticDebris': 'Foam Plastic Debris',
                    'SUM_OtherPlasticDebris': 'Other Plastic Debris',
                    'NAME': 'State',
                    'COUNTRY': 'Country',
                    'ISO_CODE': 'Country Code',
                    'CONTINENT': 'Continent',
                    'LAND_TYPE': 'Land Type',
                    'LAND_RANK': 'Land Rank',
                    'Shape__Area': 'Shape Area',
                    'Shape__Length': 'Shape Length',
                    'Soft_Sheets2': 'Soft Sheets',
                    'PlasticStraps2': 'Plastic Straps',
                    'FishingGlowSticks2': 'Fishing Glow Sticks',
                    'FishingOtherPlasticDebris2': 'Other Fishing Plastic Debris'}
