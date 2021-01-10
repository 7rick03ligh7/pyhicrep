import argparse
from src.cpu_single.run_single import run_single

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--file1',
                        type=str,
                        required=False,
                        default=None,
                        help="Path to the first Hi-C file (*.cool/*.mcool)"
                        )
    parser.add_argument('--file2',
                        type=str,
                        required=False,
                        default=None,
                        help="Path to the second Hi-C file (*.cool/*.mcool)"
                        )
    parser.add_argument('--csvFile',
                        type=str,
                        required=False,
                        default=None,
                        help=("Required for multiple Hi-C data files."
                              "Csv file with paths to cool files ("
                              "first column - filenames, "
                              "second column - paths to files)")
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
                        default='all',
                        required=False,
                        help="Select chromosome for SCC calc")
    parser.add_argument('--maxBins',
                        type=int,
                        default=50,
                        required=False,
                        help="maxBins for SCC calc")
    parser.add_argument('--h',
                        type=int,
                        default=3,
                        required=False,
                        help="Radius of window for SCC calc")
    parser.add_argument('--threads',
                        type=int,
                        default=1,
                        required=False,
                        help="Number of parrallel async threads")
    parser.add_argument('--chrFile',
                        type=str,
                        default=None,
                        required=False,
                        help="File with chromosome names for SCC calc")
    parser.add_argument('--outFile',
                        type=str,
                        default=None,
                        required=False,
                        help="General output filename")
    parser.add_argument('--resFolderName',
                        type=str,
                        default=None,
                        required=False,
                        help="Folder name for saving results")
    parser.add_argument('-saveCSV',
                        type=bool,
                        default=False,
                        required=False,
                        const=True,
                        nargs='?',
                        help=("Flag for generating and saving <chrom name>.csv"
                              "files from general result")
                        )
    parser.add_argument('-hicParallel',
                        type=bool,
                        default=False,
                        required=False,
                        const=True,
                        nargs='?',
                        help=("flag for generating and saving <chrom name>.csv"
                              "files from general result")
                        )
    parser.add_argument('-chrParallel',
                        type=bool,
                        default=False,
                        required=False,
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
    result_folder_name = arguments.resFolderName
    to_csv = False
    if arguments.saveCSV:
        to_csv = True

    # stubs
    is_csv = False
    files = [arguments.file1, arguments.file2]

    if int(arguments.hicParallel) + int(arguments.chrParallel) == 0:
        run_single(files,
                   max_bins,
                   h,
                   chromnames,
                   out_file=out_file,
                   result_folder_name=result_folder_name,
                   bin_size=bin_size,
                   is_csv=is_csv,
                   to_csv=to_csv
                   )
