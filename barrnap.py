#!/usr/bin/env python3
"""
Barrnap rRNA Extraction
--------------------------------
This script:
1. Loads scaffold FASTA files.
2. Runs Barrnap for rRNA prediction.
3. Extracts rRNA regions via Bedtools.
4. Saves the longest 18S region per sample.
5. Compiles a summary CSV of longest 18S lengths.

Dependencies: barrnap, bedtools, biopython
Author: Darren Ten
"""

import csv
import logging
import subprocess
from pathlib import Path

from Bio import SeqIO


# Logging Configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


# User Configuration
INPUT_DIR = Path("/path/to/scaffolds")
OUTPUT_DIR = Path("/path/to/barrnap_results")
BARRNAP_CMD = "barrnap"  # or full path to the executable

SAMPLE_IDS = [
    # "Sample1",
    # "Sample2",
    # ...
]


def run_barrnap(input_fasta: Path, output_gff: Path, log_file: Path) -> None:
    """
    Runs Barrnap to predict rRNA genes and writes GFF output.

    Raises:
        subprocess.CalledProcessError if Barrnap fails.
    """
    cmd = [
        BARRNAP_CMD,
        "--kingdom", "euk",
        str(input_fasta)
    ]
    with output_gff.open("w") as gff_out, log_file.open("w") as log_out:
        subprocess.run(cmd, stdout=gff_out, stderr=log_out, check=True)
    logging.info(f"Barrnap completed for {input_fasta.name}")


def extract_rrna_regions(input_fasta: Path, gff_file: Path, output_fasta: Path) -> None:
    """
    Extracts rRNA sequences using Bedtools getfasta.

    Raises:
        subprocess.CalledProcessError if Bedtools fails.
    """
    cmd = [
        "bedtools", "getfasta",
        "-fi", str(input_fasta),
        "-bed", str(gff_file),
        "-fo", str(output_fasta)
    ]
    subprocess.run(cmd, check=True)
    logging.info(f"rRNA sequences extracted to {output_fasta.name}")


def extract_longest_18s(rrna_fasta: Path, output_fasta: Path) -> int:
    """
    Selects and writes the longest 18S sequence from rrna_fasta.

    Returns:
        Length of the longest 18S sequence, or 0 if none found.
    """
    longest_record = None
    for record in SeqIO.parse(rrna_fasta, "fasta"):
        if "18S" not in record.description:
            continue
        if not longest_record or len(record.seq) > len(longest_record.seq):
            longest_record = record

    if longest_record:
        SeqIO.write(longest_record, output_fasta, "fasta")
        logging.info(f"Longest 18S for {rrna_fasta.stem}: {len(longest_record.seq)} bp")
        return len(longest_record.seq)

    logging.warning(f"No 18S sequences found in {rrna_fasta.name}")
    return 0


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    summary_csv = OUTPUT_DIR / "summary_18S_extraction.csv"

    with summary_csv.open("w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["SampleID", "Longest18S_Length"])

        for sample_id in SAMPLE_IDS:
            fasta_in = INPUT_DIR / f"{sample_id}_scaffolds.fasta"
            if not fasta_in.exists():
                logging.warning(f"Input file not found: {fasta_in}")
                continue

            gff_out = OUTPUT_DIR / f"{sample_id}_rrna.gff"
            log_out = OUTPUT_DIR / f"{sample_id}_barrnap.log"
            rrna_fa = OUTPUT_DIR / f"{sample_id}_rrna.fasta"
            fa18_out = OUTPUT_DIR / f"{sample_id}_18S.fasta"

            try:
                run_barrnap(fasta_in, gff_out, log_out)
                extract_rrna_regions(fasta_in, gff_out, rrna_fa)
                length = extract_longest_18s(rrna_fa, fa18_out)
            except subprocess.CalledProcessError as e:
                logging.error(f"Error processing {sample_id}: {e}")
                length = 0

            writer.writerow([sample_id, length])

    logging.info(f"All samples processed. Summary written to {summary_csv}")


if __name__ == "__main__":
    main()