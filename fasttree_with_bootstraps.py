#!/usr/bin/env python3
"""
Bootstrap Trees Generation with FastTree
---------------------------------------
This script performs non-parametric bootstrap resampling and infers trees
for each replicate using FastTree, saving all outputs in Newick format.

Dependencies: biopython, fasttree
Author: Darren Ten
"""

import logging
import random
import subprocess
from pathlib import Path
from typing import List

from Bio import AlignIO, SeqIO
from Bio.Align import MultipleSeqAlignment

# Logging Configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# User Configuration
INPUT_FASTA = Path("/path/to/aligned_18s.fasta")
OUTPUT_DIR = Path("/path/to/bootstrap_trees")
NUM_REPLICATES = 100
FASTTREE_CMD = "FastTree"  # or full path to the FastTree executable


def generate_bootstrap_alignment(
    alignment: MultipleSeqAlignment
) -> MultipleSeqAlignment:
    """
    Creates a bootstrap replicate by sampling columns with replacement.

    Returns:
        A new MultipleSeqAlignment of the same dimensions.
    """
    num_cols = alignment.get_alignment_length()
    indices = [random.randint(0, num_cols - 1) for _ in range(num_cols)]
    bootstrap = MultipleSeqAlignment([rec[:0] for rec in alignment])

    for rec in alignment:
        seq = "".join(rec.seq[i] for i in indices)
        new_rec = rec[:]
        new_rec.seq = seq
        bootstrap.append(new_rec)

    return bootstrap


def run_fasttree(input_fasta: Path, output_nwk: Path) -> None:
    """
    Runs FastTree on the given FASTA and writes a Newick tree.

    Raises:
        subprocess.CalledProcessError if FastTree fails.
    """
    cmd = [FASTTREE_CMD, "-nt", "-gtr", "-gamma", str(input_fasta)]
    with output_nwk.open("w") as out_fd:
        subprocess.run(cmd, stdout=out_fd, check=True)
    logging.info(f"FastTree output written to {output_nwk.name}")


def main() -> None:
    """
    Main workflow: loads the alignment, generates bootstrap replicates,
    and infers trees for each replicate.
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if not INPUT_FASTA.exists():
        logging.error(f"Input alignment not found: {INPUT_FASTA}")
        return

    alignment = AlignIO.read(INPUT_FASTA, "fasta")
    n_seq = len(alignment)
    n_col = alignment.get_alignment_length()
    logging.info(f"Loaded alignment: {n_seq} sequences × {n_col} columns")

    for i in range(1, NUM_REPLICATES + 1):
        # Generate bootstrap alignment
        bs_align = generate_bootstrap_alignment(alignment)
        bs_fasta = OUTPUT_DIR / f"replicate_{i}.fasta"
        SeqIO.write(bs_align, bs_fasta, "fasta")

        # Run FastTree on the replicate
        bs_tree = OUTPUT_DIR / f"replicate_{i}.nwk"
        try:
            run_fasttree(bs_fasta, bs_tree)
        except subprocess.CalledProcessError as e:
            logging.error(f"FastTree failed on replicate {i}: {e}")

    logging.info("All bootstrap replicates completed.")


if __name__ == "__main__":
    main()