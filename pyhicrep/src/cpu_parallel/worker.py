import cooler
import numpy as np
import multiprocessing as mp
from ..core.calc_scc import calc_scc
from ..core.mean_smooth import mean_filter_upper_ndiag
from typing import NoReturn


def calc_scc_onevsall_worker(pid: int,
                             queue_input: mp.Queue,
                             queue_output: mp.Queue,
                             chromnames: list,
                             max_bins: int,
                             h: int) -> NoReturn:
    while True:
        input_data = queue_input.get()
        if len(input_data) == 1 and input_data[0] == 'stop':
            return
        assert len(input_data) == 2, (
            "incomprehensible data, should be '[path1, [path2, path3, ...]]'")
        selected_hic, for_comparison_hics = input_data

        selected_file = selected_hic.split('/')[-1]
        clr1 = cooler.Cooler(selected_hic)
        mtx1 = clr1.matrix(balance=False, sparse=True)

        for comparison_path in for_comparison_hics:
            for_comparison_file = comparison_path.split('/')[-1]
            clr2 = cooler.Cooler(comparison_path)
            mtx2 = clr2.matrix(balance=False, sparse=True)

            scores = []
            # TODO: optimize - overkill by recomputation hic1
            # solution is precompute hic1
            for chrom in chromnames:
                hic1 = mtx1.fetch(chrom)
                hic2 = mtx2.fetch(chrom)

                # hic1 = meanFilterSparse(hic1, h=h)
                # hic2 = meanFilterSparse(hic2, h=h)
                # scores.append(calc_scc(hic1, hic2, max_bins))

                hic1_smoothed = np.zeros(hic1.shape, dtype=float)
                hic2_smoothed = np.zeros(hic2.shape, dtype=float)
                mean_filter_upper_ndiag(hic1.A, hic1_smoothed,
                                        h=h, max_bins=max_bins)
                mean_filter_upper_ndiag(hic2.A, hic2_smoothed,
                                        h=h, max_bins=max_bins)

                score = calc_scc(hic1_smoothed, hic2_smoothed,
                                 max_bins=max_bins)
                scores.append(score)
            scores = np.array(scores)
            queue_output.put([pid, 'step', [selected_file,
                                            for_comparison_file,
                                            scores]])
        queue_output.put([pid, 'end', []])
