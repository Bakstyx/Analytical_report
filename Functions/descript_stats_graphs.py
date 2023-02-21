#Libraries
import os
import matplotlib.pyplot as plt
from matplotlib.cbook import boxplot_stats
from adjustText import adjust_text
import numpy as np
import seaborn as sns
import matplotlib.gridspec as gridspec
import pandas as pd
import itertools
import pingouin as pg
import textwrap
from sklearn import linear_model
from sklearn.metrics import r2_score
from torch import combinations

#Scripts
import exception_handeler as eh
import automatization_funtions as af


#Graph and save a box plot with a broken axis ()
def box_plot_broken(lims, data, x, cat, hue=None, save=False, 
                folder=None):
    for i in cat:
        if i in data.columns:
            y=i
            ylim  = lims[0]
            ylim2 = lims[1]
            ylimratio = (ylim[1]-ylim[0])/(ylim2[1]-ylim2[0]+ylim[1]-ylim[0])
            ylim2ratio = (ylim2[1]-ylim2[0])/(ylim2[1]-ylim2[0]+ylim[1]-ylim[0])
            gs = gridspec.GridSpec(2, 1, 
                                height_ratios=[ylimratio, ylim2ratio]
                                )
            fig = plt.figure()
            ax1 = fig.add_subplot(gs[0])
            ax2 = fig.add_subplot(gs[1])
            ax1 = sns.boxplot(x=x, y=y,
                            hue=hue,
                            data=data, 
                            ax = ax1,
                        )
            ax1 = sns.swarmplot(x=x, y=y,
                                hue=hue,
                                data=data, 
                                ax = ax1, 
                            color = 'black'
                            )
            ax2 = sns.boxplot(x=x, y=y,
                            hue=hue,
                            data=data, 
                            ax = ax2,
                        )
            ax2 = sns.swarmplot(x=x, y=y,
                                hue=hue,
                                data=data, 
                                ax = ax2, 
                                color = 'black'
                            )
            ax1.set_ylim(ylim)
            ax2.set_ylim(ylim2)
            plt.subplots_adjust(hspace=0.1)
            ax1.spines['bottom'].set_visible(False)
            ax2.spines['top'].set_visible(False)
            ax1.xaxis.tick_top()
            ax1.set_xticklabels([])
            ax1.tick_params(labeltop='off')
            ax2.xaxis.tick_bottom()
            ax1.set_ylabel('')
            ax1.set_xlabel('')
            if hue is not None:
                ax1.legend().set_visible(False)
                ax2.legend(loc = 'lower left', bbox_to_anchor= (1, 1))
            ax2.yaxis.set_label_coords(0.05, 0.5, transform=fig.transFigure)
            kwargs = dict(color='k', clip_on=False)
            xlim = ax1.get_xlim()
            dx = .02*(xlim[1]-xlim[0])
            dy = .01*(ylim[1]-ylim[0])/ylimratio
            ax1.plot((xlim[0]-dx,xlim[0]+dx), (ylim[0]-dy,ylim[0]+dy), **kwargs)
            ax1.plot((xlim[1]-dx,xlim[1]+dx), (ylim[0]-dy,ylim[0]+dy), **kwargs)
            dy = .01*(ylim2[1]-ylim2[0])/ylim2ratio
            ax2.plot((xlim[0]-dx,xlim[0]+dx), (ylim2[1]-dy,ylim2[1]+dy), **kwargs)
            ax2.plot((xlim[1]-dx,xlim[1]+dx), (ylim2[1]-dy,ylim2[1]+dy), **kwargs)
            ax1.set_xlim(xlim)
            ax2.set_xlim(xlim)
            ax1.set_title(y)
            if save == True:
                af.automatic_graph_saver(folder=folder, name_file=y)
            plt.show()


