import numpy as np
from numba import njit
from typing import NoReturn


@njit
def mean_filter_upper_ndiag(mat: np.ndarray,
                            new_mat: np.ndarray,
                            h: int,
                            max_bins: int) -> NoReturn:  # pragma: no cover
    """mean filter function

    Applying mean filter to first max_bins diagonals

    Parameters
    ----------
    mat : np.ndarray
        input 2d ndarray
    new_mat : np.ndarray
        output 2d ndarray (result)
    h : int
        mean filter kernel radius -> kernel size = 2*h+1
    max_bins : int
        control applying mean filter to the first max_bins diagonals

    Returns
    -------
    NoReturn
        No return
    """
    rows = mat.shape[1]
    for i in range(rows):
        for j in range(i, min(i+max_bins, rows)):
            kernel_sum = 0
            kernel_size = 0
            for k_i in range(max(i-h, 0), min(i+h+1, rows)):
                for k_j in range(max(j-h, 0), min(j+h+1, rows)):
                    kernel_sum += mat[k_i, k_j]
                    kernel_size += 1
            new_mat[i, j] = kernel_sum/kernel_size


def mean_filter_upper_ndiag_nonjit(mat: np.ndarray,
                                   new_mat: np.ndarray,
                                   h: int,
                                   max_bins: int) -> NoReturn:
    """mean filter function

    Applying mean filter to first max_bins diagonals
    NOTE: this is no njit implementation of mean filter for testing.
    njit implementation should be an EXACT copy of this function.

    Parameters
    ----------
    mat : np.ndarray
        input 2d ndarray
    new_mat : np.ndarray
        output 2d ndarray (result)
    h : int
        mean filter kernel radius -> kernel size = 2*h+1
    max_bins : int
        control applying mean filter to the first max_bins diagonals

    Returns
    -------
    NoReturn
        No return
    """
    rows = mat.shape[1]
    for i in range(rows):
        for j in range(i, min(i+max_bins, rows)):
            kernel_sum = 0
            kernel_size = 0
            for k_i in range(max(i-h, 0), min(i+h+1, rows)):
                for k_j in range(max(j-h, 0), min(j+h+1, rows)):
                    kernel_sum += mat[k_i, k_j]
                    kernel_size += 1
            new_mat[i, j] = kernel_sum/kernel_size
