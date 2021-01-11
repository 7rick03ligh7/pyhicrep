from src.core.calc_scc import calc_scc
from src.core.mean_smooth import meanFilterSparse
from src.utils import (open_cooler_file,
                       get_out_filepath,
                       save_to_csv,
                       save_to_txt)


def run_single(filepathes: list,
               max_bins: int,
               h: int,
               chromnames: list,
               out_file="",
               result_folder="",
               bin_size=-1,
               to_csv=False
               ):

    # List for calculated SCC
    all_scores = []

    # Calculate SCC between two files
    if len(filepathes) == 2:
        path1, path2 = filepathes
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
        for i, path1 in enumerate(filepathes[:-1]):
            paths2 = filepathes[i+1:]
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
                                result_folder=result_folder)

    # Saving to txt
    save_to_txt(filepath, chromnames=chromnames, all_scores=all_scores)

    # Saving to csv
    if to_csv:
        filenames = [path.split('/')[-1] for path in filepathes]
        save_to_csv(filepath,
                    chromnames=chromnames,
                    indexnames=filenames)
