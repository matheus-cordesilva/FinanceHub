from statistics import mean, stdev, median

import pandas as pd

import numpy as np


class MacroIndicator(object):
    """
    To build a macroeconomic indicator according to Ilmanem (2014).

    """

    def __init__(self):
        pass

    def _historical_normalizer(self, df):
        """
        Normalize the series iterating row by row.

        Parameters
        ----------
        df : Pandas Dataframe uni-column

        Returns
        -------
        Series: with the normalized series
        df: Pandas Dataframe with data as index and column of the normalized series

        """
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

        normalized_df[str(normalized_df.columns[0])].replace(
            to_replace=normalized_df[str(normalized_df.columns[0])].values,
            value=pd.Series(normalized_rows),
            inplace=True)

        normalized_df.rename(columns={str(normalized_df.columns[0]): 'Normalized ' + str(normalized_df.columns[0])},
                             inplace=True)

        return pd.Series(normalized_rows), normalized_df

    def _expanding_median(self, df):
        """
        Calculates the historical median iterating row by row

        Parameters
        ----------
        df : Pandas Dataframe uni-column

        Returns
        -------
        Series: with the historical median
        df: Pandas Dataframe with data as index and column of the median series

        """
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

    def get_macro_indicator(self, dfs, name, median_type, window=3):
        """
        Takes series of macroeconomic data and provides signals if the variable is in an up or down scenario by comparing
        the average series with the median series.

        Parameters
        ----------
        dfs: List of macroeconomic data Pandas DataFrame
        name: str pf the name of the macro indicator, e.g. 'growth'
        median_type: str 'expanding' or 'rolling'
        window: number of years that will be used in the rolling median

        Returns
        -------
        df : Pandas DataFrame with dates as index and columns as: (1) normalized series of each macro
        data, (2) the mean series, (3) the median series, and (4) the signal up (1) and down (0).

        """

        normalized_df_list = []
        for df in dfs:
            normalized_df = self._historical_normalizer(df)[1]

            normalized_df_list.append(normalized_df)

        concat_df = pd.concat(normalized_df_list, join='inner', axis=1)

        concat_df['Average ' + '({})'.format(name)] = concat_df.mean(axis=1)

        if median_type == 'rolling':

            median_df = concat_df[['Average ' + '({})'.format(name)]].rolling(window * 252).median()

            median_df.rename(columns={'Average ' + '({})'.format(name): 'Median ' + '({})'.format(name)},
                             inplace=True)

            median_df.dropna(inplace=True)

            concat_df = concat_df.join(median_df, how='inner')

        elif median_type == 'expanding':

            concat_df['Median ' + '({})'.format(name)] = \
            self._expanding_median(concat_df[['Average ' + '({})'.format(name)]])[1]

        else:
            raise ValueError('The only two valid arguments are "rolling" and "expanding".')

        concat_df['Up-Down ' + '({})'.format(name)] = np.where(
            concat_df['Average ' + '({})'.format(name)] > concat_df['Median ' + '({})'.format(name)], 1, 0)

        return concat_df

    def get_final_dataframe(self, factor_return_df, macro_indicator_df1, macro_indicator_df2):
        """
        Merge the factor return dataframe with the macro indicators dataframes, applying a 'backfill' method of filling NA data
        on the macro indicators dataframes, keeping the factor return dataframe as the original.

        Parameters
        ----------
        factor_return_df: Pandas DataFrame with the daily factor returns.
        macro_indicator_df1: Pandas DataFrame with the macro indicator signals.
        macro_indicator_df2: Pandas DataFrame with the macro indicator signals

        Returns
        -------
        df : Pandas DataFrame with the factor returns and the macro idnicator signals.

        """

        factor_retruns_signals_aux1 = factor_return_df.loc[macro_indicator_df1.index[0]:macro_indicator_df1.index[-1],
                                      :].join(macro_indicator_df1[[str(macro_indicator_df1.columns[-1])]], how='left')
        factor_retruns_signals_aux1.fillna(method='backfill', inplace=True)

        factor_retruns_signals_aux2 = factor_retruns_signals_aux1.loc[
                                      macro_indicator_df2.index[0]:macro_indicator_df2.index[-1], :].join(
            macro_indicator_df2[[str(macro_indicator_df2.columns[-1])]], how='left')
        factor_retruns_signals_aux2.fillna(method='backfill', inplace=True)

        return factor_retruns_signals_aux2