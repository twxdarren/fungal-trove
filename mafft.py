#!/usr/bin/env python3
""#!/usr/bin/env python3
"""
18S rRNA Multiple Sequence Alignment with Merge Step
-------------------------------------
This script:
1. Merges individual 18S FASTA files from a directory into one multi-FASTA.
2. Aligns the combined multi-FASTA using MAFFT.

Dependencies: mafft
Author: Darren Ten
"""

import logging
import subprocess
from pathlib import Path

# Logging Configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# User Configuration
INPUT_DIR = Path("/path/to/fungal_18s_sequences")  # Directory containing *_18S.fasta files
COMBINED_FASTA = Path("/path/to/all_18s.fasta")    # Path for merged FASTA
ALIGNED_FASTA = Path("/path/to/aligned_18s.fasta")  # Path for MAFFT output


def merge_fastas(input_dir: Path, combined_fasta: Path) -> None:
    """
    Merges all *_18S.fasta files in input_dir into combined_fasta.
    """
    if not input_dir.exists() or not any(input_dir.glob("*_18S.fasta")):
        logging.error(f"No FASTA files found in {input_dir}")
        return

    combined_fasta.parent.mkdir(parents=True, exist_ok=True)
    with combined_fasta.open("w") as out_fd:
        for fasta in sorted(input_dir.glob("*_18S.fasta")):
            logging.info(f"Adding {fasta.name} to {combined_fasta.name}")
            with fasta.open() as in_fd:
                out_fd.write(in_fd.read())
    logging.info(f"Merged FASTA files to {combined_fasta}")


def run_mafft(input_fasta: Path, output_fasta: Path) -> None:
    """
    Runs MAFFT to align input_fasta, writing the alignment to output_fasta.

    Raises:
        subprocess.CalledProcessError if MAFFT fails.
    """
    cmd = ["mafft", "--auto", str(input_fasta)]
    with output_fasta.open("w") as out_fd:
        subprocess.run(cmd, stdout=out_fd, check=True)
    logging.info(f"MAFFT alignment written to {output_fasta}")


def main() -> None:
    # Merge individual FASTAs
    merge_fastas(INPUT_DIR, COMBINED_FASTA)

    # Check combined file exists
    if not COMBINED_FASTA.exists():
        logging.error(f"Combined FASTA not found: {COMBINED_FASTA}")
        return

    # Ensure output directory exists
    ALIGNED_FASTA.parent.mkdir(parents=True, exist_ok=True)

    # Run alignment
    try:
        run_mafft(COMBINED_FASTA, ALIGNED_FASTA)
        logging.info("Alignment complete.")
    except subprocess.CalledProcessError as e:
        logging.error(f"MAFFT failed: {e}")


if __name__ == "__main__":
    main()