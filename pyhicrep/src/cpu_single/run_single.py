import pandas as pd

from src.core.calc_scc import calc_scc
from src.core.mean_smooth import meanFilterSparse
from src.utils import (open_cooler_file,
                       get_out_filepath,
                       save_to_csv,
                       save_to_txt)


def run_single(files: list,
               max_bins: int,
               h: int,
               chromnames: list,
               out_file="",
               result_folder_name="",
               bin_size=-1,
               is_csv=False,
               to_csv=False
               ):

    # List for calculated SCC
    all_scores = []

    # Calculate SCC between two files
    if not is_csv:
        path1, path2 = files
        mat1, file1 = open_cooler_file(path1, bin_size=bin_size)
        mat2, file2 = open_cooler_file(path2, bin_size=bin_size)
        scores = []

        for chrom in chromnames:
            hic1 = mat1.fetch(chrom)
            hic2 = mat2.fetch(chrom)

            hic1 = meanFilterSparse(hic1, h=h)
            hic2 = meanFilterSparse(hic2, h=h)

            score = calc_scc(hic1, hic2, max_bins=max_bins)
            scores.append(score)
        all_scores.append([file1, file2, scores])

    # Calculate SCC between multiple files
    else:
        data = pd.read_csv(files[0])
        for i, path1 in enumerate(data['full_path'][:-1]):
            paths2 = data['full_path'][i+1:]
            mat1, file1 = open_cooler_file(path1, bin_size=bin_size)
            for j, path2 in enumerate(paths2):
                mat2, file2 = open_cooler_file(path2, bin_size=bin_size)
                scores = []

                for chrom in chromnames:
                    hic1 = mat1.fetch(chrom)
                    hic2 = mat2.fetch(chrom)

                    hic1 = meanFilterSparse(hic1, h=h)
                    hic2 = meanFilterSparse(hic2, h=h)

                    score = calc_scc(hic1, hic2, max_bins=max_bins)
                    scores.append(score)
                all_scores.append([file1, file2, scores])

    filepath = get_out_filepath(out_file=out_file,
                                result_folder_name=result_folder_name)

    # Saving to txt
    save_to_txt(filepath, chromnames=chromnames, all_scores=all_scores)

    # Saving to csv
    if to_csv:
        save_to_csv(filepath,
                    chromnames=chromnames,
                    indexnames=list(data['name'].values))
