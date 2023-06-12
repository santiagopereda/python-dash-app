import pandas as pd
import plotly.express as px

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


def dynamic_barchart(df: pd.DataFrame, bar_chart_cols: list) -> None:
    """
    Generate a dynamic bar chart based on a DataFrame and specified column names.

    Args:
        df (pandas.DataFrame): The input DataFrame.
        bar_chart_cols (list): List of column names to include in the bar chart.

    Returns:
        None
    """
    # Transpose the DataFrame
    transposed_df = df[bar_chart_cols].T

    # Group by the third level and sum the values
    transposed_df = transposed_df.groupby(level=2, axis=1).sum()

    # Calculate the sum of each COUNTRY and NAME and add a 'SUM' column
    transposed_df['SUM'] = transposed_df.sum(axis=1)

    # Sort the DataFrame by the 'SUM' column in descending order
    transposed_df = transposed_df.sort_values(by='SUM', ascending=False)

    # Calculate the cumulative sum of the 'SUM' column
    transposed_df['cumulative_sum'] = transposed_df['SUM'].cumsum()

    # Find the threshold value for the top 80% most relevant bars
    threshold = transposed_df['SUM'].sum() * 0.8

    # Filter the DataFrame to include only the bars below the threshold
    filtered_df = transposed_df[transposed_df['cumulative_sum'] <= threshold]
    
    return filtered_df

