#!/usr/bin/env python3

import subprocess  #A module for running external commands and creating new processes.
import sys         #Provides access to system-specific parameters and functions.
import os          #Offers tools that provides a consistent interface across different operating systems

#Defining a function called run_command, function will run a shell command and handle any errors
def run_command(cmd, description):
    print(description)
    try: #try block attempts to execute the shell command
        result = subprocess.run( 
            cmd,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e: #except block handles any errors that occurs
        print(f"Error during: {description}", file=sys.stderr)
        print(f"Command: {cmd}", file=sys.stderr)
        print(f"Return Code: {e.returncode}", file=sys.stderr)
        print(f"Error Output: {e.stderr}", file=sys.stderr)
        sys.exit(e.returncode)

#Defining a function called normalize_vcf to normalize the VCF file by splitting multi-allelic sites
def normalize_vcf(input_vcf, output_vcf):
    norm_cmd = (
        f"bcftools norm -m -any "
        f"-O z -o {output_vcf} {input_vcf}"
    )
    run_command(norm_cmd, f"Normalizing VCF: {input_vcf} -> {output_vcf}")

#Defining a function called build_index to build indexes for required VCF files
def build_index(vcf_file):
    run_command(f"bcftools index {vcf_file}", f"Indexing {vcf_file}")

#Defining a function called annotate_vcf to annotate VCF file with allele frequencies from gnomAD VCF file
def annotate_vcf(input_vcf, annotation_vcf, output_vcf):
    annotate_cmd = (
        f"bcftools annotate "
        f"-a {annotation_vcf} "
        f"-c CHROM,POS,REF,ALT,INFO/AF "
        f"-O z "
        f"-o {output_vcf} "
        f"{input_vcf}"
    )
    run_command(annotate_cmd, f"Annotating VCF: {input_vcf} with {annotation_vcf} -> {output_vcf}")

#Defining a function called filter_variants to filter variants based on allele frequency threshold
def filter_variants(input_vcf, output_vcf, threshold): 
    filter_cmd = (
        f"bcftools view "
        f"-i 'MIN(INFO/AF[*]) < {threshold} || INFO/AF=\".\"' "
        f"-O z "
        f"-o {output_vcf} "
        f"{input_vcf}"
    )
    run_command(filter_cmd, f"Filtering variants with AF < {threshold} or missing AF -> {output_vcf}")

#Defining a function called count_variants to count the number of variants in a VCF file
def count_variants(vcf_file): 
    count_cmd = f"bcftools query -f '%CHROM\\t%POS\\t%REF\\t%ALT\\n' {vcf_file} | wc -l"
    rare_count = run_command(count_cmd, f"Counting the number of rare variants in {vcf_file}")
    try:
        return int(rare_count)
    except ValueError:
        print(f"Unexpected output while counting variants: {rare_count}", file=sys.stderr)
        sys.exit(1)

#Defining a function called list_variants_with_af to list rare variants
def list_variants_with_af(vcf_file, output_file, threshold):
    #Defining the header
    header = "CHROM\tPOS\tREF\tALT\tAF"

    #Writing the header to the output file
    with open(output_file, "w") as f:
        f.write(header + "\n")

    #Appending the query results to the output file
    list_cmd = (
        f"bcftools query -f '%CHROM\\t%POS\\t%REF\\t%ALT\\t%INFO/AF\\n' {vcf_file} >> {output_file}"
    )
    run_command(list_cmd, f"Listing rare variants with AF values -> {output_file}")

#The main() function manages the workflow for processing a VCF file, 
#including normalization, annotation, filtering, and variant analysis.
def main():
    #Defining input and output file paths
    original_vcf = "NA12878.chr21.slice.vcf.gz"
    normalized_vcf = "NA12878.chr21.slice.norm.vcf.gz"
    gnomad_vcf = "gnomad.chr21.slice.vcf.gz"
    annotated_vcf = "NA12878.chr21.slice.annotated.vcf.gz"
    filtered_vcf = "NA12878.chr21.slice.filtered.vcf.gz"
    output_file = "rare_variants_with_AF.txt"
    threshold = 0.01

    #Ensuring the required input files exist before proceeding
    for file in [original_vcf, gnomad_vcf]:
        if not os.path.isfile(file):
            print(f"Input file not found: {file}", file=sys.stderr)
            sys.exit(1)

    #Step 1: Normalizing the Sample VCF
    normalize_vcf(original_vcf, normalized_vcf)

    #Step 2: Indexing the Normalized Sample VCF
    build_index(normalized_vcf)

    #Step 3: Indexing the Annotation VCF (Assuming no index exists)
    build_index(gnomad_vcf)

    #Step 4: Annotating normalized VCF file with allele frequencies from gnomAD VCF file
    annotate_vcf(normalized_vcf, gnomad_vcf, annotated_vcf)

    #Step 5: Indexing the Annotated VCF
    build_index(annotated_vcf)

    #Step 6: Filtering Variants Based on gnomAD AF < threshold or AF Missing
    filter_variants(annotated_vcf, filtered_vcf, threshold)

    #Step 7: Indexing the Filtered VCF
    build_index(filtered_vcf)

    #Step 8: Counting the Number of Rare Variants
    rare_count = count_variants(filtered_vcf)
    print(f"Total number of rare variants (AF < {threshold}): {rare_count}")

    #Step 9: Listing the Rare Variants with AF Values
    list_variants_with_af(filtered_vcf, output_file, threshold)
    print(f"Rare variants with AF < {threshold} saved in: {output_file}")

    #Displaying the output file contents
    if os.path.isfile(output_file):
        print("\nRare variants list with AF:")
        with open(output_file, 'r') as f:
            print(f.read())

if __name__ == "__main__":
    main()