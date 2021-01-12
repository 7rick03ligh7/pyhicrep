from ..core.calc_scc import calc_scc
from ..core.mean_smooth import meanFilterSparse
from ..utils import (open_cooler_file,
                     get_out_filepath,
                     save_to_csv,
                     save_to_txt)
from ..logger import log
import logging
from typing import NoReturn


@log
def run_between_two_file(filepathes: list,
                         chromnames: list,
                         bin_size: int,
                         h: int,
                         max_bins: int) -> list:
    all_scores = []
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
    logging.info(f"{file1} {file2} done.")
    return all_scores


@log
def run_between_multiple_files(filepathes: list,
                               chromnames: list,
                               bin_size: int,
                               h: int,
                               max_bins: int) -> list:
    all_scores = []
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

            logging.info(f"{file1} {file2} done.")
    return all_scores


@log
def run_single(filepathes: list,
               max_bins: int,
               h: int,
               chromnames: list,
               out_file="",
               result_folder="",
               bin_size=-1,
               to_csv=False
               ) -> NoReturn:

    # List for calculated SCC
    all_scores = []

    # Calculate SCC between two files
    if len(filepathes) == 2:
        all_scores = run_between_two_file(filepathes,
                                          chromnames,
                                          bin_size,
                                          h,
                                          max_bins)

    # Calculate SCC between multiple files
    else:
        all_scores = run_between_multiple_files(filepathes,
                                                chromnames,
                                                bin_size,
                                                h,
                                                max_bins)

    # Calculate filepath
    filepath = get_out_filepath(out_file=out_file,
                                result_folder=result_folder)

    # Saving to txt
    save_to_txt(filepath, chromnames=chromnames, all_scores=all_scores)
    logging.info(f"txt result saved in {filepath}")

    # Saving to csv
    if to_csv:
        filenames = [path.split('/')[-1] for path in filepathes]
        save_to_csv(filepath,
                    chromnames=chromnames,
                    indexnames=filenames)
        logging.info(f"csv result saved in {filepath}")
