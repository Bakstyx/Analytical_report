#Libraries
import os
import random
from itertools import combinations
import pandas as pd
import numpy as np

### Script



#### class
class Descriptive():
    
    def __init__(self, data):
        self.data = data
    

#Functions
def descript_stats(data, dv, di, gral_description=None, param=None, percent=None, 
            save=False, folder=None, title=None):
    determ = ['count', 'mean', 'std', 'min', 'max', '25%', '50%', '75%']
    cat_list = dv + di
    drop_set = set(data.columns.to_list()).difference(set(cat_list))
    data_1 = data.drop(columns=drop_set)
    # stats_descriptions
    summary_data = data_1.groupby(by=dv).describe(percentiles=percent)
    
    #delete unnecesary row of metrics
    if param != None:
        drop_params_set = [metric for metric in determ if metric not in param]      
        summary_data.drop(columns=drop_params_set, axis=1, level=1, 
                            inplace=True, errors='ignore')
    
    #organize de dataframe
    summary_data.columns = summary_data.columns.map('{0[0]}/{0[1]}'.format)
    summary_data = summary_data.transpose()
    summary_data.reset_index(inplace=True)
    summary_data[['Category', 'Metric']]= summary_data['index'].str.split('/', expand=True, regex=True)
    summary_data.drop(columns=['index'], inplace=True, errors='ignore')
    summary_data.insert(0, 'Category', summary_data.pop('Category'))
    summary_data.insert(1, 'Metric', summary_data.pop('Metric'))
    summary_data.sort_values(by=['Category', 'Metric'], 
                                ascending=True, inplace=True)
    
    if type(gral_description) == pd.core.frame.DataFrame:
            summary_data = gral_description.merge(summary_data, on=['Category', 'Metric'])
    if save == True:
        os.makedirs(f'{folder}', exist_ok=True)
        summary_data.to_excel(f'{folder}/{title}.xlsx', index=False)
    return summary_data.round(3)

def difference_calculator (data, clasif, sub_index, abs=False, 
                            include=None, exclude=None,
                            save=False, folder=None, title=None):
    classifier_list = data[clasif].unique().tolist()
    combinatory = list(list(combinations(classifier_list, 2)))
    if include is not None:
        combinatory = [combination for combination in combinatory 
                                                if include in combination]
    if exclude is not None:
        combinatory = [combination for combination in combinatory 
                                                if exclude not in combination]
    #dataframe creation and columns selection
    dataframe = pd.DataFrame()
    columns = data.columns.tolist()
    
    for combination in combinatory:
        data_comb_1 = data[data[clasif]== combination[0]]
        data_comb_1 = data_comb_1[[column for column in columns 
                                    if data_comb_1[column].dtype != 'object']]

        data_comb_2 = data[data[clasif]== combination[1]]
        data_comb_2 = data_comb_2[[column for column in columns 
                                    if data_comb_2[column].dtype != 'object']]

        data_comb_diff = data_comb_1.set_index(sub_index).subtract(data_comb_2.set_index(sub_index))
        data_comb_diff.reset_index(inplace=True)
        data_comb_diff['Differences'] = f'{combination[0]}_vs_{combination[1]}'
        data_comb_diff.insert(0, 'Differences', data_comb_diff.pop('Differences'))
        dataframe = pd.concat([dataframe, data_comb_diff])
    dataframe.reset_index(inplace=True, drop=True)
    
    if abs ==True:
        for combination in dataframe.columns.tolist():
            if dataframe[combination].dtype=='float64' or dataframe[combination].dtype=='int64':
                dataframe[combination] = dataframe[combination].abs()
        else:
            dataframe[combination] = dataframe[combination]
    if save == True:
        os.makedirs(f'{folder}', exist_ok=True)
        dataframe.to_excel(f'{folder}/{title}.xlsx', index=False)
    
    return dataframe.round(3) 

def stats_data_arrange(df, id_vars):
    drop = list( set(df.columns.tolist()) - set(id_vars))
    df = df.melt(id_vars = id_vars, value_vars=drop, 
                    var_name='Category', value_name='Results')
    df = df[(df['Category']!= 'Rep')&(df['Category']!= 'id')]
    df.dropna(inplace=True)
    return df