#Normal box plot
def boxplot(data, x, categories, mae_data, lims=None, hue=None, size=None, 
            save=False, folder=None):
    for cat in categories:
        if cat in data.columns:
            
            #fig Size
            if size != None and type(size)==tuple:
                size=size
            else:
                size = (12, 10)
            
            
            #plot
            fig, ax = plt.subplots(figsize=size)
            box = sns.boxplot(data=data, x=x, y=cat, hue=hue, palette='Set2', ax=ax)
            swarm = sns.swarmplot(data=data, x=x, y=cat,hue=hue, palette='Set2', ax=ax)
            
            if lims!=None:
                plt.ylim(lims)
            plt.xlabel(eh.remove_under_score(x))
            ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right")
            plt.ylabel(eh.remove_under_score(cat))
            
            #stats
            stats = [boxplot_stats(data[data[x]==classif][cat])[0] for classif in data[x].unique().tolist()]
            dataframe_stats = pd.DataFrame.from_records(stats)
            dataframe_stats = dataframe_stats.drop(columns=['fliers', 'iqr', 'cilo', 'cihi']).transpose().round(2)
            
            if type(mae_data) == pd.core.frame.DataFrame:
                #stats_absoulte_data
                stats_2 = [boxplot_stats(mae_data[mae_data[x]==classsif][cat])[0] for classsif in data[x].unique().tolist()]
                dataframe_stats2 = pd.DataFrame.from_records(stats_2).round(2)
                dataframe_stats2 = dataframe_stats2['mean']
            
            #annotate
            texts = []
            for xtick in box.get_xticks():
                for row in range(len(dataframe_stats[xtick])):
                    texts.append(ax.text(xtick, dataframe_stats[xtick][row], f'{dataframe_stats.index[row]}:{dataframe_stats[xtick][row]}', 
                            horizontalalignment='left',
                                color='k', weight='semibold',fontsize=12, bbox=dict(facecolor='lightgray')))
                if type(mae_data) == pd.core.frame.DataFrame:
                    ax.text(xtick, data[cat].max()+0.01, f'MAE: {dataframe_stats2[xtick]}', horizontalalignment='center',
                            color='k', weight='semibold',fontsize=14)
            adjust_text(texts)
            if save == True:
                name = eh.name(cat)
                os.makedirs(f'{folder}', exist_ok=True)
                plt.savefig(f'{folder}/{name}.png')
            plt.title(cat)
            plt.show()
            
#Graph Barplot
def bar_plot(ci, data, x, categories, hue=None, size=None, lims=None, 
            save=False, folder=None):
    for cat in categories:
        if cat in data.columns:
            #fig Size
            if size != None:
                fig = plt.subplots(figsize=size)
            #Plots
            sns.barplot(data=data, x=x, y=cat, hue=hue, ci=ci, palette='Set2')
            if lims!=None:
                plt.ylim(lims)
            plt.xlabel(eh.remove_under_score(x))
            plt.ylabel(eh.remove_under_score(cat))
            plt.title(eh.remove_under_score(cat))
            if save == True:
                name = eh.name(cat)
                os.makedirs(f'{folder}', exist_ok=True)
                plt.savefig(f'{folder}/{name}.png')
            plt.show()

#Graph QQ-Plots
def qq_plot(data, classificators, categories, hue=None, 
            include=None, exclude=None,  save=False, folder=None):
    
    clasificadores = data[classificators].unique().tolist()
    #Combination 
    combinations = list()
    combinations += list(itertools.combinations(clasificadores, 2))
    #eliminate equal values combinations
    for comb in combinations:
        if comb[0]==comb[1]:
            combinations = combinations.pop(comb)
    
    #Just the combination containig this will remain
    if include != None:
        combinations = [comb for combs in combinations 
                        if include in combs]
    # all the combination containing this strig will be droped out.
    if exclude !=None:
        combinations = [combs for combs in combinations 
                        if exclude not in combs]

    #Data slicing
    for comb in combinations:
        x = data[data[classificators]==comb[0]]
        y = data[data[classificators]==comb[1]]
        #Columns iterations
        for cat in categories:
            if cat in data.columns.tolist():
                #hue classifiers
                if hue!=None: 
                    hue=x[hue]
                
                #Graph 
                sns.scatterplot(x=x[cat].tolist(), y=y[cat].tolist(), 
                                hue=hue, palette='Set1')
                plt.title(eh.remove_under_score(eh.name(cat)))
                if x[cat].max()>y[cat].max():
                    plt.plot([0, x[cat].max()], [0, x[cat].max()], linewidth=2)
                else:
                    plt.plot([0, y[cat].max()], [0, y[cat].max()], linewidth=2)
                plt.xlabel(eh.remove_under_score(x[classificators].unique()[0]))
                plt.ylabel(eh.remove_under_score(y[classificators].unique()[0]))
                if save==True:
                    name1 = eh.standard_name(str(comb))
                    name2 = eh.name(cat)
                    os.makedirs(f'{folder}/{name1}', exist_ok=True)
                    plt.savefig(f'{folder}/{name1}/{name2}.png')
                plt.show()

