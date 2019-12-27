import requests
from lxml import html
import unicodedata
import pandas as pd

page=requests.get('http://www.cazy.org/GH58_bacteria.html')
tree=html.fromstring(page.content)
protein_name=tree.xpath('//*[@id="separateur2"]/text()')
organism=tree.xpath('//*[@id="separateur2"]/a/b/text()')
#protein_name=list(filter(lambda item: item not in ['\r\n\t\t\t\t\r\n\t\t\t\t\r\n\t\t\t\t\t', '\r\n\t\t\t\t\r\n\t\t\t', '\r\n\t\t\t\t ','\xa0','\xa0 '], protein_name))
#protein_name
#organism
organism.insert(40,'Escherichia coli K1 PHAGE')
microbes=organism[::2]
genbank=organism[1::2]
for i in range(0,len(organism)):
    print (organism[i]+"\t"+str(i))
prtn_list=[]
for i in range(0,len(protein_name)):
    new_str= unicodedata.normalize("NFKD", protein_name[i])
    new_str= new_str.strip()
    if new_str != '':
        prtn_list.append(new_str)
#prtn_list
df=pd.DataFrame(columns=['Protein name','Organism','Genbank'])
for i in range(0,len(prtn_list)):
    if "Escherichia coli" in microbes[i]:
        df.loc[i]={'Protein name': prtn_list[i], 'Organism':microbes[i], 'Genbank':genbank[i]}
df
