# CMRI-Assignment: Rare Variant Identification Pipeline 

This repository contains two implementations of a pipeline to identify rare variants in a VCF file:
1. BCFtools wrapped in Python
2. A Snakemake workflow

# Project Objective
The goal of this project is to determine the number of rare variants in a sample VCF file based on population frequencies from gnomAD. Specifically, we identify variants with a gnomAD population allele frequency of less than 0.01.

# Input Files
1. NA12878.chr21.slice.vcf.gz: Sample's VCF file to be filtered for rare variants.
2. gnomad.chr21.slice.vcf.gz:  Population frequencies from gnomAD v4.1.0 in VCF format.

## Implementations

# 1. BCFtools with Python
This implementation uses BCFtools commands wrapped in a Python script. It provides a straightforward solution using common bioinformatics tools.

# Installation

`conda create --name CMRI-Assignment python=3.9 bcftools=1.10 gsl=2.5 -c bioconda -c conda-forge

conda activate CMRI-Assignment`

# Usage

`python3 script.py`

# 2. Snakemake Pipeline
This implementation uses Snakemake for workflow management, offering a more scalable and reproducible approach.

# Installation

`conda activate CMRI-Assignment

conda install -c bioconda -c conda-forge snakemake`

# Usage

snakemake --cores all

## Results

Both implementations will output the total number of rare variants and a list of the rare variants in NA12878.chr21.slice.vcf.gz that have a gnomAD population allele frequency of less than 0.01



