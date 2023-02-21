#Libraries
import os
from pyexpat import model
import numpy as np
import pandas as pd
from tabulate import tabulate
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.sandbox.stats.multicomp import TukeyHSDResults
from statsmodels.stats.multitest import multipletests
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from statsmodels.stats.multicomp import MultiComparison
import pingouin as pg
from bioinfokit.analys import stat
from Functions.exception_handeler import anova_categorial_dtypes

#Scripts
import exception_handeler as eh
import post_hoc_test as pht
import anova_assumptions as aa
import anova_graphs as ag


def anova_eva(df, dv, formula, alpha, name,  file, ols_r=True):
    
    print((f'{name} - {dv}').center(40, '='), '\n', '\n')
    # Anovas
    # ==============================================================================
    # Ordinary Least Squares (OLS) model
    formula1 = f'{dv}~{formula}'
    model = ols(formula = formula1, data=df).fit()
    try:
        anova_table = sm.stats.anova_lm(model, typ=1, robust='hc2')
    except:
        anova_table = sm.stats.anova_lm(model, typ=1)
    anova_table.rename(columns={'PR(>F)':'P-value'}, inplace=True)
    anova_table2 = model.summary()
    header1 = ' Anovas table results '.center(40, '=')
    if ols_r==True:
        print('OLS model report'.center(40, '='))
        print(anova_table2, '\n')
    print(header1, '\n')
    print(anova_table, '\n', '\n')
    
    # Saving file
    with open(file, 'a+') as f:
        f.write((f' {name} - {dv} ').center(40, '='))
        f.write('\n')
        if ols_r==True:
            f.write('OLS Results')
            f.write(tabulate(anova_table2.tables[0]))
            f.write(tabulate(anova_table2.tables[1]))
            f.write(tabulate(anova_table2.tables[2]))
            f.write("""Notes:
                    [1] Standard Errors assume that the covariance matrix of the errors is correctly specified.""")
            f.write('\n'+'\n')
        f.write(header1)
        f.write('\n')
        f.write(tabulate(anova_table, headers='keys', tablefmt = 'grid'))
        f.write(('\n'+'\n'+'\n'))
        f.close()
    # Summary or resume for the test and commercial purposes
    anova_table.drop(columns = 'F', inplace=True, errors='ignore')
    anova_table.reset_index(inplace=True)
    anova_table.rename(columns={'PR(>F)':'P-value', 'index': 'Variable'}, inplace=True)
    anova_table.drop(anova_table[anova_table['Variable']=='Residual'].index, inplace=True, errors='ignore')
    anova_table['Category'] = dv
    anova_table['Statistical differences'] = np.where(anova_table['P-value']>alpha, 'Not Significant', 'Significant')
    anova_table =anova_table.round(3)
    return anova_table



def anova_report(df, di, formula, name, Interaccion, alpha, file, 
                    categories, ols_r=True, folder=None):
    summary = pd.DataFrame(columns=['Category', 'Variable', 'df', 'sum_sq', 'mean_sq', 'P-value','Statistical differences'])
    post_hoc_summary = pd.DataFrame()
    #Save folder system
    if folder==None:
        folder_a = f'Statistical Evaluation - {name}'
        os.makedirs(f'{folder_a}', exist_ok = True)
    else:
        name2 = name.split('.')[0]
        folder_a = f'{folder}/{name2}'
        os.makedirs(f'{folder_a}', exist_ok = True)
    
    #File of text
    #Inicialize the object file.
    
    file = f'{folder_a}/{file}'    
    with open(file, 'w+') as f:
        f.write(name.center(40, ' '))
        f.write('\n')
        f.write('\n')
        f.close()

    for cat in categories:
        if cat in df.columns:
            formula_full = f'{cat}~{formula}'
            
            #Anova Analysis (function above)
            df = eh.anova_categorial_dtypes(df)
            anova = anova_eva(df=df, dv=cat, formula=formula, 
                                alpha=alpha, name=name,  file=file,
                                ols_r=ols_r)
            summary = summary.append(anova)
            
            #Test post_hoc. Post-hoc Analysis
            tukey = pht.Tukey_HSD_test(df=df, di=di, dv=cat, alpha=alpha, 
                                        Interaccion=Interaccion, formula=formula_full, file=file)
            post_hoc_summary = post_hoc_summary.append(tukey)
            
            # Anovas Assumptions. Normality and Homocedasticity
            aa.anova_normality(df=df, dv=cat, di=di, alpha=alpha, file=file)
            
            aa.anova_homocedasticity(df=df, dv=cat, di=di, file=file)
            
            # Graphics
            # ==============================================================================
            try:
                ag.anova_graphs(df=df, dv=cat, di=di, alpha=alpha,  
                            formula=formula_full, folder=folder_a)
            except:
                print('')
    #Saving files
    with pd.ExcelWriter(f'{folder_a}/{name}.xlsx',mode='w') as writer:  
        summary.to_excel(writer, sheet_name=f'{name}_anova', index=False)
        post_hoc_summary.to_excel(writer, sheet_name=f'{name}_post_hoc', index=False)        
    
    return summary


def anova_generator(dataframe, data_to_pull, di, formula,  Interaccion, 
                    alpha, categories, ols_r, folder):
    if data_to_pull == 'Repetibility':
        for method in dataframe['Methodology'].unique():
            df1 = dataframe[dataframe['Methodology']== method]
            anova_report(df = df1,
                    di = di,
                    formula = formula,
                    name = f'anova-{data_to_pull}.{method}',
                    Interaccion = Interaccion,
                    alpha= alpha,
                    file = f'Anova_report-{data_to_pull}_{method}.docx',
                    categories = categories,
                    ols_r = ols_r,
                    folder = folder)
    else:
        anova_report(df = dataframe,
                    di = di,
                    formula = formula,
                    name = f'anova-{data_to_pull}',
                    Interaccion = Interaccion,
                    alpha= alpha,
                    file = f'Anova_report-{data_to_pull}.docx',
                    categories = categories,
                    ols_r = ols_r,
                    folder = folder)