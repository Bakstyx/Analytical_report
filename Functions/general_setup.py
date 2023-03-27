#Libraries
import os
import glob
from pathlib import Path

import pandas as pd
import numpy as np
import warnings
from datetime import date
import matplotlib.pyplot as plt
import seaborn as sns

#Scripts
import automatic_dict as ad
import google_api
import exception_handeler as eh
import descriptive_statistics as ds
import descript_stats_graphs as dsg
import anova
import anova_assumptions as aa
import post_hoc_test as pht
import anova_graphs as ag
import limits_analysis as la




# rc parameters
plt.rc("figure", figsize=(15, 12))
plt.rc("font", family="serif", size=20)  # Ticks labels
plt.rc("xtick", labelsize=18)  # Xticks numbers
plt.rc("ytick", labelsize=18)  # Yticks numbers
plt.rc("figure", titlesize=25)  # Figure title
plt.rc("legend", fontsize=18)  # Legend
plt.rc("savefig", bbox="tight")
plt.rc("savefig", dpi=300)
plt.rc("savefig", facecolor="white")
plt.rc("savefig", transparent=False)

#sns style
sns.set_style("whitegrid")

#Functions
def folder_creator(Folder_1, Folder_2, Title_1, Title_2, Date):
    if Folder_2=='' and Title_2=='':
        fold = f'Results/{Folder_1}/{Title_1}/{Title_1}-{Date}'
    elif Folder_2!='' and Title_2=='':
        fold = f'Results/{Folder_1}/{Folder_2}/{Title_1}/{Title_1}-{Date}'
    elif Folder_2=='' and Title_2!='':
        fold = f'Results/{Folder_1}/{Title_1}/{Title_2}/{Title_2}-{Date}'
    else:
        fold = f'Results/{Folder_1}/{Folder_2}/{Title_1}/{Title_2}/{Title_2}-{Date}'
    os.makedirs(fold, exist_ok=True)
    print(fold)
    return fold



def style2(dataframe, exclude=None):
    #Columns selector
    columns = [column for column in dataframe.columns 
            if column not in exclude]
    
    #numers format
    dataframe[columns].replace(',', '.', regex=True, inplace=True)
    
    #Datatype format
    for column in columns:
        try:
            dataframe[column] = pd.to_numeric(dataframe[column])
        except:
            dataframe[column] = dataframe[column].astype(str)
    
    #date_time format flux
    print(dataframe.info())
    return dataframe


def import_data(Spreadsheet_id=None, File_id=None, data_to_pull=None):
    if Spreadsheet_id!='' and File_id=='':
        data = google_api.pull_sheet_data(Spreadsheet_id,data_to_pull)
        dataframe = pd.DataFrame(data[1:], columns=data[0], )
        dataframe = style2(dataframe)
        dataframe = eh.standard_dataframe(dataframe)
        return(dataframe)
    elif Spreadsheet_id=='' and File_id !='':
        if File_id[-4:]=='.csv':
            dataframe = pd.read_csv(File_id)
            dataframe = eh.standard_dataframe(dataframe)
            print(dataframe.info())
            return(dataframe)
        elif File_id[-4:] in ['.xls', 'xlsx']:
            dataframe = pd.read_excel(File_id, sheet_name=data_to_pull)
            dataframe = eh.standard_dataframe(dataframe)
            print(dataframe.info())
            return(dataframe)
        else:
            print('No admited type of file')
    else:
        print('None or both directions file has been pass. Only one is admited')


#Table Compilers formulas

def gather_files(folder):
    #Load all files in the folder
    data = glob.glob(f'{folder}/**/*.xlsx', recursive=True)
    #List creator for sorting. list comprehension
    descript_stats = [file for file in data  
                        if 'descript_stats' in file 
                            and 'descript_stats_diff' not in file 
                                and 'descript_stats_diff_abs' not in file]
    diff = [file for file in data  
            if 'differences' in file and 'differences_abs' not in file]
    diff_abs = [file for file in data  if 'differences_abs' in file]
    descript_stats_diff = [file for file in data  
                            if 'descript_stats_diff' in file 
                                and 'descript_stats_diff_abs' not in file]
    descript_stats_diff_abs = [file for file in data  if 'descript_stats_diff_abs' in file]
    status_analysis = [file for file in data  if 'status_analysis' in file]
    anovas = [file for file in data  if 'anova' in file]
    
    #List of files and dictionaries fo evaluations and metrics.
    tables_dicts = {
        'descript_stats':descript_stats, 
        'diff':diff, 
        'diff_abs': diff_abs, 
        'descript_stats_diff': descript_stats_diff, 
        'descript_stats_diff_abs': descript_stats_diff_abs, 
        'status_analysis' : status_analysis, 
        'anovas' : anovas
        }
    return tables_dicts


def compile_results(folder=None):
    #Gather files
    tables_dicts = gather_files(folder)
    folder1 = f'{folder}/Compiler'
    os.makedirs(f'{folder}', exist_ok=True)

    for j in tables_dicts:
        if j != 'anovas':
            df1 = pd.DataFrame()
            for i in tables_dicts[j]:
                eval = Path(i).stem.split('-')[-1]
                file = str(Path(i).stem.split('-')[0])
                df = pd.read_excel(Path(i))
                df['Evaluation'] = eval
                df.insert(0, 'Evaluation', df.pop('Evaluation'))
                df1 = df1.append(df)
            df1.replace('_', ' ', regex=True, inplace=True)
            df1.to_excel(f'{folder1}/{file}.xlsx', index=False)
        else:
            for h in [0, 1]:
                if h == 0:
                    ext = 'anova'
                else:
                    ext = 'post_hoc'
                df1 = pd.DataFrame()
                for i in tables_dicts['anovas']:
                    eval = Path(i).stem.split('-')[-1]
                    df = pd.read_excel(Path(i), sheet_name=h)
                    df['Evaluation'] = eval
                    df.insert(0, 'Evaluation', df.pop('Evaluation'))
                    df1 = df1.append(df)
                df1.replace('_', ' ', regex=True, inplace=True)
                df1.to_excel(f'{folder1}/{ext}.xlsx', index=False)
    print('Results compiled. Check compile folder, in your results folder.')


