#import sys
import os
import argparse
import tarfile
from sh import gunzip
from shutil import copy2
from joblib import Parallel,delayed

def ariba_run(read_file,j):
 #for i in range(len(read_file)/2):
 print (read_file[j]+'\t'+read_file[j+1]+'\n')
 s1,s2,s3=read_file[j].split("_")
 s_dir="_".join([s1,s2])
 os.system("ariba run "+args.prepref+' '+read_file[j]+' '+read_file[j+1]+' '+s_dir+" --threads "+str(args.threads))
 src="/".join([os.getcwd(),s_dir,'report.tsv'])
 dst="/".join([os.getcwd(),args.outdir,s_dir+'_report.tsv'])
 copy2(src,dst)
 return;

command=["al","run"]
allowed_dbs =["argannot","card","megares","plasmidfinder","resfinder","srst2_argannot","vfdb_core","vfdb_full","virulencefinder"]

parser = argparse.ArgumentParser(prog='ariba',usage='<cmd>',description='ARIBA: Antibiotic Resistance Identification By Assembly')
subparsers = parser.add_subparsers(title='Available Commands',help='', metavar='',dest="command")

#---------------------------------------------------------getref,prepareref,run-------------------------------------------------------

subparser_al= subparsers.add_parser('al',help='It will run all the three commands of ariba i.e getref,prepareref,run.',
				         usage='ariba_wrapper.py al <db> <prefix> <prepref> <readlist> <outdir> [options]',
    					 description='Run all the three commands of ariba i.e getref,prepareref,run.')

subparser_al.add_argument('db', help='Database to download. Must be one of: '+' '.join(allowed_dbs), metavar="DB name")
subparser_al.add_argument('prefix',help='Prefix of output filenames for reference sequences and metadata',metavar='file')
subparser_al.add_argument('prepref',help='Directory for storing the processed reference',metavar='DIR')
subparser_al.add_argument('readlist', help='List of compressed forward and reversed reads')
subparser_al.add_argument('outdir', help='Output directory to keep final output')
subparser_al.add_argument('--assembler', help='Assembler to use,default: fermilite', choices=['fermilite','spades'], default='fermilite')
subparser_al.add_argument('--threads',type=int, help='Number of threads for cdhit and spades, default:%(default)s', default=1, metavar='INT')

#--------------------------------------------------------------------run----------------------------------------------------------------

subparser_run = subparsers.add_parser('run',help='It will run all the three commands of ariba i.e getref,prepareref,run.',
					    usage='ariba_wrapper.py run <prepref_dir> <readlist> <outdir> [options]',
					    description='It will executes only run command of ariba')

subparser_run.add_argument('prepref',help='Name of output directory when "ariba prepareref" was run')
subparser_run.add_argument('readlist', help='List of compressed forward and reversed reads',metavar='file')
subparser_run.add_argument('outdir', help='Output directory to keep final output')
subparser_run.add_argument('--assembler', help='Assembler to use,defauilt: fermilite', choices=['fermilite','spades'], default='fermilite')
subparser_run.add_argument('--threads', type=int, help='Number of threads for cdhit and spades, default:%(default)s', default=1, metavar='INT')

args = parser.parse_args()

##Processing the read file##
read_n=[]
read_list=open(args.readlist,'r')
reads=read_list.readlines()
reads=[s.rstrip('\n') for s in reads] #Removal of newline '\n' character from read file names
reads_sorted=sorted(reads)

print "Extracting the reads\n"

for i in reads_sorted:
 if (i.endswith(".tar.gz")):
  read_n.append(i.rstrip('.tar.gz'))
  tar = tarfile.open(i)
  tar.extractall()
  tar.close()
 elif(i.endswith(".gz")):
  read_n.append(i.rstrip('.gz'))
  gunzip(("-k"),i)
 elif(i.endswith(".fastq" or ".fq")):
  read_n.append(i)

os.mkdir(os.getcwd()+'/'+args.outdir)

if args.command == "al":
 print "-------------------------------Executing getref-->prepareref-->run---------------------------------------\n"
 print "-------------------------------Downloading the "+args.db+" database!!!--------------------------------------\n"
 os.system("ariba getref "+args.db+' '+args.prefix)
 print "-------------------------------Preparing the refernce for AMR detection!!!-----------------------------------\n"
 os.system("ariba prepareref -f "+args.prefix+".fa -m"+args.prefix+".tsv"+' '+args.prepref+" --threads "+str(args.threads))
 print "-------------------------------Antimicrobial resitance detection in the samples!!!------------------------------\n"
 Parallel(n_jobs=3)(delayed(ariba_run)(read_n,j) for j in range(0,len(read_n),2))
 os.system("ariba summary summary_all "+os.getcwd()+'/'+args.outdir+'/*_report.tsv')

if args.command == "run":
 print "----------------------------Executing only Antimicrobial resitance detection in the samples!!!----------------\n"
 Parallel(n_jobs=3)(delayed(ariba_run)(read_n,j) for j in range(0,len(read_n),2))
 os.system("ariba summary summary_all "+os.getcwd()+'/'+args.outdir+'/*_report.tsv')
