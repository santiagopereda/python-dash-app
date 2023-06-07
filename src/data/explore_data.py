from functions.data_cleaning import *

df_location = '../../data/raw/earth_challenge_dataset.csv'

df = pd.read_csv(df_location)

df = split_column_by_hyphen(df, 'ISO_CODE')

null_df = get_null_percentage(df)
print("Data Null Percentage by Column")
print(null_df.sort_values(by='Null Percentage', ascending=False))
print(" ")

df = update_countries(df)

df = fill_null_countries(df)

df = fill_country_code(df)

df = fill_country_subdivision(df)

df = df.drop(index=df[(df['COUNTRY'].isna())].index)
df = df.drop(index=df[df['Location'].isna()].index)
df = df.drop(index=df[df['ISO_SUB'].isna()].index)

drop_list = ['TotalArea_Sq_m', 'Other', 'FieldObsevations', 'BeachAreaLandcover', 'BeachType', 'DebrisDescription',
             'WaterfrontName', 'TotalWidth_m', 'StartTime', 'Longitude2', 'ShorelineName', 'Latitude2', 'X', 'Y',
             'UniqueID', 'SourceID', 'SubCountry_L1_FromSource', 'SubCountry_L2_FromSource', 'CountryName_FromSource'
             'OBJECTID']

null_df = get_null_percentage(df)
print(" ")
print("Data Null Percentage by Column")
print(null_df.sort_values(by='Null Percentage', ascending=False))
print(" ")
