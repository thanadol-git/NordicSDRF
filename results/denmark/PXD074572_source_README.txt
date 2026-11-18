Ligand‑Resolved In Vivo Phosphoproteomics of the Adult Heart Maps ErbB Signaling by EGF and NRG1β

## Overview
This dataset contains the following mass-spectrometry-based data:
- Phosphoproteome: mouse heart tissue collected 10 min after injection of EGF or NRG1β
- IP of EGFR: mouse heart tissue collected 10 min after injection of EGF
The aim of the study was to characterize phosphorylation signaling events after ErbB receptors activation in cardiac tissue.

## Project details

### Samples
Phosphoproteome experiment includes 32 .raw files:

	- Control group: 8 biological replicates, 2 phosphopeptide enrichment methods
	- EGF group: 4 biological replicates, 2 phosphopeptide enrichment methods
	- NRG1 group: 4 biological replicates, 2 phosphopeptide enrichment methods


IP of EGFR experiment includes 8 .d files:
	- Control group: 4 biological replicates
	- EGF group: 4 biological replicates

Description of each file name and corresponding sample names is provided in experiment_annotation files.

### Data Analysis

FragPipe (v. 22.0) search using LFQ-Phospho workflow with MBR (fragger.params file) against UniProtKB/Swiss-Prot mouse database (.fas file); global FDR 1%, class I sites.
The combined_site_STY_79.9663 was used for differential expression analysis using DEP (v. 1.26.0) and LIMMA (v. 3.60.6) R packages:
	1. Filter to retain features quantified in all samples of the treated condition group
	2. log2-transform intensities
	3. Median normalization
	4. Imputation of missing values (MVs) using a mixed imputation method. If MVs in more than 50% of samples, impute MVs using MinProb from a distribution centered near the 1st percentil of the observed intensities.

Results after pre-processing (filtering, log-2 transformation, normalization and imputation) are provided:

- Normalised_phosphopeptides_quantities_EGF : Imputed missing values of EGF stimulation dataset
- Normalised_phosphopeptides_quantities_NRG1 : Imputed missing values of NRG1 stimulation dataset

Each table contains an Index column with the UniprotID_AAsite and the quantitative values of each sample.


### File Structure
├─ raw/       # Peptide spectra data: phosphoproteome(.raw) or IP (.d)
├─ search/    # Search engine output files
|                - IP_combined_site_STY_79.9663 (.tsv) # IP
| 		 - combined_site_STY_79.9663 (.tsv) # Phosphoproteome
|─ fasta/	   # Database
|	         - 2025-02-07-decoys-reviewed-contam-UP000000589_mouse (.fas)
└─ other/     # Sample annotations
	         - IP_experiment_annotation (.tsv) # IP
	         - experiment_annotation (.tsv) # Phosphoproteome
               # Search parameter files
		 - IP_fragger (.params) # IP
	         - fragger (.params) # Phosphoproteome
	       # Phosphoproteome pre-processed files (filtered, normalized and imputed phosphopeptide quantities)
                 - Normalised_phosphopeptides_quantities_EGF (.txt)
                 - Normalised_phosphopeptides_quantities_NRG1 (.txt)
