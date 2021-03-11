#!/usr/bin/env python
#This script will summarize the annotation, gene symbols and cog letter for each orthologous gene clusters from the eggnog output

import pandas as pd
import argparse
from pathlib import Path
import numpy as np




if __name__ == '__main__':
    parser=argparse.ArgumentParser(description='summarizing eggnog result')
    parser.add_argument( '-l', '--locustag', type = str, required = True, help = 'Path to the file consist of full path of gene clusters with locustag')
    parser.add_argument( '-i', '--input_file', type = str, required = True, help = 'result from the eggnog annotation pipeline')
    parser.add_argument('-o', '--output',type = str,required=True, help="output file name")
    args = parser.parse_args()


locustags_file=pd.read_table(args.locustag, header=None)
#len(locustags_file)
eggnog=pd.read_table(args.input_file, header=None, low_memory=False, comment='#')
eggnog.columns=['query_name','seed_eggNOG_ortholog','seed_ortholog_evalue','seed_ortholog_score','best_tax_level','Preferred_name','GOs','EC','KEGG_ko','KEGG_Pathway','KEGG_Module','KEGG_Reaction','KEGG_rclass','BRITE','KEGG_TC','CAZy','BiGG_Reaction','Unnamed: 17','Unnamed: 18','Unnamed: 19','Unnamed: 20','Unnamed: 21']

eggnog['Unnamed: 21'].fillna('No-gene-function',inplace=True)
eggnog['Preferred_name'].fillna('No-gene-symbol',inplace=True)
eggnog['Unnamed: 20'].fillna('No-cog-letter',inplace=True)
final_summary=pd.DataFrame()

for i in range(0,len(locustags_file)):
    eggnog_matched=pd.DataFrame()
    combine_df=pd.DataFrame()
    missing=pd.DataFrame()
    cluster_summary=pd.DataFrame()

    file_1=locustags_file.iloc[i,0]
    cluster_name=Path(file_1).name
    cluster_read=pd.read_table(file_1,header=None)

    eggnog_matched=eggnog[eggnog['query_name'].isin(cluster_read[0])]
    missing=cluster_read[~cluster_read[0].isin(eggnog['query_name'])]
    missing=missing.reset_index().drop('index',axis=1)
    missing_df=pd.DataFrame('No-hits',index=np.arange(len(missing)), columns=eggnog.columns)
    missing_df['query_name']=missing

    eggnog_frames=[eggnog_matched,missing_df]
    combine_df=pd.concat(eggnog_frames,ignore_index=True)

    cluster_summary=combine_df.groupby(["Preferred_name","Unnamed: 21","Unnamed: 20"]).size().reset_index()
    cluster_summary['cluster']=cluster_name
    cluster_summary['total_count']=len(cluster_read)

    if final_summary.empty:
        final_summary=cluster_summary
    else:
        tmp=[final_summary,cluster_summary]
        final_summary=pd.concat(tmp,ignore_index=True)

final_summary.columns=["Gene_name","Function","COG","Count","cluster_name","total_count"]
final_summary=final_summary[["cluster_name","Gene_name","Function","COG","Count","total_count"]]
final_summary.to_csv(args.output,header=True,sep="\t",index=False)