# QQ plots in comparison
def qq_plot_comparison(data, classificators, categories, include_comp,  hue=None, 
                        exclude=None,  save=False, folder=None):
    #Variables list
    classificators_list = data[classificators].unique().tolist()
    #list without the comparison method
    classificators_list = [classif for classif in classificators_list 
                            if classif != include_comp]
    # all the combination containing this strig will be droped out.
    if exclude !=None:
        classificators_list = [clasiff for clasiff in classificators_list 
                                if exclude not in classificators_list]
    for cat in categories:
        if cat in data.columns.tolist():
            #Initialize subplots
            fig, axes = plt.subplots(nrows=1, ncols=len(classificators_list), 
                                        figsize=(25, 15))
            #title of plot
            fig.suptitle(eh.remove_under_score(cat) , 
                            fontweight = "bold")
            #Data slicing and selection
            for i, classif in enumerate(classificators_list):
                x = data[data[classificators]==include_comp][cat]
                y = data[data[classificators]==classif][cat]
                
                # Need to add a len of lists
                
                #hue classifiers
                if hue!=None: 
                    hue=x[hue]
                #Graph 
                sns.scatterplot(x=x.tolist(), y=y.tolist(), 
                                hue=hue, palette='Set2', ax=axes[i])
                #Plot diagonal line
                if x.max() > y.max():
                    axes[i].plot([0, x.max()], [0, x.max()], linewidth=2)
                else:
                    axes[i].plot([0, y.max()], [0, y.max()], linewidth=2)
                    
                axes[i].set_xlabel(eh.remove_under_score(include_comp))
                axes[i].set_ylabel(eh.remove_under_score(classif))
                if save==True:
                    name = eh.name(cat)
                    os.makedirs(f'{folder}/comparison', exist_ok=True)
                    plt.savefig(f'{folder}/comparison/{name}.png')
            plt.show()


# QQ plot compiler
def qq_plot_report(data, classificators, categories, include_comp='', hue=None, include=None, 
                    exclude=None,  save=False, folder=None):
    if include_comp != '':
        qq_plot_comparison(data=data, classificators=classificators, categories=categories, 
                    include_comp=include_comp,  hue=hue,  exclude=exclude,  
                    save=save, folder=folder)
    else:
        qq_plot(data=data, classificators=classificators, categories=categories, 
            save=save, folder=folder)



#Pair plot. box plot that show the same result in both plots                
def pair_plot(data, x, cat,  pair, clasiff=None, save=False, folder=None):
    
    for i in cat:
        if i in data.columns.tolist():
            if clasiff != None:
                for j in data[clasiff].unique().tolist():
                    df = data[data[clasiff]==j]
                    ax = pg.plot_paired(data=df, dv=i, within=x,
                                    subject=pair)
                    plt.title(f'{i}/{j}')
                    if save==True:
                        name = eh.name(i)
                        os.makedirs(f'{folder}/{clasiff}_{j}', exist_ok=True)
                        plt.savefig(f'{folder}/{clasiff}_{j}/{name}.png')    
                    plt.show()
            else:
                pg.plot_paired(data=data, dv=i, within=x, 
                                subject=pair)
                plt.title(f'{i}')
                if save==True:
                    name = eh.name(i)
                    os.makedirs(f'{folder}/{clasiff}', exist_ok=True)
                    plt.savefig(f'{folder}/{clasiff}/{name}.png')    
                plt.show()


