import os
import shutil
from .utils import read_txt_results
reference_data = "./tests/r_hicrep_results.txt"


def test_run_parallel_from_cli_multiple_files_chr1():
    os.system(("python pyhicrep/cli.py "
               "--chr=chr1 "
               "--maxBins=50 "
               "--h=3 "
               "--resFolder=test_results "
               "--filesFolder=./tests/data "
               "-hicParallel "
               "--threads=4 "
               "-silent"))
    real_data = read_txt_results(reference_data)
    gen_data = read_txt_results('./test_results/result_SCC.txt')

    assert len(real_data) == len(gen_data)

    gen_chromnames = gen_data['chromnames']
    real_chromnames = real_data['chromnames']
    gen_chromnames_indmap = []
    for gchrom in gen_chromnames:
        for i, rchrom in enumerate(real_chromnames):
            if gchrom == rchrom:
                gen_chromnames_indmap.append(i)

    for filenames, scores in real_data['data'].items():
        for i, ind in enumerate(gen_chromnames_indmap):
            assert abs(gen_data['data'][filenames][i] - scores[ind]) < 0.01

    shutil.rmtree('./test_results')


def test_run_parallel_from_cli_multiple_files_chr3():
    os.system(("python pyhicrep/cli.py "
               "--chr=chr3 "
               "--maxBins=50 "
               "--h=3 "
               "--resFolder=test_results "
               "--outFile=testout.txt "
               "--filesFolder=./tests/data "
               "-hicParallel "
               "--threads=4 "
               "-silent"))
    real_data = read_txt_results(reference_data)
    gen_data = read_txt_results('./test_results/testout.txt')

    assert len(real_data) == len(gen_data)

    gen_chromnames = gen_data['chromnames']
    real_chromnames = real_data['chromnames']
    gen_chromnames_indmap = []
    for gchrom in gen_chromnames:
        for i, rchrom in enumerate(real_chromnames):
            if gchrom == rchrom:
                gen_chromnames_indmap.append(i)

    for filenames, scores in real_data['data'].items():
        for i, ind in enumerate(gen_chromnames_indmap):
            assert abs(gen_data['data'][filenames][i] - scores[ind]) < 0.01

    shutil.rmtree('./test_results')


def test_run_parallel_from_cli_multiple_files_chr1ch2():
    os.system(("python pyhicrep/cli.py "
               "--chr=chr1,chr2 "
               "--maxBins=50 "
               "--h=3 "
               "--resFolder=test_results "
               "--outFile=testout.txt "
               "--filesFolder=./tests/data "
               "-hicParallel "
               "--threads=4 "
               "-silent"))
    real_data = read_txt_results(reference_data)
    gen_data = read_txt_results('./test_results/testout.txt')

    assert len(real_data) == len(gen_data)

    gen_chromnames = gen_data['chromnames']
    real_chromnames = real_data['chromnames']
    gen_chromnames_indmap = []
    for gchrom in gen_chromnames:
        for i, rchrom in enumerate(real_chromnames):
            if gchrom == rchrom:
                gen_chromnames_indmap.append(i)

    for filenames, scores in real_data['data'].items():
        for i, ind in enumerate(gen_chromnames_indmap):
            assert abs(gen_data['data'][filenames][i] - scores[ind]) < 0.01

    shutil.rmtree('./test_results')


def test_run_parallel_from_cli_multiple_files_chrFile():
    os.system(("python pyhicrep/cli.py "
               "--chrFile=./tests/chr.txt "
               "--maxBins=50 "
               "--h=3 "
               "--resFolder=test_results "
               "--outFile=testout.txt "
               "--filesFolder=./tests/data "
               "-hicParallel "
               "--threads=4 "
               "-silent"))
    real_data = read_txt_results(reference_data)
    gen_data = read_txt_results('./test_results/testout.txt')

    assert len(real_data) == len(gen_data)

    gen_chromnames = gen_data['chromnames']
    real_chromnames = real_data['chromnames']
    gen_chromnames_indmap = []
    for gchrom in gen_chromnames:
        for i, rchrom in enumerate(real_chromnames):
            if gchrom == rchrom:
                gen_chromnames_indmap.append(i)

    for filenames, scores in real_data['data'].items():
        for i, ind in enumerate(gen_chromnames_indmap):
            assert abs(gen_data['data'][filenames][i] - scores[ind]) < 0.01

    shutil.rmtree('./test_results')
