import numpy as np
import scipy.stats as ss


def get_distr_values_of_ranks(ranks: np.ndarray) -> np.ndarray:
    """get values from empirical distribution of ranks

    This function gets the ranks, calculates the empirical distribution (ED)
    of the ranks, and returns the values from the ED in the order of the
    ranks received.
    In other words, this function calculates the normalized ranks.

    Parameters
    ----------
    ranks : np.ndarray
        1d ndarray of ranks

    Returns
    -------
    np.ndarray
        1d ndarray of values from ED

    Examples
    --------
    >>> import numpy as np
    >>> ranks = np.array([3,1,2,2])
    >>> get_distr_values_of_ranks(ranks)
    array([1.  , 0.25, 0.75, 0.75])
    """

    uniq, invr, cnt = np.unique(ranks,
                                return_inverse=True,
                                return_counts=True)
    cnt_cumsum = cnt.cumsum()
    distr_values = cnt_cumsum[invr]/cnt_cumsum[-1]
    return distr_values


def vstran(d1: np.ndarray, d2: np.ndarray) -> tuple:
    """calculate variance stabilized weights

    Calculation of variance stabilized weights which describes in paper
    in section "Variance stabilized weights"

    Parameters
    ----------
    d1 : np.ndarray
        1d ndarray of diagonal elements
    d2 : np.ndarray
        1d ndarray of diagonal elements

    Returns
    -------
    tuple
        tuple with 2 elements
        (
            d1 rank distribution
            d2 rank distribution
        )
    """

    ranks1 = ss.rankdata(d1,  method='ordinal')
    ranks2 = ss.rankdata(d2,  method='ordinal')

    ranks1_distr = get_distr_values_of_ranks(ranks1)
    ranks2_distr = get_distr_values_of_ranks(ranks2)

    ranks_distr = (ranks1_distr, ranks2_distr)

    return ranks_distr


def calc_diag_correlation(diags: np.ndarray, mask: np.ndarray) -> tuple:
    """calculate Pearson correalation between two i-th diagonals

    Parameters
    ----------
    diags : np.ndarray
        2d ndarray of i-th diagonals in Hi-C data.
        diags[0] is i-th diagonal in the first Hi-C data
        diags[1] is i-th diagonal in the second Hi-C data
    mask : np.ndarray
        1d ndarray of binary mask of pairwise non-zero values in
        both diags[0] and diags[1]

    Returns
    -------
    tuple
        return tuple with two elements
        (
            Pearson correlation between diags[0] and diags[1],
            variance stabilized weight [see vstran]
        )
    """
    if mask.sum() > 0:
        if (np.unique(diags[0]).shape[0] > 1 and
                np.unique(diags[1]).shape[0] > 1):
            n = diags.shape[1]
            nd = vstran(diags[0], diags[1])

            corr = ss.pearsonr(diags[0], diags[1])[0]
            weight = np.sqrt(np.var(nd[0], ddof=1)*np.var(nd[1], ddof=1))*n

            return (corr, weight)
    return (np.nan, np.nan)
