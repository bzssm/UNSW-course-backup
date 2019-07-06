## import modules here 
import pandas as pd
import numpy as np


################# Question 1 #################
def read_data(filename):
    df = pd.read_csv(filename, sep='\t')
    return (df)


# helper functions
def project_data(df, d):
    # Return only the d-th column of INPUT
    return df.iloc[:, d]


def select_data(df, d, val):
    # SELECT * FROM INPUT WHERE input.d = val
    col_name = df.columns[d]
    return df[df[col_name] == val]


def remove_first_dim(df):
    # Remove the first dim of the input
    return df.iloc[:, 1:]


def slice_data_dim0(df, v):
    # syntactic sugar to get R_{ALL} in a less verbose way
    df_temp = select_data(df, 0, v)
    return remove_first_dim(df_temp)


def buc_rec_optimized(df):  # do not change the heading of the function
    return buc1(df) if df.shape[0] == 1 else buc(df, [], pd.DataFrame(columns=list(df)))


def buc1(df):
    res = [list(df.loc[0])[:len(df.loc[0]) - 1]]

    for val in res:
        row = [e for e in val]
        for i, row_value in enumerate(row):
            if row_value != 'ALL':
                res_value = [(row[j], 'ALL')[j == i] for j in range(len(row))]
                if set(res_value) != {'ALL'}:
                    res.append(res_value)
    res.append(['ALL' for _ in df.loc[0][:-1]])

    rescopy = []
    for e in res:
        if e not in rescopy:
            rescopy.append(list(e))
    for e in rescopy:
        e.append(df.loc[0][-1])

    return pd.DataFrame(rescopy, columns=list(df))


def buc(df, num, res):
    if df.shape[1] == 1:
        res.loc[len(res)] = num + [sum(project_data(df, 0))]
    else:
        num_copy = [e for e in num]
        for v in set(project_data(df, 0).values):
            buc(slice_data_dim0(df, v), [e for e in num_copy] + [v], res)
        buc(remove_first_dim(df), [e for e in num_copy] + ['ALL'], res)
    return res


################# Question 2 #################

def v_opt_dp(x, num_bins):  # do not change the heading of the function

    matrix = [[-1 for i in range(len(x))] for j in range(num_bins)]
    matrix_index = [[-1 for i in range(len(x))] for j in range(num_bins)]
    xcopy = x
    nb_of_bins = num_bins
    vodp(0, num_bins - 1, xcopy, nb_of_bins, matrix, matrix_index)  # bin is 0-3
    start = matrix_index[-1][0]
    startcopy = start
    bins = [x[:start]]
    for i in range(len(matrix_index) - 2, 0, -1):
        start = matrix_index[i][start]
        bins.append(x[startcopy:start])
        startcopy = start
    bins.append(x[startcopy:])
    return matrix, bins


def vodp(xmatrix, rest_nb_of_bins, xcopy, nb_of_bins, matrix, matrix_index):
    if all([nb_of_bins - rest_nb_of_bins < 2 + xmatrix, len(xcopy) - xmatrix > rest_nb_of_bins]):
        vodp(xmatrix + 1, rest_nb_of_bins, xcopy, nb_of_bins, matrix, matrix_index)
        if not rest_nb_of_bins:
            matrix[rest_nb_of_bins][xmatrix] = np.var(xcopy[xmatrix:]) * len(xcopy[xmatrix:])
            return
        else:
            vodp(xmatrix, rest_nb_of_bins - 1, xcopy, nb_of_bins, matrix, matrix_index)
            min_list = [matrix[rest_nb_of_bins - 1][xmatrix + 1]]
            for i in range(xmatrix + 2, len(xcopy)):
                min_list.append(matrix[rest_nb_of_bins - 1][i] + np.var(xcopy[xmatrix:i]) * (i - xmatrix))
            matrix[rest_nb_of_bins][xmatrix] = min(min_list)
            matrix_index[rest_nb_of_bins][xmatrix] = min_list.index(matrix[rest_nb_of_bins][xmatrix]) + xmatrix + 1
