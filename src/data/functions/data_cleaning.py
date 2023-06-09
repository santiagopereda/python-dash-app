import re
import sys
import geopy
import shutil
import pycountry
import pandas as pd
from unidecode import unidecode
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
pd.options.display.max_rows = 100


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
        location = geolocator.reverse(
            latitude + ',' + longitude, language='en')

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
        print(string + padding, end='\r')

    # Get a list of countries with null values in the 'Location' column
    country_list = df[df['Location'].isnull()]['COUNTRY'].unique()
    country_len = len(df[df['Location'].isnull()]['COUNTRY'])
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
            progress = (f"{i}/{country_len} {row['COUNTRY']}")
            echo(progress)

    # Get a subset of the DataFrame for rows with null values in both 'Location' and 'COUNTRY' columns
    null_df = df[df['Location'].isnull() & df['COUNTRY'].isnull()]
    null_len = len(df[df['Location'].isnull() & df['COUNTRY']])
    # Counter for tracking progress
    i = 0
    # Iterate over each row in the subset
    for index, row in null_df.iterrows():
        update_location(df, index)

        i += 1
        progress = (f"{i}/{null_len} {row['COUNTRY']}")
        echo(progress)

    # Get a list of countries with null values in the 'Location' column
    country_list = df[df['COUNTRY'].isnull(
    )]['CountryName_FromSource'].unique()
    country_len = len(df[df['COUNTRY'].isnull()]['CountryName_FromSource'])
    # Counter for tracking progress
    i = 0
    # Iterate over each country
    for country in country_list:
        # Get a subset of the DataFrame for rows with null values in both 'Location' and 'COUNTRY' columns
        country_df = df[(df['COUNTRY'].isnull()) & (
            df['CountryName_FromSource'] == country)]

        # Iterate over each row in the subset
        for index, row in country_df.iterrows():
            update_location(df, index)

            i += 1
            progress = (f"{i}/{country_len} {row['COUNTRY']}")
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
                code=subdivision_code).name
            df.at[index, 'LAND_TYPE'] = pycountry.subdivisions.get(
                code=subdivision_code).type
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
                        code=subdivision_code).name
                    df.at[index, 'LAND_TYPE'] = pycountry.subdivisions.get(
                        code=subdivision_code).type
                    break
    return df


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
            df.at[index, target_column] = unidecode(newname_map)

    return df
