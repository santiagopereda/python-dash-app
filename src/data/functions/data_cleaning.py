import re
import sys
import shutil
import pandas as pd
import pycountry
import geopy
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
pd.options.display.max_rows = 100


def get_null_percentage(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the null percentage for each column in the DataFrame.
    Parameters:
        df (pd.DataFrame): The input DataFrame.
    Returns:
        pd.DataFrame: A DataFrame with two columns: 'Column Name' and 'Null Percentage'.
    """
    null_percentage = (df.isnull().sum() / len(df)) * 100
    null_df = pd.DataFrame(
        {'Column Name': null_percentage.index, 'Null Percentage': null_percentage.values})
    null_df.set_index('Column Name', inplace=True)
    null_df.index.name = None
    return null_df


def split_column_by_hyphen(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Splits a specified column, adds a hyphen if it doesn't exist, and joins it back together.

    Parameters:
        df (pd.DataFrame): The input DataFrame.
        column (str): The name of the column to split and join.

    Returns:
        pd.DataFrame: The DataFrame with the updated column.
    """
    # Convert the specified column to string type
    df[column] = df[column].astype(str).apply(
        lambda x: x if '-' in x else x[:2] + '-' + x[2:] if len(x) >= 4 else x)

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
                df.at[index, 'COUNTRYAFF'] = raw_data['country']

            if 'country_code' in raw_data:
                df.at[index, 'ISO_CC'] = raw_data['country_code'].upper()
                df.at[index, 'ISO3166-2-lvl4'] = raw_data['ISO3166-2-lvl4']
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
        'COUNTRYAFF', 'ISO_CC', and 'ISO3166-2-lvl4' columns.
    """

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
            print(f"{i}/{country_len} {row['COUNTRY']}", end="\r")

    # Get a subset of the DataFrame for rows with null values in both 'Location' and 'COUNTRY' columns
    null_df = df[df['Location'].isnull() & df['COUNTRY'].isnull()]
    null_len = len(df[df['Location'].isnull() & df['COUNTRY']])
    # Counter for tracking progress
    i = 0
    # Iterate over each row in the subset
    for index, row in null_df.iterrows():
        update_location(df, index)

        i += 1
        print(f"{i}/{null_len} {row['COUNTRY']}", end="\r")

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
            print(f"{i}/{country_len} {row['COUNTRY']}", end="\r")

    return df


def update_countries(df: pd.DataFrame) -> pd.DataFrame:
    """
    Update missing values in the 'COUNTRY' and 'COUNTRYAFF' columns based on a country list.

    Parameters:
        df (pd.DataFrame): The input DataFrame.
        column_list (list): A list of column names to iterate over.

    Returns:
        pd.DataFrame: The DataFrame with updated 'COUNTRY' and 'COUNTRYAFF' columns.
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
                        df.at[index, 'COUNTRYAFF'] = country_name.name
                        break
                    if country_name.alpha_3 in country_lower:
                        df.at[index, 'COUNTRY'] = country_name.name
                        df.at[index, 'COUNTRYAFF'] = country_name.name
                        break
                    if country_name.alpha_2 in country_lower:
                        df.at[index, 'COUNTRY'] = country_name.name
                        df.at[index, 'COUNTRYAFF'] = country_name.name
                        break

    return df


def fill_country_code(df: pd.DataFrame) -> pd.DataFrame:
    """
    Fills missing values in the 'ISO_CC' column based on the 'COUNTRY' column using pycountry.

    Parameters:
        df (pd.DataFrame): The input DataFrame.

    Returns:
        pd.DataFrame: The DataFrame with updated 'ISO_CC' column.
    """
    # Create a mapping of countries to country codes
    country_mapping = {
        country.name: country.alpha_2
        for country in pycountry.countries
    }

    # Iterate over rows with missing values in 'ISO_CC' column
    for index, row in df[df['ISO_CC'].isna() & ~df['COUNTRY'].isna()].iterrows():
        country = row['COUNTRY']

        # Check if country exists in the mapping
        if country in country_mapping:
            # Update the 'ISO_CC' column with the country code
            df.at[index, 'ISO_CC'] = country_mapping[country]

    return df


def fill_country_subdivision(df: pd.DataFrame) -> pd.DataFrame:
    """
    Fills missing values in the 'ISO_SUB', 'NAME', and 'LAND_TYPE' columns based on the 'Location' column using pycountry.

    Parameters:
        df (pd.DataFrame): The input DataFrame.

    Returns:
        pd.DataFrame: The DataFrame with updated 'ISO_SUB', 'NAME', and 'LAND_TYPE' columns.
    """
    # Create a mapping of subdivision names to subdivision codes
    subdivision_mapping = {
        subdivision.name.lower(): subdivision.code
        for subdivision in pycountry.subdivisions
    }

    # Iterate over rows with missing values in 'ISO_SUB' column
    for index, row in df[df['ISO_SUB'].isna()].iterrows():
        location = str(row['Location'])

        matching_subdivision = None
        subdivision_code = None

        # Look for exact matches of subdivision names in the 'Location' column
        for subdivision_name, subdivision_code in subdivision_mapping.items():
            if subdivision_name in location:
                matching_subdivision = subdivision_name
                break

        if matching_subdivision:
            # Update the corresponding columns with the subdivision information
            df.at[index, 'ISO_SUB'] = subdivision_code
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
                    df.at[index, 'ISO_SUB'] = subdivision_code
                    df.at[index, 'NAME'] = pycountry.subdivisions.get(
                        code=subdivision_code).name
                    df.at[index, 'LAND_TYPE'] = pycountry.subdivisions.get(
                        code=subdivision_code).type
                    break

    return df
