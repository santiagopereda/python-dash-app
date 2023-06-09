from functions.data_cleaning import *
from unidecode import unidecode
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
# Normalize Country Names
# ======================================================================================================================
upd_df = df.copy()

countrytoname_mapping = {
    "Russia": "Russian Federation",
    "Saint Helena, Ascension and Tristan da Cunha": "Saint Helena",
    "Madeira": "Portugal",
    "Brunei": "Brunei Darussalam",
    "US Virgin Islands": "United States"
}

nametocountry_mapping = {
    "Puerto Rico": "Puerto Rico",
    "Guam": "Guam",
    "Aruba": "Aruba",
    "Curacao": "Curacao",
}

upd_df = normalize_countrynames(
    upd_df, "COUNTRY", "COUNTRY", countrytoname_mapping)

upd_df = normalize_countrynames(
    upd_df, "NAME", "COUNTRY", nametocountry_mapping)


# ======================================================================================================================
# Drop Columns with repeated data or more than 90% missing values
# ======================================================================================================================
upd_df = upd_df.drop(index=upd_df[(upd_df['COUNTRY'].isna())].index)
upd_df = upd_df.drop(index=upd_df[upd_df['Location'].isna()].index)
upd_df = upd_df.drop(index=upd_df[upd_df['ISO_SUB'].isna()].index)
drop_list = ['TotalArea_Sq_m', 'Other', 'FieldObsevations', 'BeachAreaLandcover', 'BeachType', 'DebrisDescription',
             'WaterfrontName', 'TotalWidth_m', 'StartTime', 'Longitude2', 'ShorelineName', 'Latitude2', 'X', 'Y',
             'SourceID', 'SubCountry_L1_FromSource', 'SubCountry_L2_FromSource', 'CountryName_FromSource', 'OBJECTID',
             "ISO_SUB", "ISO_CC", "ADMINTYPE", "RecordSequenceID", "DateOriginal", "MonthYear", "Year", "MonthNum",
             "Month", "Day", "DOW", "COUNTRYAFF", "DISPUTED", "NOTES", "AUTONOMOUS"]
upd_df = upd_df.drop(drop_list, axis=1)


# ======================================================================================================================
# Set Date as index
# ======================================================================================================================
upd_df["DateStandardized"] = upd_df["DateStandardized"].dt.date
upd_df = upd_df.set_index(upd_df["DateStandardized"]).sort_index()
upd_df.index = pd.to_datetime(upd_df.index)


upd_df["COUNTRY"].unique()

sorted(upd_df[upd_df["COUNTRY"] == "United States"]["NAME"].unique())


# ======================================================================================================================
# Export dataset
# ======================================================================================================================
upd_df.to_pickle("../../data/interim/01_data_processed.pkl")
