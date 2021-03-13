import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np
import argparse
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.ensemble import ExtraTreesClassifier

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Host classifiction using RandomForest')
    parser.add_argument( '-g', '--gene_pres_abs_file', type = str, required = True, help = '')
    parser.add_argument( '-p', '--phenotype_file', type = str, required = True, help = '')
    #parser.add_argument( '-t', '--threshold', type =int, required = False,default=90, help = '')
    #parser.add_argument( '-n', '--number_of_iterations', type =int, required = False,default=100, help = '')
    parser.add_argument( '-o', '--output_file', type = str, required = False, help = '')
    args = parser.parse_args()

gene_pres_abs = pd.read_table(args.gene_pres_abs_file,sep='\t',index_col='Gene')
pheno=pd.read_csv(args.phenotype_file,sep=',',index_col='id',header=0)

host=[]
pres_abs_t=gene_pres_abs.T
for i in range(0,len(pres_abs_t.index)):
    for j in range(0,len(pheno.index)):
        if pres_abs_t.index[i] == pheno.index[j]:
           #print (pres_abs_t.index[i]+'\t'+pheno.index[j]+'\t'+pheno.iloc[j,0])
           host.append(pheno.iloc[j,0])

host_label=np.array(host)

labels=pd.DataFrame(host_label.reshape(len(host_label),1))
X=pres_abs_t.iloc[:,0:len(pres_abs_t.columns)-1].values
y=labels.iloc[:,0].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.50, random_state=0)

regressor = RandomForestClassifier(n_estimators=100, random_state=0)
regressor.fit(X_train, y_train)


importances = regressor.feature_importances_
std = np.std([tree.feature_importances_ for tree in regressor.estimators_],
             axis=0)
indices = np.argsort(importances)[::-1]


for f in range(X.shape[1]):
    print("%d. feature %d (%f)" % (f + 1, indices[f], importances[indices[f]]))



y_pred = regressor.predict(X_test)

print(regressor.feature_importances_)
print(confusion_matrix(y_test,y_pred))  
print(classification_report(y_test,y_pred))  
print(accuracy_score(y_test, y_pred))











