import re
from typing import Any
import pycountry
import pandas as pd
from unidecode import unidecode
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut


def split_column_by_hyphen(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Splits a specified column, adds a hyphen, and joins it back together.
    Parameters:
        df (pd.DataFrame): The input DataFrame.
        column (str): The name of the column to split and join.
    Returns:
        pd.DataFrame: The DataFrame with the updated column.
    """
    # Convert the specified column to string type, split each value, add a hyphen, and join them back together
    df[column] = df[column].astype(str).apply(lambda x: x[:2] + '-' + x[2:])
    return df


def update_countries(df: pd.DataFrame) -> pd.DataFrame:
    """
    Update missing values in the 'COUNTRY' and 'COUNTRYAFF' columns based on a country list.
    Parameters:
        df (pd.DataFrame): The input DataFrame.
        column_list (list): A list of column names to iterate over.
    Returns:
        pd.DataFrame: The DataFrame with updated 'COUNTRY' columns.
    """
    column_list = ['Location', 'CountryName_FromSource']

    country_list = set()

    # Collect unique country values from specified columns
    for column in column_list:
        country_list |= set(df[df['COUNTRY'].isnull()][column].unique())

    # Iterate over country values
    for country in country_list:
        # Iterate over specified columns
        for column in column_list:
            # Get subset of rows where 'COUNTRY' is null and 'column' matches the country value
            subset = df[(df['COUNTRY'].isnull()) & (df[column] == country)]

            # Iterate over subset rows
            for index, row in subset.iterrows():
                # Check for matching country name, alpha-3 code, or alpha-2 code
                for country_name in pycountry.countries:
                    country_lower = country.strip().lower()

                    if country_name.name.lower() in country_lower:
                        df.at[index, 'COUNTRY'] = country_name.name
                        break
                    if country_name.alpha_3 in country_lower:
                        df.at[index, 'COUNTRY'] = country_name.name
                        break
                    if country_name.alpha_2 in country_lower:
                        df.at[index, 'COUNTRY'] = country_name.name
                        break
    return df


def update_location(df: pd.DataFrame, index: int) -> None:
    """
    Updates the location information for a single row based on latitude and longitude values.
    Parameters:
        df (pd.DataFrame): The DataFrame containing the row to update.
        index (int): The index of the row to update.
    Returns:
        None
    """
    geolocator = Nominatim(user_agent="http")

    latitude = str(df.at[index, 'Latitude1'])
    longitude = str(df.at[index, 'Longitude1'])

    try:
        # Retrieve location information using geolocator
        location: Any = geolocator.reverse(latitude + ',' + longitude, language='en') # type: ignore

        # Update the DataFrame if location information is available
        if location is not None and location.raw is not None:
            raw_data = location.raw.get('address', {})

            if 'display_name' in location.raw:
                df.at[index, 'Location'] = location.raw['display_name']

            if 'city' in raw_data:
                df.at[index, 'NAME'] = raw_data['state']

            if 'country' in raw_data:
                df.at[index, 'COUNTRY'] = raw_data['country']
    except (GeocoderTimedOut, KeyError, ValueError):
        # Handle specific geocoding errors
        pass


def fill_null_countries(df: pd.DataFrame) -> pd.DataFrame:
    """
    Fills missing values in the 'Location' column by retrieving location information
    using latitude and longitude values for each country.
    Parameters:
        df (pd.DataFrame): The input DataFrame.
    Returns:
        pd.DataFrame: The DataFrame with the updated 'Location', 'NAME', 'COUNTRY',
        'COUNTRYAFF', and 'ISO_CC' columns.
    """

    def echo(string, padding=80):
        padding = " " * (padding - len(string)) if padding else ""
        print(string + padding, end='\r', flush=True)

    # Get a list of countries with null values in the 'Location' column
    country_list = df[df['Location'].isnull()]['COUNTRY'].unique()
    country_len = len(df[df['Location'].isnull()]['COUNTRY'])

    # Get a subset of the DataFrame for rows with null values in both 'Location' and 'COUNTRY' columns
    null_df = df[df['Location'].isnull() & df['COUNTRY'].isnull()]
    null_len = len(df[df['Location'].isnull() & df['COUNTRY'].isnull()])

    # Get a list of countries with null values in the 'Location' column
    null_country_list = df[df['COUNTRY'].isnull(
    )]['CountryName_FromSource'].unique()
    location_len = len(df[df['COUNTRY'].isnull()]['CountryName_FromSource'])

    job_len = country_len + null_len + location_len

    # Counter for tracking progress
    i = 0

    # Iterate over each country
    for country in country_list:
        # Get a subset of the DataFrame for the current country
        country_df = df[df['Location'].isnull() & (df['COUNTRY'] == country)]

        # Iterate over each row in the subset
        for index, row in country_df.iterrows():
            update_location(df, index)

            i += 1
            progress = (f"{i}/{job_len} {row['COUNTRY']}")
            echo(progress)

    # Iterate over each row in the subset
    for index, row in null_df.iterrows():
        update_location(df, index) # type: ignore

        i += 1
        progress = (f"{i}/{job_len} {row['Location']}")
        echo(progress)

    # Iterate over each country
    for country in null_country_list:
        # Get a subset of the DataFrame for rows with null values in both 'Location' and 'COUNTRY' columns
        null_country_df = df[(df['COUNTRY'].isnull()) & (
            df['CountryName_FromSource'] == country)]

        # Iterate over each row in the subset
        for index, row in null_country_df.iterrows():
            update_location(df, index)

            i += 1
            progress = (f"{i}/{job_len} {row['CountryName_FromSource']}")
            echo(progress)

    return df


def fill_country_subdivision(df: pd.DataFrame) -> pd.DataFrame:
    """
    Fills missing values in the 'NAME', and 'LAND_TYPE' columns based on the 'Location' column using pycountry.
    Parameters:
        df (pd.DataFrame): The input DataFrame.
    Returns:
        pd.DataFrame: The DataFrame with updated 'NAME', and 'LAND_TYPE' columns.
    """
    # Create a mapping of subdivision names to subdivision codes
    subdivision_mapping = {
        subdivision.name: subdivision.code
        for subdivision in pycountry.subdivisions
    }

    # Iterate over rows with missing values in 'NAME' column
    for index, row in df[df['NAME'].isnull()].iterrows():
        location = str(row['Location'])

        matching_subdivision = None
        subdivision_code = None

        # Look for exact matches of subdivision names in the 'Location' column
        for subdivision_name, subdivision_code in subdivision_mapping.items():
            if unidecode(subdivision_name.lower()) in unidecode(location.lower()):
                matching_subdivision = subdivision_name
                break

        if matching_subdivision:
            # Update the corresponding columns with the subdivision information
            df.at[index, 'NAME'] = pycountry.subdivisions.get(
                code=subdivision_code).name  # type: ignore
            df.at[index, 'LAND_TYPE'] = pycountry.subdivisions.get(
                code=subdivision_code).type  # type: ignore
        else:
            # Try to match subdivision using regular expressions on the 'Location' column
            for subdivision_name, subdivision_code in subdivision_mapping.items():
                if '-' in subdivision_code:
                    # Extract the second part of the subdivision code after the hyphen
                    escaped_subdivision_code = re.escape(
                        subdivision_code.split('-')[1])
                else:
                    escaped_subdivision_code = re.escape(subdivision_code)

                if re.search(r'\b' + escaped_subdivision_code + r'\b', location):
                    matching_subdivision = subdivision_name

                    # Update the corresponding columns with the subdivision information
                    df.at[index, 'NAME'] = pycountry.subdivisions.get(
                        code=subdivision_code).name  # type: ignore
                    df.at[index, 'LAND_TYPE'] = pycountry.subdivisions.get(
                        code=subdivision_code).type  # type: ignore
                    break
    return df


from unidecode import unidecode

def normalize_countrynames(df: pd.DataFrame, check_column: str, target_column: str, mapping_values: dict) -> pd.DataFrame:
    """
    Normalize country names in a DataFrame column based on a mapping dictionary.

    Parameters:
        df: The input DataFrame.
        check_column: The name of the column to check for country names.
        target_column: The name of the column to update with normalized country names.
        mapping_values: A dictionary mapping old country names to new country names.

    Returns:
        The DataFrame with normalized country names in the specified column.
    """

    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        # Get the value in the check column for the current row
        check_loc = str(row[check_column])

        # Initialize variable to track matching subdivision
        matching_subdivision = None

        # Iterate over the mapping values
        for oldname_map, newname_map in mapping_values.items():
            # Check if the old country name is found in the check column value
            if unidecode(oldname_map.lower()) in unidecode(check_loc.lower()):
                matching_subdivision = newname_map
                break

        # Update the target column value if a matching subdivision is found
        if matching_subdivision:
            df.at[index, target_column] = unidecode(matching_subdivision)

    return df



def fill_null_organizations(df: pd.DataFrame) -> pd.DataFrame:
    """
    Fills null, None, and non-null, non-NoneType organization values in a DataFrame with corresponding mapped values from the same DataFrame.
    Sets organization to "Not Listed" if there is no match for a LocationFreqID.

    Args:
        df (pd.DataFrame): The input DataFrame containing 'LocationFreqID' and 'Organization' columns.

    Returns:
        pd.DataFrame: The DataFrame with null, None, and non-null, non-NoneType organization values filled using the mapped values.

    """
    org_dict = {}

    for index, row in df.iterrows():
        if pd.isna(row['Organization']) or row['Organization'] is None or row['Organization'] == 'nan':
            location_id = row['LocationFreqID']

            if location_id in org_dict:
                df.at[index, 'Organization'] = org_dict[location_id]
            else:
                non_null_org = df.loc[(
                    df["LocationFreqID"] == location_id) & df["Organization"].notna(), "Organization"]
                if isinstance(non_null_org, pd.Series) and not non_null_org.empty:
                    org_value = non_null_org.iloc[0]
                    org_dict[location_id] = org_value
                else:
                    # Set to "Not Listed" when there is no match
                    org_value = "No Organization Data Provided"
                    org_dict[location_id] = org_value

                df.at[index, 'Organization'] = org_value
        else:
            continue

    return df


def extract_location(df: pd.DataFrame) -> pd.DataFrame:
    """
    Extracts the first part of the 'Location' column by splitting on comma and updates the DataFrame.

    Args:
        df (pd.DataFrame): The input DataFrame containing the 'Location' column.

    Returns:
        pd.DataFrame: The DataFrame with the 'Location' column updated to contain only the first part of the location.

    """
    for index, row in df.iterrows():
        location = str(row['Location']).split(", ")[0]
        df.at[index, 'Location'] = location

    return df


def add_coordinates_to_dataframe(df: pd.DataFrame, coordinates: dict) -> pd.DataFrame:
    """
    Add latitude and longitude coordinates to a dataframe based on a given dictionary.

    Args:
        df (pd.DataFrame): The dataframe to update.
        coordinates (dict): A dictionary containing country coordinates.

    Returns:
        pd.DataFrame: The updated dataframe with latitude and longitude columns.
    """
    # Create new columns for latitude and longitude in the dataframe
    df['COUNTRY_Latitude'] = None
    df['COUNTRY_Longitude'] = None

    # Iterate through the dataframe and update latitude and longitude columns
    for index, row in df.iterrows():
        country = row['COUNTRY']
        if country in coordinates:
            df.at[index, 'COUNTRY_Latitude'] = coordinates[country][0]['latitude']
            df.at[index, 'COUNTRY_Longitude'] = coordinates[country][0]['longitude']

    return df


def create_country_dict(df: pd.DataFrame) -> dict:
    """
    Create a dictionary of countries and their coordinates based on a given dataframe.

    Args:
        df (pd.DataFrame): The dataframe containing country data.

    Returns:
        dict: A dictionary mapping country names to lists of coordinate dictionaries.
    """
    country_dict = {}

    for _, row in df.iterrows():
        country = row['name']
        latitude = row['latitude']
        longitude = row['longitude']

        if country not in country_dict:
            country_dict[country] = []

        country_dict[country].append({
            'latitude': float(latitude),
            'longitude': float(longitude)
        })

    return country_dict


fill_values = {'TotalVolunteers': 0.0,
               'Totalltems_EventRecord': 0,
               'TotalClassifiedItems_EC2020': 0,
               'PCT_PlasticAndFoam': 0.0,
               'PCT_Glass_Rubber_Lumber_Metal': 0.0,
               'SUM_Hard_PlasticBeverageBottle': 0,
               'SUM_Hard_OtherPlasticBottle': 0,
               'SUM_HardOrSoft_PlasticBottleCap': 0,
               'SUM_PlasticOrFoamFoodContainer': 0.0,
               'SUM_Hard_BucketOrCrate': 0,
               'SUM_Hard_Lighter': 0.0,
               'SUM_OtherHardPlastic': 0,
               'SUM_PlasticOrFoamPlatesBowlsCup': 0,
               'SUM_HardSoft_PersonalCareProduc': 0,
               'SUM_HardSoftLollipopStick_EarBu': 0,
               'SUM_Soft_Bag': 0,
               'SUM_Soft_WrapperOrLabel': 0,
               'SUM_Soft_Straw': 0.0,
               'SUM_Soft_OtherPlastic': 0,
               'SUM_Soft_CigaretteButts': 0.0,
               'SUM_Soft_StringRingRibbon': 0,
               'Fishing_Net': 0,
               'SUM_FishingLineLureRope': 0,
               'Fishing_BuoysAndFloats': 0,
               'SUM_Foam_OtherPlasticDebris': 0,
               'SUM_OtherPlasticDebris': 0.0,
               'LAND_RANK': 0.0,
               'Shape__Area': 0.0,
               'Shape__Length': 0.0,
               'Soft_Sheets2': 0,
               'PlasticStraps2': 0,
               'FishingGlowSticks2': 0,
               'FishingOtherPlasticDebris2': 0}

col_data_type = {'UniqueID': str,
                 'LocationFreqID': str,
                 'Location': str,
                 'Dataset': str,
                 'TotalLength_m': str,
                 'EventType': str,
                 'TotalVolunteers': int,
                 'Month': str,
                 'Totalltems_EventRecord': int,
                 'TotalClassifiedItems_EC2020': int,
                 'PCT_PlasticAndFoam': int,
                 'PCT_Glass_Rubber_Lumber_Metal': int,
                 'SUM_Hard_PlasticBeverageBottle': int,
                 'SUM_Hard_OtherPlasticBottle': int,
                 'SUM_HardOrSoft_PlasticBottleCap': int,
                 'SUM_PlasticOrFoamFoodContainer': int,
                 'SUM_Hard_BucketOrCrate': int,
                 'SUM_Hard_Lighter': int,
                 'SUM_OtherHardPlastic': int,
                 'SUM_PlasticOrFoamPlatesBowlsCup': int,
                 'SUM_HardSoft_PersonalCareProduc': int,
                 'SUM_HardSoftLollipopStick_EarBu': int,
                 'SUM_Soft_Bag': int,
                 'SUM_Soft_WrapperOrLabel': int,
                 'SUM_Soft_Straw': int,
                 'SUM_Soft_OtherPlastic': int,
                 'SUM_Soft_CigaretteButts': int,
                 'SUM_Soft_StringRingRibbon': int,
                 'Fishing_Net': int,
                 'SUM_FishingLineLureRope': int,
                 'Fishing_BuoysAndFloats': int,
                 'SUM_Foam_OtherPlasticDebris': int,
                 'SUM_OtherPlasticDebris': int,
                 'NAME': str,
                 'COUNTRY': str,
                 'CONTINENT': str,
                 'LAND_TYPE': str,
                 'LAND_RANK': int,
                 'Shape__Area': int,
                 'Shape__Length': int,
                 'Soft_Sheets2': int,
                 'PlasticStraps2': int,
                 'FishingGlowSticks2': int,
                 'FishingOtherPlasticDebris2': int}
