#!/usr/bin/envs python
#THis is a script which unables to download the available genomes in ftp ncbi server of bacterial genomes (both individual and a list of bacterial species) 
import pandas as pd
from ftplib import FTP
import urllib.request
import subprocess
from subprocess import Popen, PIPE
import argparse
from pathlib import Path

def ftp_download(file_name):
    ftp=FTP('ftp.ncbi.nlm.nih.gov')
    ftp.login() #by default is annoymous username and password
    ftp.cwd('/genomes/refseq/bacteria/')
    download_file=open(file_name,'wb')
    ftp.retrbinary('RETR '+file_name,download_file.write,1024)
    ftp.quit()

def extracting_ftp_url(assembly_summary,taxid,status):
    genome=assembly_summary.loc[assembly_summary["species_taxid"]==str(taxid)]
    extracted_genome=genome.loc[genome["assembly_level"]==str(status)]
    for index,row in extracted_genome.iterrows():
        name=row['# assembly_accession']+"_"+row['asm_name']+"_genomic.fna.gz"
        urllib.request.urlretrieve(row['ftp_path']+"/"+name,row['# assembly_accession']+".gz")
    return extracted_genome

def genome_process(genome,scheme):
    sequence_type=[]
    for index,row in genome.iterrows():
        print (row['ftp_path'],row['# assembly_accession']+".fa")
        name=row['# assembly_accession']+"_"+row['asm_name']+"_genomic.fna.gz"
        urllib.request.urlretrieve(row['ftp_path']+"/"+name,row['# assembly_accession']+".gz")
        cmd =['/home/skt/Softwares/mlst/bin/mlst', '--scheme', scheme, row['# assembly_accession']+".gz"]
        out=subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        output = out.communicate()[0].decode("utf-8")
        output.split("\t")[2]
        ST=list(output.split("\t")[2])
        ST="".join(ST)
        sequence_type.append(ST)
    return sequence_type

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description='Downloading genomes sequence from refseq ncbi and Sequence type detection')
    parser.add_argument( '-f', '--assembly_report', type = str, default="assembly_summary.txt", help = 'ftp://ftp.ncbi.nlm.nih.gov/genomes/refseq/bacteria/assembly_summary.txt')
    parser.add_argument( '-t', '--taxid', type = str, required = True, help = 'Single or list of taxonomic id of the bacterial species eg: 562,199,..,n')
    parser.add_argument( '-g', '--genome_status', type = str, help = 'Either one of the option or as list [Complete Genome,Chromosome,Scaffold,Contig]')
    parser.add_argument( '-download', action='store_true',help = 'Only download the genomes specified genomes sequence')
    parser.add_argument( '-mlst', action='store_true', help = 'Performing sequence typing using mlst tool developed by Torsten Seemann')
    args = parser.parse_args()

#microbes_taxid=['562']
#assembly_status=['Chromosome','Complete Genome']
if Path(args.assembly_report).is_file():
    print ("File exist!!!")
else:
    print ("Downloading the file from ftp ncbi!!!")
    ftp_download(args.assembly_report) #Function for downloading the assembly_summary.txt file from the ftp ncbi

microbes_taxid=[i for i in args.taxid.split(',')]
assembly_status=[j for j in args.genome_status.split(',')]

assembly_summary=pd.read_table(args.assembly_report, header=1,low_memory=False,sep="\t",error_bad_lines=False)

for id in microbes_taxid:
    genomes_metadata=pd.DataFrame()
    df=pd.DataFrame()
    for ss in assembly_status:
        print (id+"\t"+ss)
        genomes_metadata=extracting_ftp_url(assembly_summary,int(id),ss) #for extracting the ftp url for the genomes
