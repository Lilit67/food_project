import pandas as pd


def set_val_at(df, row, col, val):
    pass

def walk_rows(df, operation):
    for index, row in df.iterrows():
        print(row['A'], row['B'])


def get_values(df, col):
    dfList = df.col.values
    return dfList


def df_to_matrix(df):
    matix_type = df.as_matrix()
    return matix_type


def reindex(df, index=[]):
    df1 = df.set_index(index)
    df1.sort_index(inplace=True)
    print('Reindexed: {}'.format(df1))

    return df1

def sum_by_one_column(df, column):
    """ Groups by one column, and sums applicable columns"""
    # Create group object
    one = df.groupby(col)

    # Apply sum function
    df2 = one.sum()
    return df2

def sum_by_multi_columns(df, cols=[]):
    """
    Creates a mutiindexed columns sum
    Example, cols=['stepNo', 'ingredient']
    """
    letterone = df.groupby(cols).sum()
    return letterone

def add_column_init_with_same_value(df, colname, val):
    df[colname] = val
    return df

def delete_column(df, colname):
    del df[colname]
    return df

def set_cell_at_index(df, index, col, val):
    """
    Set at whatever index is given. Multiindex should be a list
    :param df:
    :param index:
    :param col:
    :param val:
    :return:
    """
    # TODO: necessary checks...
    df.loc[index, col] = val
    return df

def inspect_data(self, df):
    """ Count nulls in df """
    col_nulls = df.isnull().sum()
    cols = df.columns
    for col in cols:
        pass

def drop_empty_cols(self, df):
    df.dropna(axis=1, how='all')
    return df

def drop_empty_rows(self, df):
    df.dropna(axis=0, how='all')