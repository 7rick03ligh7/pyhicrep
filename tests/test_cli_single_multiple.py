import sys
import shutil
from .utils import read_txt_results
from pyhicrep.cli import main
reference_data = "./tests/r_hicrep_results.txt"


def test_run_single_from_cli_multiple_files_chr1():
    sys.argv = ["pyhicrep",
                "--chr=chr1",
                "--maxBins=50",
                "--h=3",
                "--resFolder=test_results",
                "--filesFolder=./tests/data",
                "-silent"]
    main()
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


def test_run_single_from_cli_multiple_files_chr3():
    sys.argv = ["pyhicrep",
                "--chr=chr3",
                "--maxBins=50",
                "--h=3",
                "--resFolder=test_results",
                "--filesFolder=./tests/data",
                "-silent"]
    main()
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


def test_run_single_from_cli_multiple_files_chr2chr3():
    sys.argv = ["pyhicrep",
                "--chr=chr2,chr3",
                "--maxBins=50",
                "--h=3",
                "--resFolder=test_results",
                "--filesFolder=./tests/data",
                "-silent"]
    main()
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


def test_run_single_from_cli_multiple_files_chrFile():
    sys.argv = ["pyhicrep",
                "--chrFile=./tests/chr.txt",
                "--maxBins=50",
                "--h=3",
                "--resFolder=test_results",
                "--filesFolder=./tests/data",
                "-silent"]
    main()
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