#funcion de distribucion (simil raincloudplot)
def distribution_plot(data, dx, dy, title=None ,hue=None, size = None, save=None, folder=None):
    fig, ax = plt.subplots(figsize=size)
    violin=sns.violinplot( x = dx, y = dy, data = data,  bw = .2, cut = 0., scale = "area", width = .6, inner = None, zorder = 0, ax=ax)
    strip=sns.stripplot( x = dx, y = dy, data = data, color='black', edgecolor = "white", size = 3, jitter = 1, zorder = 1, ax=ax)
    box=sns.boxplot( x = dx, y = dy, data = data, color = "grey", width = .3, zorder = 3, 
                    showcaps = True, boxprops = {'facecolor':'none', "zorder":4}, 
                    showfliers=True, whiskerprops = {'linewidth':2, "zorder":5}, saturation = 3, linewidth=3, ax=ax)
    
    #stats
    stats = [boxplot_stats(data[data[dx]==model][dy])[0] for model in data[dx].unique().tolist()]
    dataframe_stats = pd.DataFrame.from_records(stats)
    dataframe_stats = dataframe_stats.drop(columns=['fliers', 'iqr', 'cilo', 'cihi']).transpose().round(2)
    
    #annotate
    texts = []
    for xtick in box.get_xticks():
        for row in range(len(dataframe_stats[xtick])):
            if row==0:
                position='right'
            else:
                position='left'
            texts.append(ax.text(xtick, dataframe_stats[xtick][row], f'{dataframe_stats.index[row]}:{dataframe_stats[xtick][row]}', 
                    horizontalalignment=position, zorder = 6,
                        color='k', weight='semibold',fontsize=12, bbox=dict(facecolor='lightgray')))
    adjust_text(texts)
    plt.title(title)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right")
    if save!=None and folder!=None:
        title = eh.name(title)
        os.makedirs(f'{folder}', exist_ok=True)
        plt.savefig(f'{folder}/{title}.png')
    else:
        print('Save or folder does not contain the correct data')


def dist_plot(data, dx, dy, title=None ,hue=None, size=None, save=None, folder=None):
    if size!=None:
        fig_size = size
    else:
        fig_size = (12, 12)
    if type(dy) == list:
        for element in dy:
            if element in data.columns.tolist():
                distribution_plot(data=data, dx=dx, dy=element, title=element ,hue=hue, size=fig_size, save=save, folder=folder)
    else:
        distribution_plot(data=data, dx=dx, dy=dy, title=title ,hue=hue, size=fig_size, save=save, folder=folder)
    plt.show()

