# Probabilistic Diagnosis

Python implementation and experimental data accompanying **Probabilistic Diagnosis Strategies of Clustered Faults in Low-girth Interconnection Networks**, by Xueli Sun, Shuangxiang Kan, Jianxi Fan, Weibei Fan, and Zhenjiang Dong.

The project studies probabilistic fault diagnosis in augmented k-ary n-cube networks, denoted by AQ(n, k). It implements local node classification and a multiprocessing version that partitions the network into k subgraphs. The experiments examine parameter sensitivity, diagnosis accuracy, and sequential versus parallel execution time.

## Repository contents

All research scripts and results are under `Probabilistic-Diagnosis/`.

| File or directory | Purpose |
| --- | --- |
| `AugmentedKAryNCube.py` | Network and syndrome generation, sequential diagnosis, parallel diagnosis, and CSV export; implements the structure of Algorithm 1. |
| `evaulation_results.py` | Batch experiment runner using parameter CSV files. The original filename is preserved. |
| `get_parameters.py` | Generates parameter tables for p, beta, and gamma. |
| `parameters/` | Parameter tables used by the batch runner. |
| `parameters-paper/` | Additional archived parameter tables. |
| `evaluation/` | Stored measurements and generated plots. |
| `evaluation-original/`, `evaluation-paper-original/`, `evaluation-backup/` | Historical experiment results retained with their original directory names. |
| `get_average.py` | Appends an average row to result CSV files. |
| `RQ2-p-n.py`, `RQ2-beta-n.py`, `RQ2-gamma-n.py` | Parameter and accuracy plots related to paper RQ1/RQ2 and Figures 11-13. |
| `RQ3-1.py`, `RQ3-2.py`, `RQ3-3.py` | Timing plots and aggregate sequential/parallel performance analysis related to paper RQ3. |

## Installation

Create a Python environment and install the pinned dependencies from the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Run an experiment

Run research scripts from inside `Probabilistic-Diagnosis/`, because their data paths are relative to the working directory:

```bash
cd Probabilistic-Diagnosis
python AugmentedKAryNCube.py
```

The current entry point uses n=7, k=3, p=0.9, beta=0.1, and gamma=0.9. It runs 10 random instances and writes a result CSV under `evaluation/beta/`. Matching output files are overwritten when experiments are repeated; preserve a copy of archived measurements before regenerating them.

The model parameters describe the network dimension n, the coordinate base k, the probability p that a node is fault-free, and the syndrome generation parameters beta and gamma. Their interpretation in the paper is beta = P(sigma=0 | both nodes faulty) and gamma = P(sigma=1 | one node faulty and one node fault-free). The implementation is in `_calculate_sigma`.

## Batch experiments and plots

```bash
python evaulation_results.py
```

The batch runner currently selects `parameters/beta.csv`. Its other functions select the p and gamma parameter tables. The selected function, parameter ranges, output directory in `evaulation_test`, and plotting input paths are configured directly in the scripts.

For plots and timing summaries from the stored results:

```bash
python RQ2-p-n.py
python RQ2-beta-n.py
python RQ2-gamma-n.py
python RQ3-1.py
python RQ3-2.py
python RQ3-3.py
```

The plotting scripts contain fixed network dimensions and input paths; edit these values to select a different configuration. Several summaries read the final row of each CSV. The archived analysis CSVs include an appended average row; newly generated CSVs contain only the 10 measurements until aggregation is performed. `get_average.py` modifies its selected CSV files in place and should be run once on freshly generated results.

## Result fields and timing

Correct diagnosis ratios in exported CSV files are percentages, and times are measured in seconds. The correctness ratios are calculated from the sequential diagnosis output.

The implementation records three different parallel timings:

- `parallel_compute_time`: the interval from the earliest worker task start to the latest worker task finish.
- `parallel_process_time`: the process-pool execution interval, including process startup and communication.
- `parallel_all_time`: the full parallel diagnosis call, including subgraph preparation and result merging.

The RQ3 analysis scripts use `parallel_compute_time` for their speedup calculations. The local diagnosis routine includes a 0.001-second delay per unclassified node in both sequential and worker execution. Random instances are generated without a fixed seed, so new measurements vary with the random data, hardware, and runtime environment.
