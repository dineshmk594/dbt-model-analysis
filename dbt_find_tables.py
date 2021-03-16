# -*- coding: utf-8 -*-
"""
@author: Dineshkumar
"""

import pandas as pd
import sys
import subprocess
  
import warnings


warnings.simplefilter("ignore")
    
input = sys.argv[1]
print("Model name read as input: ",input)
w= 'findstr /S "ref" ' + input
a=subprocess.check_output(w)
a=a.decode("utf-8") 
a=a.splitlines()   

df=pd.DataFrame(a,columns=['text'])
df_ref=pd.DataFrame(df.text.str.split("'",3).tolist(),
                                 columns = ['junk','table','junk'])

ref_output=df_ref[['table']].drop_duplicates()

ref_output['counter']=0


n=10
while n>=1:
    max_counter=max(ref_output.counter)
    ref_temp=ref_output.table[ref_output.counter==max_counter]
    all_final_ref = pd.DataFrame(columns = ['junk','table','junk'])
    for k in ref_temp:
        if k == None:
            continue
        k=k+'.sql'
        z='findstr /S "ref" ' + k
        try:
            subprocess.check_output(z)
        except:
            continue
        z=subprocess.check_output(z)
        z=z.decode("utf-8") 
        z=z.splitlines()
        if z == ['FINDSTR: // ignored']:
            continue
        all_ref=[]
        for j in z:    
            all_ref.append(j)
        all_ref=pd.DataFrame(all_ref,columns=['text'])
        all_ref=pd.DataFrame(all_ref.text.str.split("'",3).tolist(),
                                 columns = ['junk','table','junk'])
        all_final_ref = pd.concat([all_final_ref,all_ref.drop_duplicates()],axis=0)
    if all_final_ref.table.value_counts().sum() == 0:
        n=0
    all_final_ref['counter']=max(ref_output.counter)+1
    ref_output=pd.concat([ref_output,all_final_ref[['table','counter']]],axis=0)
    ref_output=ref_output.drop_duplicates(subset='table',keep='last')
    print("looping in level",max_counter)


ref_output.dropna(inplace=True)
ref_output.reset_index(drop=True,inplace=True)

ref_output.columns = ['table','level']
# SOurce table findings

source_output=pd.DataFrame(columns=['schema','table'])
for s in ref_output.table:
    tbl=s+'.sql'
    stg = 'findstr /S "{{source" '+ tbl
    try:
        subprocess.check_output(stg)
    except:
        continue
    stg=subprocess.check_output(stg)
    stg=stg.decode("utf-8") 
    stg=stg.splitlines()
    if stg == ['FINDSTR: // ignored']:
            continue
    all_ref=[]
    for e in stg:
        all_ref.append(e)
    all_ref=pd.DataFrame(all_ref,columns=['text'])
    all_ref=pd.DataFrame(all_ref.text.str.split("'").tolist(),
                                 columns = ['junk','schema','q','table','junk'])    
    source_output = pd.concat([source_output,all_ref[['schema','table']]],axis=0)
source_output = source_output.drop_duplicates(subset=['schema','table'])


source_output.dropna(inplace=True)
source_output.reset_index(drop=True,inplace=True)
pd.set_option('display.max_rows', None)
print("List of tables used in reference")
print(ref_output)
print("List of tables used as source")
print(source_output)


