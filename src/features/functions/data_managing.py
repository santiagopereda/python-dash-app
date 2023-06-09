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
