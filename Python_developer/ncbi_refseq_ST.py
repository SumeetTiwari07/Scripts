import pandas as pd
from ftplib import FTP
import urllib.request
import subprocess
from subprocess import Popen, PIPE

def ftp_download(file_name):
    ftp=FTP('ftp.ncbi.nlm.nih.gov')
    ftp.login() #by default is annoymous username and password
    ftp.cwd('/genomes/refseq/bacteria/')
    download_file=open(file_name,'wb')
    ftp.retrbinary('RETR '+file_name,download_file.write,1024)
    ftp.quit()

def extracting_ftp_url(file_name,taxid,status):
    assembly_summary=pd.read_table(file_name, header=1,low_memory=False,sep="\t")
    assembly_summary.head()
    list(assembly_summary.columns)
    #assembly_summary["# assembly_accession"][1]
    E_coli=assembly_summary.loc[assembly_summary["species_taxid"]==taxid]
    E_coli.loc[23872]
    E_coli_complete_genome=E_coli.loc[E_coli["assembly_level"]==status]
#    E_coli_complete_genome["ftp_path"][23872]
    return E_coli_complete_genome

def genome_process(genome,scheme):
    sequence_type=[]
    for index,row in genome.iterrows():
        print (row['ftp_path'],row['# assembly_accession']+".fa")
        name=row['# assembly_accession']+"_"+row['asm_name']+"_genomic.fna.gz"
        urllib.request.urlretrieve(row['ftp_path']+"/"+name,row['# assembly_accession']+".gz")
        cmd =['/home/skt/Softwares/mlst/bin/mlst', '--scheme', scheme, row['# assembly_accession']+".gz"]
        out=subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        output = out.communicate()[0].decode("utf-8")
        #out_status = out.wait()
        output.split("\t")[2]
        ST=list(output.split("\t")[2])
        ST="".join(ST)
        sequence_type.append(ST)
    return sequence_type


file_name='assembly_summary.txt' #file to download
taxid=562
status="Complete Genome"
scheme="ecoli"
ftp_download(file_name) #Function for downloading the assembly_summary.txt file from the ftp ncbi
complete_genome=extracting_ftp_url(file_name,taxid,status) #for extracting the ftp url for the genomes
complete_genome=complete_genome.reset_index()#x=complete_genome.head(4) This for reseting the index otherwise i have to pass exact index value to convatenate the STs
seq_type=genome_process(complete_genome,scheme)
complete_genome['STs']=seq_type
complete_genome.to_csv("Refseq_E_coli_ST.csv",index=False)
