import sys
from pyhicrep.cli import main


def test_existing_input_data():
    sys.argv = ["pyhicrep",
                "--chrFile=./tests/chr.txt",
                "--maxBins=50",
                "--h=3",
                "--resFolder=test_results",
                "--outFile=testout.txt",
                "-hicParallel",
                "--threads=4",
                "-saveCSV"]
    main()


def test_help():
    sys.argv = ["pyhicrep",
                "--maxBins=50"]
    main()


def test_chrFile():
    sys.argv = ["pyhicrep",
                "--file1=./tests/data/1CSE-10.cool",
                "--file2=./tests/data/1CSE-11.cool",
                "--chrFile=./tests/chr_corrupted.txt",
                "--maxBins=50",
                "--h=3",
                "--outFile=testout.txt",
                "--resFolder=test_results",
                "-pbar",
                "-saveCSV"]
    main()


def test_parallel_method_selection():
    sys.argv = ["pyhicrep",
                "--file1=./tests/data/1CSE-10.cool",
                "--file2=./tests/data/1CSE-11.cool",
                "--chrFile=./tests/chr.txt",
                "--maxBins=50",
                "--h=3",
                "--outFile=testout.txt",
                "--resFolder=test_results",
                "-hicParallel",
                "-chrParallel",
                "-pbar",
                "-saveCSV"]
    main()


def test_chrwise_parallel_error():
    sys.argv = ["pyhicrep",
                "--chr=chr3",
                "--maxBins=50",
                "--h=3",
                "--resFolder=test_results",
                "--outFile=testout.txt",
                "--filesFolder=./tests/data",
                "-chrParallel",
                "--threads=4",
                "-silent"]
    main()
