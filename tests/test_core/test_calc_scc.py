from pyhicrep.src.core.calc_scc import calc_scc
from pyhicrep.src.core.mean_smooth import meanFilterSparse
import cooler


def test_calc_scc():
    clr1 = cooler.Cooler("./tests/data/1CSE-6.cool")
    clr2 = cooler.Cooler("./tests/data/1CSE-9.cool")
    mat1 = clr1.matrix(balance=False,
                       sparse=True).fetch('chr1')
    mat2 = clr2.matrix(balance=False,
                       sparse=True).fetch('chr1')

    mat1 = meanFilterSparse(mat1, 3)
    mat2 = meanFilterSparse(mat2, 3)
    res = calc_scc(mat1, mat2, 50)
    assert str(res)[:6] == str(-0.05866464993050103)[:6]
