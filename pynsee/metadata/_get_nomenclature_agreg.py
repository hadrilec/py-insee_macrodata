# -*- coding: utf-8 -*-
from functools import lru_cache
import pandas as pd

@lru_cache(maxsize=None)
def _get_nomenclature_agreg(file):
    
    df = pd.read_csv(file, sep=";",
                     #encoding='latin1',
                     encoding="ISO-8859-1",
                     dtype=str)
    
    for i in range(len(df.index)):
        for j in range(2,len(df.columns)):
            if pd.isna(df.iloc[i,j]):
                df.iloc[i,j] = df.iloc[i,j-1]
    
    for j in range(len(df.columns)):
        for i in range(len(df.index)):        
            if pd.isna(df.iloc[i,j]):
                df.iloc[i,j] = df.iloc[i-1,j]
                
    df = df.iloc[:,1:10] 
    df.columns = ['A10', 'A21', 'A38', 'A64', 'A88', 'A129', 'A138', 'TITLE']
    return(df)