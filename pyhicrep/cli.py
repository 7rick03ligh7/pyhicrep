import sys
import os
import argparse
import re

from src.cpu_single.run_single import run_single
from src.cpu_parallel.run_parallel import run_parallel
from src.logger import configure_logging


class CustomFormatter(argparse.ArgumentDefaultsHelpFormatter,
                      argparse.MetavarTypeHelpFormatter):
    pass


def main():
    args = sys.argv
    parser = argparse.ArgumentParser(
        formatter_class=CustomFormatter
        )
    parser.add_argument('--file1',
                        type=str,
                        required=False,
                        default="",
                        help="Path to the first Hi-C file (*.cool/*.mcool)"
                        )
    parser.add_argument('--file2',
                        type=str,
                        required=False,
                        default="",
                        help="Path to the second Hi-C file (*.cool/*.mcool)"
                        )
    parser.add_argument('--filesFolder',
                        type=str,
                        required=False,
                        default="",
                        help="Required for multiple Hi-C data files"
                        )
    parser.add_argument('--binSize',
                        type=int,
                        required=False,
                        default=-1,
                        help=("binSize of Hi-C cooler file "
                              "a.k.a. resolution of mcool Hi-C data."
                              "Required if using mcool files")
                        )
    parser.add_argument('--chr',
                        type=str,
                        required=False,
                        default='all',
                        help="Select chromosome for SCC calc")
    parser.add_argument('--maxBins',
                        type=int,
                        required=False,
                        default=50,
                        help="maxBins for SCC calc")
    parser.add_argument('--h',
                        type=int,
                        required=False,
                        default=3,
                        help="Radius of window for SCC calc")
    parser.add_argument('--threads',
                        type=int,
                        required=False,
                        default=1,
                        help="Number of parrallel async threads")
    parser.add_argument('--chrFile',
                        type=str,
                        required=False,
                        default=None,
                        help="File with chromosome names for SCC calc")
    parser.add_argument('--outFile',
                        type=str,
                        required=False,
                        default=None,
                        help="General output filename")
    parser.add_argument('--resFolder',
                        type=str,
                        required=False,
                        default=None,
                        help="Folder name for saving results")
    parser.add_argument('-saveCSV',
                        type=bool,
                        required=False,
                        default=False,
                        const=True,
                        nargs='?',
                        help=("Flag for generating and saving <chrom name>.csv"
                              "files from general result")
                        )
    parser.add_argument('-hicParallel',
                        type=bool,
                        required=False,
                        default=False,
                        const=True,
                        nargs='?',
                        help=("flag for generating and saving <chrom name>.csv"
                              "files from general result")
                        )
    parser.add_argument('-chrParallel',
                        type=bool,
                        required=False,
                        default=False,
                        const=True,
                        nargs='?',
                        help=("flag for generating and saving <chrom name>.csv"
                              "files from general result")
                        )
    parser.add_argument('-silent',
                        type=bool,
                        required=False,
                        default=False,
                        const=True,
                        nargs='?',
                        help=("")
                        )
    parser.add_argument('-pbar',
                        type=bool,
                        required=False,
                        default=False,
                        const=True,
                        nargs='?',
                        help=("")
                        )
    arguments = parser.parse_args()
    if len(args) == 1:
        parser.print_help()
        return

    bin_size = arguments.binSize
    max_bins = arguments.maxBins
    h = arguments.h
    out_file = arguments.outFile
    result_folder = arguments.resFolder

    chromnames = []
    if arguments.chrFile:
        with open(arguments.chrFile, 'r') as f:
            for line in f:
                chromnames.append(line[:-1])
            if line[-1] != '\n':
                print('ERROR: \n must be at last line')
    else:
        chromnames = arguments.chr.split(',')

    is_pbar = arguments.pbar
    if arguments.silent:
        is_pbar = False

    to_csv = False
    if arguments.saveCSV:
        to_csv = True

    if arguments.file1 and arguments.file2:
        filepathes = [arguments.file1, arguments.file2]
    elif arguments.filesFolder:
        files = os.listdir(arguments.filesFolder)
        files.sort(key=lambda f: int(re.sub(r"\D", "", f)))
        folderpath = arguments.filesFolder

        # this crutch for join path with "/" on Windows
        if folderpath[-1] != '/':
            folderpath += '/'
        filepathes = [os.path.join(folderpath, file) for file in files]
    else:
        print(("ERROR: Select file1 and file2 or filesFolder. "
               "For help: pyhicrep --help"))
        return

    logger_stdout = not arguments.pbar and not arguments.silent
    configure_logging(stdout=logger_stdout)

    if int(arguments.hicParallel) + int(arguments.chrParallel) == 0:
        run_single(filepathes,
                   max_bins,
                   h,
                   chromnames,
                   out_file=out_file,
                   result_folder=result_folder,
                   bin_size=bin_size,
                   to_csv=to_csv,
                   is_pbar=is_pbar
                   )

    elif int(arguments.hicParallel) + int(arguments.chrParallel) == 1:
        n_processes = arguments.threads
        if arguments.hicParallel:
            is_hicwise = arguments.hicParallel
        else:
            is_hicwise = not arguments.hicParallel
        run_parallel(filepathes,
                     max_bins,
                     h,
                     chromnames,
                     out_file=out_file,
                     result_folder=result_folder,
                     bin_size=bin_size,
                     to_csv=to_csv,
                     n_processes=n_processes,
                     is_hicwise=is_hicwise,
                     is_pbar=is_pbar
                     )
    else:
        print(("ERROR: Only one of the parallel method can be selected. "
               "For help: pyhicrep --help"))
        return


if __name__ == '__main__':
    main()
