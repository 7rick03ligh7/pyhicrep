import os
from pyhicrep.src.cpu_parallel.run_parallel import run_hicwise_parallel


def test_run_hicwise_parallel():
    test_folder = "./tests/data"
    files = os.listdir(test_folder)
    folderpath = test_folder
    filepathes = [os.path.join(folderpath, file) for file in files]
    scores = run_hicwise_parallel(filepathes,
                                  chromnames=['chr1'],
                                  bin_size=-1,
                                  h=3,
                                  max_bins=50,
                                  n_processes=4,
                                  is_pbar=False)
    scores = set([str(score[2][0])[:6] for score in scores])
    real_scores = []
    with open('./tests/test_cpu_parallel/results_folder.txt', 'r') as f:
        for i, line in enumerate(f):
            real_score = line[:-1]
            real_scores.append(str(real_score)[:6])
    real_scores = set(real_scores)
    assert len(scores.intersection(real_scores)) == len(scores)
