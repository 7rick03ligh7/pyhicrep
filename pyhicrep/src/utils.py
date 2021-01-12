import cooler
import os
import pandas as pd
import numpy as np
from .logger import log


@log
def open_cooler_file(path: str, bin_size: int) -> tuple:
    filename = path.split("/")[-1]
    fileformat = filename.split(".")[-1]
    if fileformat == "mcool":
        path = path + "::resolutions/" + bin_size
    mat = cooler.Cooler(path).matrix(balance=False, sparse=True)
    return mat, filename


@log
def get_out_filepath(out_file: str, result_folder: str) -> str:
    if not out_file:
        filepath = "result_SCC.txt"
    else:
        filepath = out_file

    if result_folder is not None:
        os.makedirs(result_folder, exist_ok=True)
        filepath = f"./{result_folder}/{filepath}"

    return filepath


@log
def save_to_txt(filepath: str,
                chromnames: list,
                all_scores: list
                ):

    with open(filepath, 'w') as f:
        f.write("@ ")
        f.write(" ".join(chromnames))
        f.write("\n")
        for file1, file2, scores in all_scores:
            f.write(f"# {file1} {file2}")
            f.write("\n")
            f.write(", ".join([str(score) for score in scores]))
            f.write("\n")


@log
def save_to_csv(filepath: str,
                chromnames: str,
                indexnames: list
                ):
    data = dict(zip(chromnames,
                    [pd.DataFrame(index=indexnames,
                                  columns=indexnames,
                                  dtype=float) for _ in chromnames]))
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if line[0] == "@":
                continue
            elif line[0] == "#":
                file1, file2 = line.split(" ")[1:3]
            else:
                a = np.array([float(x) for x in line.split(", ")])
                for i, chrom in enumerate(data.keys()):
                    data[chrom].loc[file1, file2] = a[i]
                    data[chrom].loc[file2, file1] = a[i]

    for d in data.values():
        for col in d.columns:
            d.loc[col, col] = 0

    folderpath = "/".join(filepath.split("/")[:-1])
    for k, v in data.items():
        data[k].to_csv(f"./{folderpath}/{k}.csv", index=True)
