# import sys
# import os
# sys.path.append(os.path.sep.join(sys.path[0].split(sep=os.path.sep)[:-1]))


import numpy as np
import pandas as pd
import cooler
import shutil
from pyhicrep.src.utils import (
    open_cooler_file,
    get_out_filepath,
    save_to_csv,
    save_to_txt
)


def test_open_cooler_file():
    clr = cooler.Cooler("./tests/data/1CSE-10.cool")
    mat = clr.matrix(balance=False, sparse=True)
    chrom = clr.chromnames[0]
    fname = "1CSE-10.cool"

    mat_new, fname_new = open_cooler_file("./tests/data/1CSE-10.cool",
                                          bin_size=0)
    assert np.all(~(mat.fetch(chrom) != mat_new.fetch(chrom)).toarray())
    assert fname == fname_new


def test_get_out_filepath():
    path = "result_SCC.txt"
    path_new = get_out_filepath("", "")
    assert path == path_new

    path = "./test_results/test.txt"
    path_new = get_out_filepath(out_file="test.txt",
                                result_folder="test_results")
    assert path == path_new


def test_save_to_txt():
    path = get_out_filepath(out_file="test.txt",
                            result_folder="test_results")
    chromnames = ['testchrom']
    scores = [('f1', 'f2', [1]), ('f1', 'f3', [2]), ('f2', 'f3', [3])]
    save_to_txt(filepath=path,
                chromnames=chromnames,
                all_scores=scores)

    res = [
        "@ testchrom",
        "# f1 f2",
        "1",
        "# f1 f3",
        "2",
        "# f2 f3",
        "3",
    ]
    with open('./test_results/test.txt') as f:
        for i, line in enumerate(f):
            line = line[:-1]
            assert res[i] == line
    shutil.rmtree('./test_results')


def test_save_to_csv():
    txtpath = get_out_filepath(out_file="test.txt",
                               result_folder="test_results")
    csvpath = get_out_filepath(out_file="testchrom.csv",
                               result_folder="test_results")
    chromnames = ['testchrom']
    scores = [('f1', 'f2', [1]), ('f1', 'f3', [2]), ('f2', 'f3', [3])]
    indexnames = ['f1', 'f2', 'f3']
    df = pd.DataFrame(columns=indexnames, index=indexnames)
    df['f1']['f2'] = 1
    df['f2']['f1'] = 1
    df['f1']['f3'] = 2
    df['f3']['f1'] = 2
    df['f2']['f3'] = 3
    df['f3']['f2'] = 3
    df['f1']['f1'] = 1
    df['f2']['f2'] = 1
    df['f3']['f3'] = 1

    save_to_txt(filepath=txtpath,
                chromnames=chromnames,
                all_scores=scores)
    save_to_csv(filepath=txtpath,
                chromnames=chromnames,
                indexnames=indexnames)

    df_new = pd.read_csv(csvpath, index_col=0)
    assert np.all(df.values == df_new.values)
    shutil.rmtree('./test_results')


# if __name__ == "__main__":
#     test_save_to_csv()