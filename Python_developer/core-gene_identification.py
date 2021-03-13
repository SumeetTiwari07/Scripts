#!/usr/bin/env python

#This will identify the core-genes by mapping reads to a reference genome.
#Core gene is defined as a gene which is present in 99% of the strain collection.

import pandas as pd
import argparse
import subprocess
import os
import math

def bwa_indexing(ref,loc,gff_in):
    reference="/".join([loc,"ref_seq"])
    os.mkdir(reference)
    #Converting gff to bed format
    #Converting bed file to SAF file required for readocunt by featurecount
    #Indexing the reference
    gff_2_bed=" ".join(["gff2bed","<",gff_in,">",reference+"/reference.bed"])
    os.system(gff_2_bed)
    bwa_index=subprocess.Popen(['bwa', 'index', ref, '-p', reference+"/reference"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = bwa_index.communicate()
    bed_2_saf=pd.read_table(reference+"/reference.bed",header=None,sep="\t")
    bed_2_saf=bed_2_saf.drop(columns=[4,6,7,8,9])
    bed_2_saf=bed_2_saf[[3,0,1,2,5]]
    bed_2_saf.to_csv(reference+"/reference.saf",index=False,header=False,sep="\t")
    return()

def bwa_mapping(reads,loc):
    ref_index="/".join([loc, "ref_seq", "reference"])
    for index, rows in reads.iterrows():
        path_strains_dir="/".join([loc, str(rows["id"])])
        os.mkdir(path_strains_dir)
        out=path_strains_dir+"/"+str(rows["id"])
        bwa_mem=subprocess.Popen(["bwa", "mem","-t","10", ref_index, rows["R1"], rows["R2"]],stdout=subprocess.PIPE)
        bam_to_sam=subprocess.Popen(['samtools','view','-bS','-o',out+".bam", '-'], stdin=bwa_mem.stdout, stdout=subprocess.PIPE)
        bam_to_sam.communicate()
    return()

def samtools(id,loc):
    bed_file="/".join([loc,"ref_seq","reference.bed"])
    input_path="/".join([loc, str(id), str(id)])
    subprocess.run(["samtools", "sort", input_path+".bam", "-o",input_path+"_sorted.bam"])
    subprocess.run(["samtools", "index", input_path+"_sorted.bam"])
    bed_coverage=" ".join(["bedtools", "coverage", "-a", bed_file, "-b", input_path+"_sorted.bam", ">", input_path+".coverage"])
    os.system(bed_coverage)
    #Counting number of reads mapped to individual regions
    #Taking into account of a read mapped to muliple regions or multioverlapping reads
    subprocess.run(["featureCounts", "-a", loc+"/ref_seq/reference.saf", "-F", "SAF", "-M", "-O","--donotsort", "-o",input_path+"_read.count", input_path+"_sorted.bam"])
    #Bedtools for Calculating the Proportion of the gene covered by the mapped reads
    return()

def genes_pres_abs(id,loc,minreads,cov):
    input_path="/".join([loc, str(id), str(id)])
    strain_id=str(id)+"_sorted.bam"
    n_reads=pd.read_table(input_path+"_read.count",header=1)
    #n_reads=n_reads.loc[n_reads[strain_id]>=minreads].reset_index().drop(columns=["index","Length","Strand"],axis=1)
    n_reads=n_reads.loc[n_reads[input_path+"_sorted.bam"]>=minreads]["Geneid"].reset_index().drop(columns=["index"])
    n_reads=n_reads.loc[n_reads["Geneid"]!="."].reset_index().drop(columns=["index"])
    #Filtering the regions based on proportion of region covered by the reads.
    coverage_filter=pd.read_table(input_path+".coverage",header=None)
    coverage_filter=coverage_filter.loc[coverage_filter[13] >= cov][3].reset_index().drop(columns=["index"])
    coverage_filter=coverage_filter.rename(columns={3:"Geneid"})
    coverage_filter=coverage_filter.loc[coverage_filter["Geneid"]!="."].reset_index().drop(columns=["index"])
    strains_genes=pd.merge(n_reads, coverage_filter, how='inner') # Genes presence based on coverage and detpth of the reads.
    strains_genes.to_csv(loc+"/"+"gene_presence"+"/"+str(id)+"_genes_pres.csv",index=False,header=True)
    return()


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description='creating core-gene snps file using mapping approach')
    parser.add_argument( '-ref', '--reference', type = str, required = True, help = 'Path to reference file in fasta format *.fasta or *.fa')
    parser.add_argument( '-i', '--input_file', type = str, required = True, help = 'Tab-delimited file with strain_id\tPath_to_read_1\tPath_to_read_2')
    parser.add_argument( '-out_dir', '--output_dir', required=True, type = str, help = 'output directory')
    parser.add_argument('-gff','--gff_ref', required=True, type=str, help='Annotation of the reference genome in gff3 format')
    parser.add_argument('-c','--cov', default=0.80, type=float, help='Proportion of a region on genome cover by mapped reads')
    parser.add_argument('-n','--min_reads',default=10, type=int, help='minimum number of reads to be mapped to a certain region')
    args = parser.parse_args()

    reads=pd.read_table(args.input_file,header=0,sep="\t")
    #Current directory full path
    #Creating essential file required through out the processing
    loc="/".join([os.getcwd(),args.output_dir]) #Full path of the current working directory
    #loc
    os.mkdir(loc) #Creating the output directory
    #Indexing the feference genome
    bwa_indexing(args.reference,loc,args.gff_ref)
    bwa_mapping(reads,loc)

    #sorting and indexing the bam file using samtools and counting the number of reads mapped to each region on the genome using featureCounts
    reads.apply(lambda r: samtools(r["id"],loc), axis=1)

    #Defining core-genes
    os.mkdir(loc+"/"+"gene_presence")
    reads.apply(lambda x: genes_pres_abs(x["id"], loc, args.min_reads, args.cov), axis=1)

    #Extracting the core-genes
    all_genes=pd.read_csv(loc+"/ref_seq/reference.bed",header=None,sep="\t")
    all_genes["Count"]=0
    all_genes=all_genes.drop(columns=[0,4,5,6,7,8,9])
    all_genes=all_genes[[3,1,2,"Count"]].rename(columns={3:"Geneid",1:"Start",2:"End"})
    all_genes=all_genes.loc[all_genes["Geneid"]!="."].reset_index().drop(columns=["index"])
    all_genes.set_index("Geneid", inplace=True)
    all_genes_dict=all_genes.to_dict('index')
    #Counting the occurence of genes in each genome
    for index, rows in reads.iterrows():
        gene_count=pd.DataFrame()
        gene_count=pd.read_table(loc+"/gene_presence/"+str(rows['id'])+"_genes_pres.csv",header=0)
        for index,rows in gene_count.iterrows():
            all_genes_dict[rows["Geneid"]]["Count"]+=1

    #Separating the core-genes from the pan-genome
    core=0.99*len(reads)
    frac, whole = math.modf(core)
    if frac >=0.5:
        core=math.ceil(core)
    else:
        core=math.floor(core)
    core

    final_core_genes={}
    for key, val in all_genes_dict.items():
        if val['Count']>=core:
            final_core_genes[key]=all_genes_dict[key]

    final=pd.DataFrame()
    final=pd.DataFrame.from_dict(final_core_genes,orient='index')
    final[['Start','End','Count']].to_csv(loc+"/result.csv")