#outliers plot
def outliers_comp_graph(data, classificators, categories, include_comp, identifier, 
                    legend=True , ransac=True, save=False, folder=None):
    outliers = pd.DataFrame(columns=['Cat', 'id', 'R_Method', 'Comp', 'Comp_name'])
    for cat in categories:
        if cat in data.columns.tolist() and include_comp in data[classificators].unique().tolist()  and len(data[cat].unique()) > 1:
            dataframe = data[[classificators, identifier, cat]]

            comp_list = [comp for comp in dataframe[classificators].unique().tolist() 
                            if comp != include_comp]

            fig, axes = plt.subplots(nrows=1, ncols=len(comp_list), figsize=(25, 15))
            #title of plot
            fig.suptitle(cat , fontweight = "bold")

            for i, comp in enumerate(comp_list):
                y = dataframe[dataframe[classificators]==include_comp][cat].array.reshape(-1, 1)
                X = dataframe[dataframe[classificators]==comp][cat].array.reshape(-1, 1)
                n = dataframe[dataframe[classificators]==comp][identifier].array.reshape(-1, 1)

                #linear model
                lr = linear_model.LinearRegression()
                lr.fit(X, y)
                r2_lr = r2_score(y, lr.predict(X)).round(2)

                # Robustly fit linear model with RANSAC algorithm
                ransac = linear_model.RANSACRegressor(max_trials=100000,)
                ransac.fit(X, y)
                r2_ransac = r2_score(y, ransac.predict(X)).round(2)
                inlier_mask = ransac.inlier_mask_
                outlier_mask = np.logical_not(inlier_mask)

                # Predict data of estimated models
                line_X = np.arange(X.min(), X.max())[:, np.newaxis]
                line_y = lr.predict(line_X)
                line_y_ransac = ransac.predict(line_X)
                
                if dataframe[cat].max() < 6:
                    overplot=0.25
                    overtext=-0.5
                    overtext2=-0.75
                    extended=1
                else:
                    overplot=0.5
                    overtext=-2
                    overtext2=-1
                    extended=3
                
                lw = 2
                #Graphs
                axes[i].scatter(X[inlier_mask], y[inlier_mask], color="yellowgreen", 
                                    marker=".", linewidth=3, label="Inliers")
                axes[i].scatter(X[outlier_mask], y[outlier_mask], color="red", 
                                    marker=".", linewidth=3, label="Outliers")
                axes[i].plot(line_X, line_y, color="navy", linewidth=lw, 
                                label="Linear regressor")
                axes[i].plot(line_X, line_y_ransac, color="orange", linewidth=lw, 
                                label="RANSAC regressor")
                
                #annotate
                annotate = []
                for x, y, sample in zip(X[outlier_mask], y[outlier_mask], n[outlier_mask]):
                    annotate.append(axes[i].annotate(sample[0], (x[0], y[0]+overplot), 
                                                        transform=axes[i].transAxes))
                    outliers = outliers.append({'Cat':cat, 'id':sample[0], 'R_Method':y[0], 
                                                'Comp':x[0], 'Comp_name':comp}, 
                                                ignore_index=True)
                adjust_text(annotate)
                if legend ==True:
                    axes[i].legend(loc="lower right")
                axes[i].text(0, overtext, f'linear regression: {r2_lr}', fontsize=14)
                if ransac == True:
                    axes[i].text(0, overtext2, f'RANSAC regression: {r2_ransac}', fontsize=14)
                axes[i].set_ylabel(include_comp)
                axes[i].set_xlabel(f"Method: {comp}")
                axes[i].set_ylim(0, dataframe[cat].max()+extended)
                axes[i].set_xlim(0, dataframe[cat].max()+extended)
                
                #saving file
                if save!=None and folder!=None:
                    title = eh.name(cat)
                    os.makedirs(f'{folder}/outliers_plot', exist_ok=True)
                    plt.savefig(f'{folder}/outliers_plot/{title}.png')
                
            plt.show()
    #Save table
    os.makedirs(f'{folder}', exist_ok=True)
    outliers.to_excel(f'{folder}/outliers.xlsx', index=False)
    return outliers

def histogram_plot(data, categories, hue, bins, kde=False, 
                save=True, folder=None):
    for cat in categories:
        if cat in data.columns.tolist():
            size = (25, 10)
            fig, ax = plt.subplots(figsize=size)
            sns.histplot(ax=ax, data=data, x=cat, hue=hue, kde=kde, 
                            multiple='layer', stat='count', bins=bins )
            for container in ax.containers:
                ax.bar_label(container)
            #plt.xticks(x_ticks_label(data, cat))
            title = eh.remove_under_score(cat)
            plt.title(f'Relative differences: {title}')
            
            if save==True:
                name = eh.name(cat)
                os.makedirs(f'{folder}/Differences_histogram', exist_ok=True)
                plt.savefig(f'{folder}/Differences_histogram/{name}.png')    
            
            plt.show()

#ticks generator
def x_ticks_label(df, cat):
    data = df[cat]
    min_sep = (data.min())/10
    max_sep = -abs((data.max())/10)

    origin_value = 0
    max_list=[]
    min_list=[]

    for i in range(10):
        if i==0:
            max_value = origin_value + max_sep
            min_value = min_sep
        else:
            max_value = max_list[-1] + max_sep
            min_value = min_list[-1] - min_sep
        max_list.append(round(max_value, 3))
        min_list.append(round(min_value, 3))

    max_list.append(0)
    full_range = min_list + max_list
    print(cat, list(sorted(set(full_range))))
    return list(sorted(set(full_range)))