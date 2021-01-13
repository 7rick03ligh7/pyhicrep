import os
import shutil
from utils import read_txt_results
reference_data = "./tests/r_hicrep_results.txt"


def test_run_single_from_cli_two_files_chr1():
    os.system(("python pyhicrep/cli.py "
               "--file1=./tests/data/1CSE-6.cool "
               "--file2=./tests/data/1CSE-7.cool "
               "--chr=chr1 "
               "--maxBins=50 "
               "--h=3 "
               "--resFolder=test_results "
               "-silent"))
    real_data = read_txt_results(reference_data)
    gen_data = read_txt_results('./test_results/result_SCC.txt')
    assert abs(gen_data['data']['1CSE-6.cool 1CSE-7.cool'][0] -
               real_data['data']['1CSE-6.cool 1CSE-7.cool'][0]) < 0.01
    shutil.rmtree('./test_results')


def test_run_single_from_cli_two_files_chr2():
    os.system(("python pyhicrep/cli.py "
               "--file1=./tests/data/1CSE-6.cool "
               "--file2=./tests/data/1CSE-7.cool "
               "--chr=chr2 "
               "--maxBins=50 "
               "--h=3 "
               "--resFolder=test_results "
               "-silent"))
    real_data = read_txt_results(reference_data)
    gen_data = read_txt_results('./test_results/result_SCC.txt')
    assert abs(gen_data['data']['1CSE-6.cool 1CSE-7.cool'][0] -
               real_data['data']['1CSE-6.cool 1CSE-7.cool'][1]) < 0.01
    shutil.rmtree('./test_results')


def test_run_single_from_cli_two_files_chr3():
    os.system(("python pyhicrep/cli.py "
               "--file1=./tests/data/1CSE-6.cool "
               "--file2=./tests/data/1CSE-7.cool "
               "--chr=chr3 "
               "--maxBins=50 "
               "--h=3 "
               "--outFile=testout.txt "
               "--resFolder=test_results "
               "-silent"))
    real_data = read_txt_results(reference_data)
    gen_data = read_txt_results('./test_results/testout.txt')
    assert abs(gen_data['data']['1CSE-6.cool 1CSE-7.cool'][0] -
               real_data['data']['1CSE-6.cool 1CSE-7.cool'][2]) < 0.01
    shutil.rmtree('./test_results')


def test_run_single_from_cli_two_files_chr1chr3():
    os.system(("python pyhicrep/cli.py "
               "--file1=./tests/data/1CSE-6.cool "
               "--file2=./tests/data/1CSE-7.cool "
               "--chr=chr1,chr3 "
               "--maxBins=50 "
               "--h=3 "
               "--outFile=testout.txt "
               "--resFolder=test_results "
               "-silent"))
    real_data = read_txt_results(reference_data)
    gen_data = read_txt_results('./test_results/testout.txt')
    assert abs(gen_data['data']['1CSE-6.cool 1CSE-7.cool'][0] -
               real_data['data']['1CSE-6.cool 1CSE-7.cool'][0]) < 0.01
    shutil.rmtree('./test_results')


def test_run_single_from_cli_two_files_chrFile():
    os.system(("python pyhicrep/cli.py "
               "--file1=./tests/data/1CSE-6.cool "
               "--file2=./tests/data/1CSE-7.cool "
               "--chrFile=./tests/chr.txt "
               "--maxBins=50 "
               "--h=3 "
               "--outFile=testout.txt "
               "--resFolder=test_results "
               "-silent"))
    real_data = read_txt_results(reference_data)
    gen_data = read_txt_results('./test_results/testout.txt')
    assert abs(gen_data['data']['1CSE-6.cool 1CSE-7.cool'][0] -
               real_data['data']['1CSE-6.cool 1CSE-7.cool'][0]) < 0.01
    shutil.rmtree('./test_results')
