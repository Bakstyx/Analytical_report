#Libraries
import pingouin as pg
from bioinfokit.analys import stat
from tabulate import tabulate


#Funtions
#test for normality and homocedasticity
def anova_normality(df, dv, di, alpha, file):
    # Anovas Assumptions. Normality
    try:
        for b in di:
            # Test ANOVA assumptions
            # ==========================================
            # Shapiro - Wilk test (Normality)
            shap = pg.normality(data = df, dv=dv , group= b, 
                                method='shapiro', alpha = alpha)
            print(' Normality table results '.center(40, '='), '\n')
            print(f' Effect:{b} '.center(40, '='), '\n')
            print(shap, '\n', '\n')
            #save in file
            with open(file, 'a+') as f:
                f.write(' Normality table results '.center(40, '='))
                f.write('\n')
                f.write(f' Effect:{b} '.center(40, '='))
                f.write('\n')
                f.write(tabulate(shap, headers='keys', tablefmt = 'grid'))
                f.write('\n'+'\n')
                f.close()
    except :
        print('Few amount of data. Normality test is not possible')
        with open(file, 'a+') as f:
                f.write(' Normality table results '.center(40, '='))
                f.write('\n')
                f.write(f' Effect:{b} '.center(40, '='))
                f.write('\n')
                f.write('Few amount of data. Normality test is not possible')
                f.write('\n'+'\n')
                f.close()

def anova_homocedasticity(df, dv, di, file):
    # Anovas Assumptions. Homocedasticity of variances.
    try:
        for b in di:
            # Test ANOVA assumptions
            # ===========================================
            # Bartlett Homogeneity of variances test
            res = stat()
            res.bartlett(df= df, res_var=dv, xfac_var= b)
            print(' Homogeneity of variances results '.center(40, '='), '\n')
            print(f' Effect:{b} '.center(40, '='), '\n')
            print(res.bartlett_summary, '\n', '\n',)
            with open(file, 'a+') as f:
                f.write(' Homogeneity of variances results '.center(40, '='))
                f.write('\n')
                f.write(f' Effect:{b} '.center(40, '='))
                f.write('\n')
                f.write(tabulate(res.bartlett_summary, headers='keys', tablefmt = 'grid'))
                f.write('\n'+'\n')
                f.close()
    except :
        print('Few amount of data. Homocedasticity test is not possible')
        with open(file, 'a+') as f:
                f.write(' Homogeneity of variances results '.center(40, '='))
                f.write('\n')
                f.write(f' Effect:{b} '.center(40, '='))
                f.write('\n')
                f.write('Few amount of data.  Homocedasticity test is not possible')
                f.write('\n'+'\n')
                f.close()