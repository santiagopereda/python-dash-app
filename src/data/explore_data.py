from functions.data_cleaning import *
import pickle
pd.set_option('display.max_columns', 2100)
pd.set_option('display.max_rows', 2100)

# ======================================================================================================================
# Specify CSV Location and create a Pandas Dataframe
# ======================================================================================================================
df_location = '../../data/raw/earth_challenge_dataset.csv'
df = pd.read_csv(df_location, parse_dates=['DateStandardized'])
df.fillna(value=fill_values, inplace=True)

df_2_location = '../../data/raw/country_coordinates.csv'
df_2 = pd.read_csv(df_2_location)
country_coordinates = create_country_dict(df_2)

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
# Fill missing values in 'Organization'
# ======================================================================================================================
df = fill_null_organizations(df)

# ======================================================================================================================
# Remove repetitive information in Location Column
# ======================================================================================================================
df = extract_location(df)

# ======================================================================================================================
# Normalize Country Names
# ======================================================================================================================
countrytoname_mapping = {
    "Russian Federation": "Russia",
    "Saint Helena, Ascension and Tristan da Cunha": "Saint Helena",
    "Madeira": "Portugal",
    "Brunei Darussalam": "Brunei",
    "US Virgin Islands": "United States",
    "Saba": "Netherlands",
    "Canarias": "Spain",
    "Azores": "Portugal",
    "The Bahamas": "Bahamas",
    "Cabo Verde": "Cape Verde"
}

nametocountry_mapping = {
    "Puerto Rico": "Puerto Rico",
    "Guam": "Guam",
    "Aruba": "Aruba",
    "Curacao": "Curacao",
}

nametoname_mapping = {
    "Dependencias Federales": "Distrito Federal",
}

df = normalize_countrynames(
    df, "COUNTRY", "COUNTRY", countrytoname_mapping)

df = normalize_countrynames(
    df, "NAME", "COUNTRY", nametocountry_mapping)

# ======================================================================================================================
# Add General Country Coordinates
# ======================================================================================================================
df = add_coordinates_to_dataframe(df, country_coordinates)

# ======================================================================================================================
# Drop Columns with repeated data or more than 90% missing values
# ======================================================================================================================
df = df.drop(index=df[(df['COUNTRY'].isna())].index)
df = df.drop(index=df[df['Location'].isna()].index)
df = df.drop(index=df[df['ISO_SUB'].isna()].index)
drop_list = ['TotalArea_Sq_m', 'Other', 'FieldObsevations', 'BeachAreaLandcover', 'BeachType', 'DebrisDescription',
             'WaterfrontName', 'TotalWidth_m', 'StartTime', 'Longitude2', 'ShorelineName', 'Latitude2', 'X', 'Y',
             'SourceID', 'SubCountry_L1_FromSource', 'SubCountry_L2_FromSource', 'CountryName_FromSource', 'OBJECTID',
             "ISO_SUB", "ISO_CC", "ADMINTYPE", "RecordSequenceID", "DateOriginal", "MonthYear", "Year", "MonthNum",
             "Day", "DOW", "COUNTRYAFF", "DISPUTED", "NOTES", "AUTONOMOUS", 'Count_']
df = df.drop(drop_list, axis=1)


# ======================================================================================================================
# Set Date as index
# ======================================================================================================================
df["DateStandardized"] = df["DateStandardized"].dt.date
df = df.set_index(df["DateStandardized"]).sort_index()
df.index = pd.to_datetime(df.index)
df = df.astype(col_data_type)

# ======================================================================================================================
# Export dataset
# ======================================================================================================================
df.to_pickle("../../data/interim/01_data_processed.pkl")
