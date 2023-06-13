import pandas as pd
import plotly.express as px

# --------------------------------------------------------------
# Data Slice Parameters
# --------------------------------------------------------------


def slice_multi_index_dataframe(df: pd.DataFrame, level_one_slice=slice(None), level_two_slice=slice(None), year_slice=slice(None)) -> pd.DataFrame:
    """
    Slices a DataFrame with a multi-level index based on the provided level slices.
    Parameters:
        df (pd.DataFrame): The input DataFrame with a multi-level index.
        level_one_slice (slice): Slice for the first level of the multi-level index. Default is slice(None).
        level_two_slice (slice): Slice for the second level of the multi-level index. Default is slice(None).
        year_slice (slice): Slice for the third level of the multi-level index. Default is slice(None).
    Returns:
        pd.DataFrame: The sliced DataFrame based on the provided level slices.
    """
    # Create the pd.IndexSlice object
    idx = pd.IndexSlice

    # Use .loc accessor and pd.IndexSlice to slice the DataFrame
    sliced_df = df.loc[idx[level_one_slice,
                           level_two_slice, year_slice], :]

    return sliced_df


def yearly_filtered_data(df: pd.DataFrame, bar_chart_cols: list, threshold_check: bool) -> pd.DataFrame:
    """
    Generate a dynamic bar chart based on a DataFrame and specified column names, with an option to apply a threshold.

    Args:
        df (pandas.DataFrame): The input DataFrame.
        bar_chart_cols (list): List of column names to include in the bar chart.
        threshold_check (bool): Whether to apply a threshold for the top 80% most relevant bars.

    Returns:
        pandas.DataFrame: The filtered DataFrame based on the threshold (if applied).
    """
    # Transpose the DataFrame
    transposed_df = df[bar_chart_cols].T

    # Group by the third level and sum the values
    transposed_df = transposed_df.groupby(level=2, axis=1).sum()

    # Calculate the sum of each COUNTRY and NAME and add a 'SUM' column
    transposed_df['SUM'] = transposed_df.sum(axis=1)

    # Sort the DataFrame by the 'SUM' column in descending order
    transposed_df = transposed_df.sort_values(by='SUM', ascending=False)

    if threshold_check:
        # Calculate the cumulative sum of the 'SUM' column
        transposed_df['cumulative_sum'] = transposed_df['SUM'].cumsum()

        # Find the threshold value for the top 80% most relevant bars
        threshold = transposed_df['SUM'].sum() * 0.8

        # Filter the DataFrame to include only the bars below the threshold
        filtered_df = transposed_df[transposed_df['cumulative_sum'] <= threshold]
    else:
        # No threshold applied, use the entire DataFrame
        filtered_df = transposed_df

    return filtered_df


def location_filter(df: pd.DataFrame, level_one_slice, level_two_slice, threshold_check: bool) -> pd.DataFrame:
    """
    Filter the DataFrame based on level one and level two slices, and apply a threshold if specified.

    Args:
        df (pd.DataFrame): The input DataFrame to filter.
        level_one_slice: The slice or value to filter the 'COUNTRY' column.
        level_two_slice: The slice or value to filter the 'NAME' column.
        threshold_check (bool): Whether to apply a threshold based on the 'SUM' column.

    Returns:
        pd.DataFrame: The filtered DataFrame.
    """
    dff = df.copy()

    # List of columns to drop from the DataFrame
    drop_list = ['UniqueID', 'LocationFreqID', 'Dataset', 'Organization',
                 'Longitude1', 'Latitude1', 'TotalLength_m', 'EventType',
                 'TotalVolunteers', 'DateStandardized', 'Totalltems_EventRecord',
                 'TotalClassifiedItems_EC2020', 'ISO_CODE', 'CONTINENT', 'LAND_TYPE', 'LAND_RANK',
                 'Shape__Area', 'Shape__Length', 'Count_']
    dff.drop(drop_list, axis=1, inplace=True)

    if isinstance(level_one_slice, slice) and isinstance(level_two_slice, slice):
        # Filter by level one slice
        dff.drop(["NAME", "Location"], axis=1, inplace=True)
        dff = dff.groupby("COUNTRY").sum()
        dff['SUM'] = dff.sum(axis=1)
        dff = dff.sort_values(by='SUM', ascending=False)

    elif not isinstance(level_one_slice, slice) and isinstance(level_two_slice, slice):
        # Filter by level one slice
        dff = dff[dff['COUNTRY'] == level_one_slice]
        dff.drop(["COUNTRY", "Location"], axis=1, inplace=True)
        dff = dff.groupby("NAME").sum()
        dff['SUM'] = dff.sum(axis=1)
        dff = dff.sort_values(by='SUM', ascending=False)

    elif not isinstance(level_one_slice, slice) and not isinstance(level_two_slice, slice):
        # Filter by both level one and level two slices
        dff = dff[(dff['COUNTRY'] == level_one_slice)
                  & (dff['NAME'] == level_two_slice)]
        dff.drop(["COUNTRY", "NAME"], axis=1, inplace=True)
        dff = dff.groupby("Location").sum()
        dff['SUM'] = dff.sum(axis=1)
        dff = dff.sort_values(by='SUM', ascending=False)

    if threshold_check:
        # Calculate the cumulative sum of the 'SUM' column
        dff['cumulative_sum'] = dff['SUM'].cumsum()
        # Find the threshold value for the top 90% most relevant bars
        threshold = dff['SUM'].sum() * 0.9

        # Filter the DataFrame to include only the bars below the threshold
        filtered_df = dff[dff['cumulative_sum'] <= threshold]
    else:
        # No threshold applied, use the entire DataFrame
        filtered_df = dff

    return filtered_df
