# Snakemake Pipeline for Rare Variant Analysis


![image](https://github.com/user-attachments/assets/28aa8555-03d5-46c8-8305-6ae0b61d5973)

## Pipeline Overview
This Snakemake workflow processes VCF files to identify rare variants through multiple steps:
1. Indexing: Creates indices for input VCF files
2. Normalization: Splits multi-allelic sites
3. Annotation: Adds gnomAD allele frequencies
4. Filtering: Identifies variants with AF < 0.01
5. Output Generation: Creates final rare variants list

## Rules Description
- all: Defines final output files
- index_raw_vcf: Creates indices for input VCF files
- normalize_vcf: Splits multi-allelic sites
- index_normalized_vcf: Creates indices for normalized files
- index_gnomad_vcf: Creates index for gnomAD reference file
- annotate_vcf: Adds gnomAD allele frequencies
- index_annotated_vcf: Creates indices for annotated files
- filter_variants: Filters variants below threshold
- generate_rare_variants: Creates final output file

## Configuration

The config.yaml file serves as the central configuration file for the Snakemake pipeline, containing essential parameters and settings:

## Parameters

### Threshold Setting
- Sets the allele frequency threshold to 0.01 for identifying rare variants
### Sample Information
- Lists the sample to be processed: NA12878.chr21.slice (without file extension)
### File Paths
- Specifies the gnomAD reference VCF file location: gnomAD_file/gnomad.chr21.slice.vcf.gz
### Directory Structure
- raw_dir: Defines the input directory as "raw" where raw VCF files are stored
- output_dir: Specifies "results" as the directory for storing pipeline outputs

This configuration file allows users to easily modify key parameters without changing the pipeline code, making the workflow more flexible and maintainable.

## Output Files

### Annotated Directory:
- Normalized VCF files (*.normalized.vcf.gz)
- Annotated VCF files with gnomAD frequencies (*.annotated.vcf.gz)
### Filtered Directory:
- Filtered VCF files containing rare variants (*.filtered.vcf.gz)
- Tab-separated text files listing rare variants with their frequencies (*.rare_variants_with_AF.txt)
### Resource Management
Each rule includes specifications for:
- Thread allocation
- Memory requirements
- Input/output handling


