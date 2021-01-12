import os
from pyhicrep.src.cpu_single.run_single import run_between_two_file
from pyhicrep.src.cpu_single.run_single import run_between_multiple_files


def test_run_between_two_file():
    scores = run_between_two_file(["./tests/data/1CSE-6.cool",
                                   "./tests/data/1CSE-9.cool"],
                                  chromnames=['chr1'],
                                  bin_size=-1,
                                  h=3,
                                  max_bins=50)
    scores = scores[0]
    real_scores = -0.05866464993050103
    assert scores[0] == "1CSE-6.cool"
    assert scores[1] == "1CSE-9.cool"
    assert str(scores[2][0])[:6] == str(real_scores)[:6]


def test_run_between_multiple_files():
    test_folder = "./tests/data"
    files = os.listdir(test_folder)
    folderpath = test_folder
    filepathes = [os.path.join(folderpath, file) for file in files]
    scores = run_between_multiple_files(filepathes,
                                        chromnames=['chr1'],
                                        bin_size=-1,
                                        h=3,
                                        max_bins=50)
    scores = [score[2][0] for score in scores]
    with open('./tests/test_cpu_single/results_folder.txt', 'r') as f:
        for i, line in enumerate(f):
            score = line[:-1]
            assert str(scores[i])[:6] == str(score)[:6]
