import numpy as np
from numba import njit
from typing import NoReturn


@njit
def mean_filter_upper_ndiag(mat: np.ndarray,
                            new_mat: np.ndarray,
                            h: int,
                            max_bins: int) -> NoReturn:
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
