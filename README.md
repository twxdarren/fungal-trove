# A Singapore-centric Fungal Dataset of 518 Cultivated Strains with Visual Phenotypes and Taxonomic Identity

**Journal Submission:** *Nature Scientific Data*

This repository contains the **analysis scripts** and **dataset components** associated with our Data Descriptor:

> **"A Singapore-centric Fungal Dataset of 518 Cultivated Strains with Visual Phenotypes and Taxonomic Identity"**

The project documents fungal biodiversity across terrestrial and marine environments in Singapore, combining high-resolution imaging, genomic sequencing, and deep learning-based feature extraction.

The compressed archive `singapore_518_fungi_dataset.zip` and `singapore_518_fungi_dataset_scripts.zip` have been uploaded to **Figshare**.  

_The manuscript and dataset is currently under review, and the Figshare link will be provided here upon completion of the deposition process._

## 📂 Repository Contents

### 💻 Analysis Scripts:
The following scripts were used for processing and generating the dataset:

1. **barrnap.py**  
   Prediction of 18S rRNA regions using Barrnap (v0.9).

2. **mafft.py**  
   Multiple sequence alignment of 18S sequences with MAFFT (v7.525).

3. **fasttree_with_bootstraps.py**  
   Phylogenetic inference with FastTree (100 bootstraps).

4. **consensus_tree.r**  
   Majority-rule consensus tree construction.

5. **resnet50.py**  
   Extraction of high-dimensional image embeddings using a pre-trained ResNet-50 convolutional neural network.

### 🍄 Dataset Components (Uploaded on figshare, refer to `singapore-518-fungi-dataset-components` for download information):
The compressed archive `singapore_518_fungi_dataset.zip` can be found on figshare, which includes:

- `fungal_18s_sequences/`  
  Predicted 18S rRNA sequences in FASTA format.

- `fungal_preharvest_resnet50_embeddings/`  
  ResNet-50-derived feature embeddings for pre-harvest colony images (PyTorch tensors).

- `fungal_timepoint_images/`  
  High-resolution images of fungal colonies captured across key developmental milestones.


## 💡 Contact
For questions or collaborations, please contact:  
[Darren Ten]  
[Institute of Sustainability for Chemicals, Energy and Environment (ISCE2), A*STAR]  
[darren_ten@isce2.a-star.edu.sg]
