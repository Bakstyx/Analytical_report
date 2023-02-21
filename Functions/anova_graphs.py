#Libraries
import os
from matplotlib.dviread import Dvi
import statsmodels.api as sm
from bioinfokit.analys import stat

#Graphical Libs

import matplotlib.pyplot as plt
import seaborn as sns


# Functions

# Graphics
# ==============================================================================
def anova_graphs(df, dv, di, alpha, formula, folder):  
    res = stat()
    res.anova_stat(df=df, res_var=dv, anova_model= formula) 
    #Columns nd rows in the subplots         
    if len(di)<=1:
        row = 2
        col = 2
    else:
        row = 3
        col = len(di)
        
    #plots per se     
    fig, axes = plt.subplots(nrows=row, ncols=col, figsize=(12, 12))
    fig.suptitle(dv ,fontweight = "bold")
    #Axes 0,0. QQ-plot
    # res.anova_std_residuals are standardized residuals obtained from ANOVA 
    # (check above)
    sm.qqplot(res.anova_std_residuals, line='45',ax = axes[0, 0])
    axes[0, 0].set_xlabel("Theoretical Quantiles")
    axes[0, 0].set_ylabel("Standardized Residuals")
    axes[0, 0].set_title('Q-Q residual of model', fontsize = 10, 
                        fontweight = "bold")
    axes[0, 0].tick_params(labelsize = 8)

    # Axes 0,1. Histogram of residues
    sns.histplot(res.anova_model_out.resid, 
                    ec='k',
                    ax = axes[0, 1])
    axes[0, 1].set_xlabel("Residuals")
    axes[0, 1].set_ylabel('Frequency')
    axes[0, 1].set_title('Histogram of residuals')

    # Axes 1,0. Histogram of standardize residuals
    sns.histplot(
        data    = res.anova_std_residuals,
        stat    = "density",
        kde     = True,
        line_kws= {'linewidth': 1},
        color   = "firebrick",
        alpha   = alpha,
        ax      = axes[1, 0])
    axes[1, 0].set_title('Standard distribution of residuals', fontsize = 10, fontweight = "bold")
    axes[1, 0].set_xlabel("Residual")
    axes[1, 0].tick_params(labelsize = 7)

    # Axes 1,1 or 2. Distribution of data points.
    if len(di) <= 1:
        #Data distribution. just 1 source of variation.
        sns.boxplot(x=di[0], y=dv, data=df, color='#99c2a2', ax = axes[1, 1])
        sns.swarmplot(x=di[0], y=dv, data=df, color='#7d0013', ax = axes[1, 1])
        axes[1, 1].set_title('Data dispersion', fontsize = 10, fontweight = "bold")
        axes[1, 1].set_xlabel(f'{di[0]}')
        axes[1, 1].set_ylabel(f'{dv}')
    else:
        fig.delaxes(axes[1,1])
        d = 0 
        for c in di:
            #Data distribution. For each source of variation.
            sns.boxplot(x=c, y=dv, data=df, color='#99c2a2', ax = axes[2, d])
            sns.swarmplot(x=c, y=dv, data=df, color='#7d0013', ax = axes[2, d])
            axes[2, d].set_title('Data dispersion', fontsize = 10, fontweight = "bold")
            axes[2, d].set_xlabel(f'{di}')
            axes[2, d].set_ylabel(f'{dv}')
            
            d+=1
        
    #Encabezados
    fig.tight_layout()
    plt.subplots_adjust(top=0.9)
    os.makedirs(f'{folder}/Graphs_anova', exist_ok = True)
    figname = f'{folder}/Graphs_anova/{dv}.png'
    fig.savefig(figname)
    plt.show()
        

