#Libraries
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from bioinfokit.analys import stat
from tabulate import tabulate
import pandas as pd
import numpy as np


#Functions
def Tukey_HSD_test(df, di, dv, alpha, Interaccion, formula, file):
    post_hoc = pd.DataFrame()
    for a in di:
                # Post-hoc comparison - Simple effect
                # ==============================================================================
                # perform multiple pairwise comparison (Tukey's HSD)
                # unequal sample size data, tukey_hsd uses Tukey-Kramer test
                HSD_res=pairwise_tukeyhsd(df[dv], df[a], alpha=alpha)
                print(' Tukey HSD table results '.center(60, '='), '\n')
                print(f' Effect:{a} '.center(60, '='), '\n')
                print(HSD_res, '\n', '\n')
                with open(file, 'a+') as f:
                    f.write((' Tukey HSD table results '.center(60, '=')))
                    f.write('\n')
                    f.write(f' Effect:{a} '.center(60, '='))
                    f.write('\n')
                    f.write(f'Multiple Comparison of Means - Tukey HSD, FWER={alpha}')
                    f.write('\n')
                    f.write(tabulate(HSD_res.summary(), tablefmt = 'grid'))
                    f.write('\n'+'\n'+'\n')
                    f.close()
                f = pd.DataFrame(HSD_res._results_table.data[1:], 
                             columns=HSD_res._results_table.data[0])
                f.insert(0, 'Variable', dv)
                f.insert(1, 'Group', a)
                post_hoc = post_hoc.append(f)

    if len(di)>1 and Interaccion == True:
        # Post-hoc comparison - Interaccion
        # ==============================================================================
        res = stat()
        res.tukey_hsd(df=df, res_var=dv, xfac_var=di, anova_model=formula, phalpha=alpha)
        dfp1 = res.tukey_summary
        dfp1.rename(columns={'Diff':'meandiff', 'Lower':'lower', 'Upper':'upper',
                            'p-value':'p-adj'}, inplace=True)
        dfp1 = dfp1.drop(columns=['q-value'])
        dfp1.insert(0, 'Variable', dv)
        dfp1.insert(1, 'Group', str(di))
        dfp1['reject'] = np.where(dfp1['p-adj']>=alpha, 'False', 'True')
        dfp2 = dfp1.loc[dfp1['p-value']<alpha]
        print(' Tukey HSD table results '.center(40, '='), '\n')
        print(f' Multiple Comparison of Means - Tukey HSD, FWER={alpha} '.center(40, ' '))
        print(''.center(40, '='))
        print(dfp1, '\n', '\n',)
        with open(file, 'a+') as f:
            f.write((' Tukey HSD table results: Interaccions '.center(50, '=')))
            f.write('\n')
            f.write(f'Multiple Comparison of Means - Tukey HSD, FWER={alpha}')
            f.write('\n')
            f.write(tabulate(dfp1, headers='keys'))
            f.write('\n'+'\n')
            f.close()
        #Print and summary all interacction case of significant differences
        if dfp2.shape[0] != 0:
            print(' Tukey HSD table results '.center(40, '='), '\n')
            print(f' Multiple Comparison of Means - Tukey HSD, FWER={alpha} '.center(40, ' '))
            print(' Summary of significant differences '.center(40, ' '))
            print(''.center(40, '='))
            print(dfp2, '\n', '\n',)
            with open(file, 'a+') as f:
                f.write((' Tukey HSD table results: Interaccions '.center(40, '=')))
                f.write('\n')
                f.write(f'Multiple Comparison of Means - Tukey HSD, FWER={alpha}')
                f.write('\n')
                f.write(' Summary of significant differences '.center(40, ' '))
                f.write('\n')
                f.write(tabulate(dfp2, headers='keys'))
                f.write('\n'+'\n')
                f.close()
        else:
            print('There is no cases of significant difference')
            with open(file, 'a+') as f:
                f.write((' Tukey HSD table results: Interaccions '.center(40, '=')))
                f.write('\n')
                f.write(f'Multiple Comparison of Means - Tukey HSD, FWER={alpha}')
                f.write('\n')
                f.write('There is no cases of significant difference')
                f.write('\n'+'\n'+'\n')
                f.close()
        post_hoc = post_hoc.append(dfp1)    
    return post_hoc