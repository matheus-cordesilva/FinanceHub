from statistics import mean, stdev, median

import pandas as pd

from dataapi import DBConnect, FocusFeeder

import numpy as np


def historical_normalizer(df):
    df_aux = df.copy()

    normalized_rows_aux = []

    normalized_rows = []

    for ind, row in df_aux.itertuples():

        normalized_rows_aux.append(row)

        if len(normalized_rows_aux) > 1:

            try:

                score = (normalized_rows_aux[-1] - mean(normalized_rows_aux)) / stdev(normalized_rows_aux)

                normalized_rows.append(score)

            except:  # divisão por zero

                score = normalized_rows[-1]

                normalized_rows.append(score)

    normalized_df = df_aux.iloc[1:]

    normalized_df[str(normalized_df.columns[0])].replace(to_replace=normalized_df[str(normalized_df.columns[0])].values,
                                                         value=pd.Series(normalized_rows),
                                                         inplace=True)

    normalized_df.rename(columns={str(normalized_df.columns[0]): 'Normalized ' + str(normalized_df.columns[0])},
                         inplace=True)

    return pd.Series(normalized_rows), normalized_df


def historical_median(df):
    df_aux = df.copy()

    list_median_rows_aux = []

    list_median_rows = []

    for ind, row in df_aux.itertuples():
        list_median_rows_aux.append(row)

        list_median_rows.append(median(list_median_rows_aux))

    df_aux[str(df_aux.columns[0])].replace(to_replace=df_aux[str(df_aux.columns[0])].values,
                                           value=pd.Series(list_median_rows),
                                           inplace=True)

    df_aux.rename(columns={str(df_aux.columns[0]): 'Median-' + str(df_aux.columns[0])}, inplace=True)

    return pd.Series(list_median_rows), df_aux


def macro_indicator(dfs):
    """
    Takes series of macroeconomic data and provides signals if the variable is in an up or down scenario by comparing
    the average series with the median series.

    Parameters
    ----------
    dfs : List of macroeconomic data Pandas DataFrame

    Returns ------- df : Pandas DataFrame with dates as index and columns as the normalized series of each macro
    data, the mean series, the median series, and the signal up (1) and down (0).

    """

    normalized_df_list = []
    for df in dfs:
        normalized_df = historical_normalizer(df)[1]

        normalized_df_list.append(normalized_df)

    concat_df = pd.concat(normalized_df_list, join='inner', axis=1)

    concat_df['average'] = concat_df.mean(axis=1)

    concat_df['median'] = historical_median(concat_df[['average']])[1]

    concat_df['up-down'] = np.where(concat_df['average'] > concat_df['median'], 1, 0)

    return concat_df
