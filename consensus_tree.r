#!/usr/bin/env Rscript

# consensus_tree.R
# ---------------------------
# Loads Newick bootstrap trees and generates a majority-rule
# consensus tree (50% threshold).
#
# Dependencies: ape
# Author: Darren Ten


# User Configuration
tree_dir    <- "/path/to/bootstrap_trees"            # directory with .nwk files
output_tree <- file.path(tree_dir, "consensus.nwk")  # output consensus tree

# Load Libraries
suppressPackageStartupMessages(library(ape))

# Find and Read Trees
tree_files <- list.files(tree_dir, pattern="\\.nwk$", full.names=TRUE)
if (length(tree_files) == 0) {
  stop("No .nwk files found in ", tree_dir)
}
trees <- lapply(tree_files, read.tree)

# Compute Consensus
cons_tree <- consensus(trees, p=0.5)

# Save Output
write.tree(cons_tree, file=output_tree)
cat("Consensus tree saved to:", output_tree, "\n")