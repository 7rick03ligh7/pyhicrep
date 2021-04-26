import sys
import shutil
from .utils import read_txt_results
from pyhicrep.cli import main
reference_data = "./tests/r_hicrep_results.txt"


def test_run_single_from_cli_two_files_chr1():
    sys.argv = ["python pyhicrep/cli.py",
                "--file1=./tests/data/1CSE-10.cool",
                "--file2=./tests/data/1CSE-11.cool",
                "--chr=chr1",
                "--maxBins=50",
                "--h=3",
                "--resFolder=test_results",
                "-silent",
                "-pbar"]
    main()
    real_data = read_txt_results(reference_data)
    gen_data = read_txt_results('./test_results/result_SCC.txt')
    assert abs(gen_data['data']['1CSE-10.cool 1CSE-11.cool'][0] -
               real_data['data']['1CSE-10.cool 1CSE-11.cool'][0]) < 0.01
    shutil.rmtree('./test_results')


def test_run_single_from_cli_two_files_chr2():
    sys.argv = ["python pyhicrep/cli.py",
                "--file1=./tests/data/1CSE-10.cool",
                "--file2=./tests/data/1CSE-11.cool",
                "--chr=chr2",
                "--maxBins=50",
                "--h=3",
                "--resFolder=test_results",
                "-silent",
                "-pbar"]
    main()
    real_data = read_txt_results(reference_data)
    gen_data = read_txt_results('./test_results/result_SCC.txt')
    assert abs(gen_data['data']['1CSE-10.cool 1CSE-11.cool'][0] -
               real_data['data']['1CSE-10.cool 1CSE-11.cool'][1]) < 0.01
    shutil.rmtree('./test_results')


def test_run_single_from_cli_two_files_chr3():
    sys.argv = ["python pyhicrep/cli.py",
                "--file1=./tests/data/1CSE-10.cool",
                "--file2=./tests/data/1CSE-11.cool",
                "--chr=chr3",
                "--maxBins=50",
                "--h=3",
                "--outFile=testout.txt",
                "--resFolder=test_results",
                "-silent",
                "-pbar"]
    main()
    real_data = read_txt_results(reference_data)
    gen_data = read_txt_results('./test_results/testout.txt')
    assert abs(gen_data['data']['1CSE-10.cool 1CSE-11.cool'][0] -
               real_data['data']['1CSE-10.cool 1CSE-11.cool'][2]) < 0.01
    shutil.rmtree('./test_results')


def test_run_single_from_cli_two_files_chr1chr3():
    sys.argv = ["python pyhicrep/cli.py",
                "--file1=./tests/data/1CSE-10.cool",
                "--file2=./tests/data/1CSE-11.cool",
                "--chr=chr1,chr3",
                "--maxBins=50",
                "--h=3",
                "--outFile=testout.txt",
                "--resFolder=test_results",
                "-silent",
                "-pbar"]
    main()
    real_data = read_txt_results(reference_data)
    gen_data = read_txt_results('./test_results/testout.txt')
    assert abs(gen_data['data']['1CSE-10.cool 1CSE-11.cool'][0] -
               real_data['data']['1CSE-10.cool 1CSE-11.cool'][0]) < 0.01
    shutil.rmtree('./test_results')


def test_run_single_from_cli_two_files_chrFile():
    sys.argv = ["python pyhicrep/cli.py",
                "--file1=./tests/data/1CSE-10.cool",
                "--file2=./tests/data/1CSE-11.cool",
                "--chrFile=./tests/chr.txt",
                "--maxBins=50",
                "--h=3",
                "--outFile=testout.txt",
                "--resFolder=test_results",
                "-silent",
                "-pbar"]
    main()
    real_data = read_txt_results(reference_data)
    gen_data = read_txt_results('./test_results/testout.txt')
    assert abs(gen_data['data']['1CSE-10.cool 1CSE-11.cool'][0] -
               real_data['data']['1CSE-10.cool 1CSE-11.cool'][0]) < 0.01
    shutil.rmtree('./test_results')
