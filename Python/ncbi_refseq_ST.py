import pandas as pd
from ftplib import FTP
import urllib

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
    E_coli_complete_genome=E_coli.loc[E_coli["assembly_level"]==status]
    #E_coli_complete_genome["ftp_path"][23872]
def genome_process(complete_genome):
    for index,row in complete_genome.iterrows():
        urllib.urlretrieve(row['ftp_path'],row['# assembly_accession'])
        


file_name='assembly_summary.txt' #file to download
taxid=562
status="Complete genome"
ftp_download(file_name) #Function for downloading the assembly_summary.txt file from the ftp ncbi
extracting_ftp_url(file_name,taxid,status) #for extracting the ftp url for the genomes
genome_process(E_coli_complete_genome)
