"""
Implementation of Chatterjee ksi in Python
chatt(X, Y) - Calculates Chatterjee ksi correlation, correlation is asymmetrical,
    it's checking Y = f(X)
chatt_table(df) - creates a correlation table based on chatterjee ksi, analogue to pd.corr()
requires Pandas
"""

import pandas as pd
from pandas.api.types import is_list_like as is_list

def chatt(X, Y):
    """
    Calculates Chatterjee ksi correlation, correlation is asymmetrical,
    it's checking Y = f(X)

    Args:
        X (list-like): First variable used for correlation
        Y (list-like): Second variable used for correlation

    Returns:
        ksi[float]: Value of chatterjee correlation
    """

    # check if variables are lists
    def is_num_list(list_like):
        if is_list(list_like) and all(isinstance(item, (int, float)) for item in list_like):
            pass
        else:
            raise TypeError(f'{list_like} does not seem to be a list-like full of numbers')

    is_num_list(X)
    is_num_list(Y)

    # to DataFrame and sort
    df_dict = {'X':X, 'Y':Y}
    sorted_list = pd.DataFrame(df_dict).sort_values('X')['Y']
    n_obs = len(sorted_list)

    # nominator
    ascending_list = sorted_list.rank()
    i_0 = ascending_list[0]
    r_sum = 0

    for i in ascending_list[1:]:
        r = abs(i - i_0)
        r_sum = r_sum + r
        i_0 = i

    # denominator
    descending_list = sorted_list.rank(ascending=False)
    L_sum = sum([j * (n_obs - j) for j in descending_list])

    # result
    ksi = 1 - ((n_obs * r_sum) / (2 * L_sum))
    return ksi

def chatt_table(df):
    """creates a correlation table based on chatterjee ksi

    Args:
        df (DataFrame): DataFrame to use for correlations

    Returns:
        df_chatt(DataFrame): table with correlation values, can be used for seaborn heatmap
    """
    df_chatt = pd.DataFrame(columns=df.columns, index=df.columns).astype('float64')

    for i in df:
        for j in df:
            if i == j:
                ksi = 1
            else:
                ksi = chatt(df[i], df[j])
            df_chatt[i][j] = ksi
    return df_chatt
