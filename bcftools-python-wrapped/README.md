# BCFtools Python Wrapper for Rare Variant Analysis

## Overview

This repository contains a Python script that identifies rare variants in a VCF file using BCFtools. The script processes VCF files to find variants with a gnomAD population allele frequency of less than 0.01.

## Files structure
- script.py: Main Python script for variant analysis
- NA12878.chr21.slice.vcf.gz: Input sample VCF file
- gnomad.chr21.slice.vcf.gz: Reference gnomAD VCF file with population frequencies
  - Generated files:
    - NA12878.chr21.slice.norm.vcf.gz: Normalized VCF
    - NA12878.chr21.slice.annotated.vcf.gz: Annotated VCF with gnomAD frequencies
    - NA12878.chr21.slice.filtered.vcf.gz: Filtered VCF containing rare variants
    - rare_variants_with_AF.txt: Output file listing rare variants with their frequencies

## Dependencies
Python 3.x 

BCFtools

## Pipeline Steps
1. Normalization: Splits multi-allelic sites into separate records
2. Indexing: Creates indices for VCF files
3. Annotation: Adds gnomAD allele frequencies to the sample VCF
4. Filtering: Identifies variants with AF < 0.01
5. Analysis: Counts and lists rare variants

## Output
The script generates:
- A filtered VCF file (*.filtered.vcf.gz) containing rare variants
- A text file (rare_variants_with_AF.txt) listing:
    - Chromosome
    - Position
    - Reference allele
    - Alternative allele
    - Allele frequency

