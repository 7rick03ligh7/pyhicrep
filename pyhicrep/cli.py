import os
import argparse
from src.cpu_single.run_single import run_single

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
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
    arguments = parser.parse_args()

    assert int(arguments.hicParallel) + int(arguments.chrParallel) != 2, (
        "only one parallel method can be selected")

    bin_size = arguments.binSize
    max_bins = arguments.maxBins
    h = arguments.h
    chromnames = [arguments.chr]
    out_file = arguments.outFile
    result_folder = arguments.resFolder

    to_csv = False
    if arguments.saveCSV:
        to_csv = True

    if arguments.file1 and arguments.file2:
        filepathes = [arguments.file1, arguments.file2]
    elif arguments.filesFolder:
        files = os.listdir(arguments.filesFolder)
        folderpath = arguments.filesFolder
        filepathes = [os.path.join(folderpath, file) for file in files]
    else:
        raise("select file1 and file2 or filesFolder")

    if int(arguments.hicParallel) + int(arguments.chrParallel) == 0:
        run_single(filepathes,
                   max_bins,
                   h,
                   chromnames,
                   out_file=out_file,
                   result_folder=result_folder,
                   bin_size=bin_size,
                   to_csv=to_csv
                   )

    elif int(arguments.hicParallel) + int(arguments.chrParallel) == 1:
        if arguments.hicParallel:
            pass
