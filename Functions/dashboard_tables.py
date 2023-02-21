#Libraries
import pandas as pd
import numpy as np
from pathlib import Path

#Functions

#Re-Arrange of eda dataframes
def descriptive_stats_arrange(folder, name, id_vars, pivot_columns,
                                round):
    df = pd.read_excel(Path(f'{folder}/{name}.xlsx'))
    id_vars2 = id_vars + pivot_columns
    drop = [col for col in df.columns if col not in id_vars2]
    #Melt the dataframe base on the list above as a first step 
    #toward a long format data  for graphical use
    df = df.melt(id_vars = id_vars2, value_vars=drop, 
                    var_name='Methodology', value_name='Results')
    index = id_vars + ['Methodology']
    #Second step, now all variables such as metrics are columns.
    df = df.pivot(index=index, columns=pivot_columns, 
                    values=['Results']).reset_index()
    df.columns = [f'{f} {s}' if s != '' else f'{f}' 
                for f, s in df.columns]
    df.dropna(inplace=True)
    df = df.round(round)
    return df

#Re-Arrange of diff dataframes
def diff_arrange(folder, name, id_vars, round):
    df = pd.read_excel(Path(f'{folder}/{name}.xlsx'))
    drop = [col for col in df.columns if col not in id_vars]
    df = df.melt(id_vars = id_vars, value_vars=drop, 
                    var_name='Category', value_name='Results')
    df = df[(df['Category']!= 'Rep')&(df['Category']!= 'id')]
    df.dropna(inplace=True)
    df = df.round(round)
    return df

def tables_loader(folder, name, round):
    dataframe = pd.read_excel(Path(f'{folder}/{name}.xlsx'))
    dataframe = dataframe.round(round)
    return dataframe