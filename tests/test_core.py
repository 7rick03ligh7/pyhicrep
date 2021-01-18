# import sys
# import os
# sys.path.append(os.path.sep.join(sys.path[0].split(sep=os.path.sep)[:-1]))

import numpy as np
import scipy.sparse as sp
from pyhicrep.src.core.mean_filter import mean_filter_upper_ndiag_nonjit
from pyhicrep.src.core.calc_scc import calc_scc

from pyhicrep.src.core.utils import (
    calc_diag_correlation,
    get_distr_values_of_ranks,
    vstran
)


EPS = 1e-4


def test_mean_filter_upper_ndiag_nonjit():

    # zero values testing
    mat = np.array([
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ])
    mat_res = np.zeros_like(mat, dtype=float)
    mean_filter_upper_ndiag_nonjit(mat, mat_res, h=2, max_bins=5)
    assert np.all(mat_res == mat)

    # single value testing
    mat = np.array([
        [0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ])
    mat_res = np.zeros_like(mat, dtype=float)
    mean_filter_upper_ndiag_nonjit(mat, mat_res, h=2, max_bins=5)
    assert not np.all(mat_res == mat)
    res = np.array([
        [0, 0.08333333, 0.06666667, 0.08333333, 0.11111111],
        [0, 0.0625, 0.05, 0.0625, 0.08333333],
        [0, 0, 0.04, 0.05, 0.06666667],
        [0, 0, 0, 0.0625, 0.08333333],
        [0, 0, 0, 0, 0]
    ])
    assert np.abs(mat_res - res).sum() < EPS

    # multiple values testing
    mat = np.array([
        [1, 0, 0, 0, 0],
        [0, 2, 0, 3, 0],
        [0, 0, 3, 0, 0],
        [0, 0, 0, 2, 0],
        [0, 0, 0, 0, 1]
    ])
    mat_res = np.zeros_like(mat, dtype=float)
    mean_filter_upper_ndiag_nonjit(mat, mat_res, h=2, max_bins=5)
    res = np.array([
        [0.66666667, 0.75,   0.6,   0.66666667, 0.66666667],
        [0,          0.6875, 0.55,  0.625,      0.66666667],
        [0,          0,      0.48,  0.55,       0.6],
        [0,          0,      0,     0.6875,     0.75],
        [0,          0,      0,     0,          0.66666667]
    ])
    assert np.abs(mat_res - res).sum() < EPS

    mean_filter_upper_ndiag_nonjit(mat, mat_res, h=1, max_bins=3)
    res = np.array([
        [0.75,      0.5,        0.83333333, 0.66666667, 0.66666667],
        [0,         0.66666667, 0.88888889, 0.66666667, 0.66666667],
        [0,         0,          1.11111111, 0.88888889, 0.83333333],
        [0,         0,          0,          0.66666667, 0.5],
        [0,         0,          0,          0,          0.75]
    ])
    assert np.abs(mat_res - res).sum() < EPS


def test_calc_scc():
    mat1 = np.array([
        [1, 1, 1, 0, 0],
        [0, 2, 2, 2, 0],
        [0, 0, 3, 3, 3],
        [0, 0, 0, 2, 4],
        [0, 0, 0, 0, 1]
    ])
    mat1 = sp.coo_matrix(mat1)

    mat2 = np.array([
        [1, 4, 1, 0, 0],
        [0, 2, 3, 2, 0],
        [0, 0, 3, 2, 3],
        [0, 0, 0, 2, 1],
        [0, 0, 0, 0, 1]
    ])
    mat2 = sp.coo_matrix(mat2)

    score = calc_scc(mat1, mat2, max_bins=1)
    assert abs(1 - score) < EPS

    score = calc_scc(mat1, mat2, max_bins=2)
    assert abs(0.09090909090909077 - score) < EPS

    score = calc_scc(mat1, mat2, max_bins=3)
    assert abs(0.3333333333333332 - score) < EPS


def test_calc_diag_correlation():
    diags = np.array([
        [1, 2, 3, 2, 1],
        [1, 2, 3, 2, 1],
    ])
    corr, weight = calc_diag_correlation(diags)
    assert abs(1 - corr) < EPS
    assert abs(0.5 - weight) < EPS

    diags = np.array([
        [1, 2, 3, 2, 1],
        [3, 2, 1, 2, 3],
    ])
    corr, weight = calc_diag_correlation(diags)
    assert abs(-1 - corr) < EPS
    assert abs(0.5 - weight) < EPS

    diags = np.array([
        [1, 2, 3, 4, 5],
        [1, 2, 1, 2, 3],
    ])
    corr, weight = calc_diag_correlation(diags)
    assert abs(0.7559289460184544 - corr) < EPS
    assert abs(0.5 - weight) < EPS

    diags = np.array([
        [1, 2, 3, 3],
        [1, 2, 3, 3],
    ])
    corr, weight = calc_diag_correlation(diags)
    assert abs(1 - corr) < EPS
    assert abs(0.4166666666666667 - weight) < EPS


def test_get_distr_values_of_ranks():
    ranks = np.array([3, 1, 2, 2])
    res = np.array([1, 0.25, 0.75, 0.75])
    distr = get_distr_values_of_ranks(ranks)
    assert np.all(res == distr)


def test_vstran():
    diag1 = np.array([1, 2, 3, 4, 5])
    diag2 = np.array([3, 2, 1, 2, 3])
    res1 = np.array([0.2, 0.4, 0.6, 0.8, 1])
    res2 = np.array([0.8, 0.4, 0.2, 0.6, 1])
    distr1, distr2 = vstran(diag1, diag2)
    assert np.all(res1 == distr1)
    assert np.all(res2 == distr2)

    diag1 = np.array([1, 2, 3, 4, 5])
    diag2 = np.array([1, 2, 3, 4, 5])
    distr1, distr2 = vstran(diag1, diag2)
    assert np.all(distr1 == distr2)


# if __name__ == '__main__':
#     test_mean_filter_upper_ndiag_nonjit()
