from functions.data_cleaning import *
import pickle

# ======================================================================================================================
# Specify CSV Location and create a Pandas Dataframe 
# ======================================================================================================================
df_location = '../../data/raw/earth_challenge_dataset.csv'
df = pd.read_csv(df_location, parse_dates=['DateStandardized'])

# ======================================================================================================================
# Splits a specified column, adds a hyphen, and joins it back together.
# ======================================================================================================================
df = split_column_by_hyphen(df, 'ISO_CODE')

# ======================================================================================================================
# Update missing values in the 'COUNTRY' columns based on a country list.
# ======================================================================================================================
df = update_countries(df)

# ======================================================================================================================
# Fills missing values in the 'Location' column by retrieving location information
# using latitude and longitude values for each country.
# ======================================================================================================================
df = fill_null_countries(df)

# ======================================================================================================================
# Fills missing values in the 'ISO_SUB', 'NAME', and 'LAND_TYPE' columns based on the 'Location' column using pycountry.
# ======================================================================================================================
df = fill_country_subdivision(df)

# ======================================================================================================================
# Drop Columns with repeated data or more than 90% missing values
# ======================================================================================================================
df = df.drop(index=df[(df['COUNTRY'].isna())].index)
df = df.drop(index=df[df['Location'].isna()].index)
df = df.drop(index=df[df['ISO_SUB'].isna()].index)
drop_list = ['TotalArea_Sq_m', 'Other', 'FieldObsevations', 'BeachAreaLandcover', 'BeachType', 'DebrisDescription',
             'WaterfrontName', 'TotalWidth_m', 'StartTime', 'Longitude2', 'ShorelineName', 'Latitude2', 'X', 'Y',
             'UniqueID', 'SourceID', 'SubCountry_L1_FromSource', 'SubCountry_L2_FromSource', 'CountryName_FromSource',
             'OBJECTID', "ISO_SUB", "ISO_CC", "ADMINTYPE", "RecordSequenceID", "DateOriginal", "MonthYear", "Year",
             "MonthNum", "Month", "Day", "DOW", "COUNTRYAFF", "DISPUTED", "NOTES", "AUTONOMOUS"]
df = df.drop(drop_list, axis=1)

# ======================================================================================================================
# Set Date as index
# ======================================================================================================================
df["DateStandardized"] = df["DateStandardized"].dt.date
df = df.set_index(df["DateStandardized"]).sort_index()
df.index.name = None

# ======================================================================================================================
# Export dataset
# ======================================================================================================================
df.to_pickle("../../data/interim/01_data_processed.pkl")