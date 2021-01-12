import multiprocessing as mp
from tqdm import tqdm
from typing import NoReturn
import logging

from .worker import calc_scc_onevsall_worker
from ..utils import (get_out_filepath,
                     save_to_csv,
                     save_to_txt)
from ..logger import log


@log
def run_hicwise_parallel(filepathes: list,
                         chromnames: list,
                         bin_size: int,
                         h: int,
                         max_bins: int,
                         n_processes: int
                         ) -> list:
    # Initializing
    procs = dict()
    # queues for send data to processes
    procs_queue_inputs = dict()
    # queue for get data from processes
    procs_queue_output = mp.Manager().Queue()
    pbars = dict()
    for pid in range(n_processes):
        procs_queue_inputs[pid] = mp.Manager().Queue()
        proc = mp.Process(target=calc_scc_onevsall_worker,
                          args=(pid,
                                procs_queue_inputs[pid],
                                procs_queue_output,
                                chromnames,
                                max_bins,
                                h,)
                          )
        procs[pid] = proc
        procs[pid].start()
    #

    # Start parallel calculation
    # o - the scHiC data to compare with selected scHiC (selected_hic)
    # x o o o  (selected 1, compare with 2, 3, 4)
    # x x o o  (selected 2, compare with 3, 4)
    # x x x o  (selected 3, compare with 4)
    # x x x x  (not computation)
    #

    # Parallel start
    # all workers are free at the initial
    workers_free_pid = [i for i in range(n_processes)]
    # index of selected hic data
    selected = 0
    # list of calculated scc
    all_scores = []
    # counter of computed hic data (one vs all)
    processed = 0
    while processed < len(filepathes):
        if workers_free_pid:
            # TODO: strange condition below (this condition needed
            # because in the LAST batch hic INDEX
            # already OUT OF BOUND but hics still not processed.
            # So algorithm try to find work for workers)
            if selected < len(filepathes):
                for pid in workers_free_pid:
                    selected_hic = filepathes[selected]
                    for_comparison_hics = filepathes[selected+1:]
                    pbars[pid] = tqdm(total=len(for_comparison_hics),
                                      desc=f'Process {pid}',
                                      leave=False,
                                      position=pid)
                    procs_queue_inputs[pid].put([selected_hic,
                                                 for_comparison_hics])
                    selected += 1
                workers_free_pid = []
        pid, status, output_data = procs_queue_output.get()
        if status == 'step':
            pbars[pid].update(1)
            all_scores.append(output_data)
        if status == 'end':
            workers_free_pid = [pid]
            processed += 1

    # Close all processes
    for pid in range(n_processes):
        procs_queue_inputs[pid].put(['stop'])
        pbars[pid].close()
        procs[pid].join()
    #
    return all_scores


@log
def run_parallel(filepathes: list,
                 max_bins: int,
                 h: int,
                 chromnames: list,
                 out_file="",
                 result_folder="",
                 bin_size=-1,
                 to_csv=False,
                 n_processes=4,
                 is_hicwise=True
                 ) -> NoReturn:

    if is_hicwise:
        all_scores = run_hicwise_parallel(filepathes,
                                          chromnames=chromnames,
                                          bin_size=bin_size,
                                          h=h,
                                          max_bins=max_bins,
                                          n_processes=n_processes)
    else:
        raise("the chromosome-wise parallel calculation doesn't realize yet")

    # Calculate filepath
    filepath = get_out_filepath(out_file=out_file,
                                result_folder=result_folder)

    # Saving to txt
    save_to_txt(filepath, chromnames=chromnames, all_scores=all_scores)
    logging.info(f"txt result saved in {filepath}")

    # Saving to csv
    if to_csv:
        filenames = [path.split('/')[-1] for path in filepathes]
        save_to_csv(filepath,
                    chromnames=chromnames,
                    indexnames=filenames)
        logging.info(f"csv result saved in {filepath}")
