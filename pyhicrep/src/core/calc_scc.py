import numpy as np
import scipy.sparse as sp
from .utils import calc_diag_correlation
from ..logger import log


@log
def calc_scc(mat1: sp.coo_matrix, mat2: sp.coo_matrix, max_bins: int) -> float:
    """calculate SCC between two hi-c matrix

    Calculate SCC between two sparse coo_matrix with identical shape

    Parameters
    ----------
    mat1 : sp.coo_matrix
        2d sparse coo_matrix of first hi-c matrix
    mat2 : sp.coo_matrix
        2d sparse coo_matrix of second hi-c matrix
    max_bins : int
        max i-th diagonals for SCC calculation

    Returns
    -------
    float
        SCC score (float value from -1 to 1)
    """

    # TODO: add assert that shape is equal

    corrs = []
    weights = []

    for i in range(max_bins):
        diag1 = mat1.diagonal(i)
        diag2 = mat2.diagonal(i)

        mask = ~((diag1 == 0) & (diag2 == 0))

        diags = np.zeros((2, mask.sum()))

        diags[0] = diag1[mask]
        diags[1] = diag2[mask]

        corr, weight = calc_diag_correlation(diags)

        if not np.isnan(corr):
            corrs.append(corr)
            weights.append(weight)

    weights = np.array(weights)
    corrs = np.array(corrs)
    weights = weights/weights.sum()
    return (corrs*weights).sum()
