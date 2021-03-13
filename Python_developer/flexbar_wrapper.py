import os
import argparse
import tarfile
from shutil import copy2
from joblib import Parallel,delayed

def flexbar(read_file,i,cmd,out_dir):
  print read_file[i]+'\t'+read_file[i+1]+'\n'
  R1="/".join([args.readdir,read_file[i]])
  R2="/".join([args.readdir,read_file[i+1]])
 
  if cmd == "adapter":
   s_dir=read_file[i].replace(str(args.string),'')
   path="/".join([out_dir,s_dir])
   print "----------------------------Adapter Trimming mode!!!----------------\n"
   ad_cmd=" ".join(["flexbar","-r",R1,"-p",R2,"-a",args.adapters,"-t",path,"-n",str(args.n),"-ae",args.ae,"-u",str(args.u),"-m",str(args.m),"-z",args.z])
   os.system(ad_cmd)

  if cmd =="quality":
   s_dir=read_file[i].replace(str(args.string),'')
   path="/".join([out_dir,s_dir])
   print "----------------------------Quality Trimming mode!!!----------------\n"
   qc_cmd=" ".join(["flexbar","-r",R1,"-p",R2,"-t",path,"-n",str(args.n),"-q",args.q,"-u",str(args.u),"-m",str(args.m),"-qt",str(args.qt),"-qf",args.qf,"-z",args.z])
   os.system(qc_cmd)

  return;

mode=["adapter","quality"]

parser = argparse.ArgumentParser(prog='flexbar',usage='<cmd>',description='Flexbar:flexible barcode and adapter removal wrapper script')
subparsers = parser.add_subparsers(title='Available Commands',help='', metavar='',dest="mode")

#---------------------------------------------------------adapter trimming-------------------------------------------------------

subparser_adapter= subparsers.add_parser('adapter',help='Remove adapter seqeunce from the paired-end reads',
				         usage='flexbar_wrapper.py adapter <readdir> <file> <outdir> [options]',
    					 description='It will remove the adapter from anywhere in the reads')

subparser_adapter.add_argument('readdir', help='Directory containing the forward and reverse reads in .fastq,.gz,.bz2', metavar="readdir")
subparser_adapter.add_argument('adapters',help='List of adater sequences in fasta format .fa or .fasta',metavar='file')
subparser_adapter.add_argument('outdir',help='Directory to save adapter trimmed reads',metavar='outdir')
subparser_adapter.add_argument('-string',help='End of the read file name eg. _R1_001.fastq.gz or _1.fastq.gz or user defined. Default: _R1_001.fastq.gz',default='_R1_001.fastq.gz')
subparser_adapter.add_argument('-ae', help='Trimming end mode:ANY,LEFT,RIGHT. Default:ANY', choices=['ANY','LEFT','RIGHT'], default='ANY')
subparser_adapter.add_argument('-u',type=int, help='Allowed uncalled bases N for each read. Default: %(default)s.', default=0,metavar='INT')
subparser_adapter.add_argument('-n',type=int, help='Number of threads, default:%(default)s', default=1, metavar='INT')
subparser_adapter.add_argument('-m',type=int, help='Minimum read lenght, default:%(default)s',default=18, metavar='INT')
subparser_adapter.add_argument('-z', help='Output compressed read format type GZ or BZ2', metavar='out_fmt')

#-------------------------------------------------------------------quality trimming----------------------------------------------------------------

subparser_quality = subparsers.add_parser('quality',help='To perform the quality trimming on reads',
					    usage='flexbar_wrapper.py quality <readdir> <outdir> [options]',
					    description='It will removes the bases based on quality')

subparser_quality.add_argument('readdir', help='Directory containing the forward and reverse reads .fastq,.gz,.bz2', metavar="readdir")
subparser_quality.add_argument('outdir',help='Directory to save quality trimmed reads',metavar='outdir')
subparser_quality.add_argument('-string',help='End of the read file name eg. _R1_001.fastq.gz or _1.fastq.gz or user defined. By default: _1.fastq.gz',default='_1.fastq.gz')
subparser_quality.add_argument('-q', help='Quality-based trimming mode. One of TAIL, WIN, and BWA.Default: TAIL', choices=['TAIL','WIN','BWA'], default='TAIL')
subparser_quality.add_argument('-u',type=int, help='Allowed uncalled bases N for each read. Default: %(default)s.', default=0,metavar='INT')
subparser_quality.add_argument('-n',type=int, help='Number of threads, default:%(default)s', default=1, metavar='INT')
subparser_quality.add_argument('-qf', help='Quality format. One of sanger, solexa, i1.3, i1.5, and i1.8. Default: sanger', default='sanger')
subparser_quality.add_argument('-qt',type=int, help='Phred score value-cut off:%(default)s', default=20, metavar='INT')
subparser_quality.add_argument('-m',type=int, help='Minimum read lenght, default:%(default)s',default=18, metavar='INT')
subparser_quality.add_argument('-z', help='Output compressed read format type GZ or BZ2', metavar='out_fmt')
args = parser.parse_args()

##Processing the read##
read_n=[]
read_dir=os.listdir(args.readdir)
reads_sorted=sorted(read_dir)

##Making output dir!!!##
os.mkdir(args.outdir)

Parallel(n_jobs=args.n)(delayed(flexbar)(reads_sorted,j,args.mode,args.outdir) for j in range(0,len(reads_sorted),2))
