#libraries
import pandas as pd
import numpy as np



#Functions

def base_tolerance_lims(cat, norm_data):
    limites = ['Limit_base', 'Limit_tolerance']
    #Definicion de limites
    lim_base = norm_data[norm_data['Category']==cat][limites[0]].tolist()[0]
    lim_tolerance = norm_data[norm_data['Category']==cat][limites[1]].tolist()[0]
    #conditional limit selection
    exchange = 0
    if lim_base > lim_tolerance:
        lim_menor = lim_tolerance
        lim_mayor = lim_base
        exchange=1
    else:
        lim_menor = lim_base
        lim_mayor = lim_tolerance
    #result list
    return [lim_menor, lim_mayor, exchange]


def limits_clasification(data, categories, limits_data, eval, save=False, name=None, 
                            folder=None):
    #Classified columns
    classified_columns = [cat for cat in data.columns.tolist() 
                            if cat not in categories]

    dfa = data.melt(id_vars=classified_columns, var_name='Category', 
                    value_name='Results')
    df_lim = pd.DataFrame()
    for cat in categories:
        if cat in data.columns.tolist():
            if cat in limits_data['Category'].unique().tolist():
                lims = base_tolerance_lims(cat, norm_data=limits_data)
                dfa_a = dfa[dfa['Category']==cat]
                if lims[2]==0:
                    dfa_a['Status'] = np.where(dfa_a['Results']<=lims[0], 'Below_base', 
                                            np.where((dfa_a['Results']>lims[0]) & (dfa_a['Results']<lims[1]), 'In between base-tolerance', 
                                                        np.where(dfa_a['Results']>=lims[1], 'Above tolerance', 'Non classified')))
                    df_lim = df_lim.append(dfa_a)
                else:
                    dfa_a['Status'] = np.where(dfa_a['Results']<=lims[0], 'Below tolerance', 
                                            np.where((dfa_a['Results']>lims[0]) & (dfa_a['Results']<lims[1]), 'In between base-tolerance', 
                                                        np.where(dfa_a['Results']>=lims[1], 'Above base', 'Non classified')))
                    df_lim = df_lim.append(dfa_a)
    # delete unsude columns. to preven un wanted behavior
    if eval in ['Repetibility', 'Accuracy_w_rep']:
        df_lim.drop(columns=['Rep'], inplace=True)
    #Save the results
    if save ==True:
        df_lim.to_excel(f'{folder}/{name}.xlsx', sheet_name=name, index=False)
    return df_lim

def limits_desicion(data, rv, classifier, merger, abs=True):
    #vr = referenced value
    #classifier = clasification column
    # merger = columns to do the merge
    dfa = data[data[classifier]==rv]
    dfb = data[data[classifier]!=rv]

    dfa.rename(columns={
        'Results' : 'Results_rv',
        'Status' : 'Status_rv'
        }, inplace=True)
    dfa.drop(columns=[classifier], inplace=True)

    dfb = dfb.merge(dfa, how='left', on=merger)
    dfb['Accuracy'] = np.where(dfb['Status']==dfb[f'Status_rv'], 'Same decision', 'Different decision')
    if abs == True:
        dfb['Differences'] = (dfb['Results'] - dfb[f'Results_rv']).abs()
    else:
        dfb['Differences'] = (dfb['Results'] - dfb[f'Results_rv'])
    return dfb

def status_analysis(data, group_total, group_parcial, 
                        save=False, name=None, folder=None):
    #Dataframe total result
    df_total = data.groupby(by=group_total, as_index=False, 
                                group_keys=False).size()
    
    #Dataframe parcial result more detailed
    group_parcial = group_total + group_parcial
    
    df_parcial = data.groupby(by=group_parcial, as_index=False, 
                                group_keys=False).size()
    
    #Organization and presentation of results
    df_parcial = df_parcial.merge(df_total, how='left', on=group_total, 
                                    suffixes=['_parcial', '_total'])
    #rename columns
    df_parcial.rename(columns={'size_parcial': 'Results_parcial',
                                        'size_total': 'Results_total'}, inplace=True)
    #calculate porcentage
    df_parcial['Porcetage'] = (df_parcial['Results_parcial']*100)/df_parcial['Results_total']
    df_parcial.insert(len(group_total), 'Methodology', df_parcial.pop('Methodology'))
    #organize table
    df_parcial.sort_values(by=group_parcial, ascending=True, inplace=True)
    df_parcial.reset_index(inplace=True, drop=True)
    df_parcial.dropna(inplace=True)
    if save ==True:
        df_parcial.to_excel(f'{folder}/{name}.xlsx', sheet_name=name, index=False)
    
    return df_parcial




