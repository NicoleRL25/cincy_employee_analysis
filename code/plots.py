# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 19:49:06 2020

@author: letti
"""


import matplotlib.pyplot as plt
from matplotlib import ticker as mtick
from matplotlib.gridspec import GridSpec
import seaborn as sns


def plot_employee_snapshot(emps,emps_by_jobclass, emps_ft_pt, emp_ages,
                           emps_race, emps_gender):
    
    """
        Plots the cleaned Cincinnati employee list as a GridSpec with an 
        overview of the employee demographics
    
        Returns
        -------
        fig : Figure
            figure of a GridSpec object
    
    """
    
    fig = plt.figure(figsize=(11,8),constrained_layout=True)
    fig.suptitle('City of Cincinnati Employee Snapshot')
    gs=GridSpec(3,3,figure=fig)
    
    #axis for logo
    ax1=fig.add_subplot(gs[0,0])
    
    #axis for full vs part-time
    ax2=fig.add_subplot(gs[0,1])
    
    #axis for emps by job category
    ax3=fig.add_subplot(gs[:,-1])
    
    #axis for age distribution
    ax4=fig.add_subplot(gs[2,:-1])
    
    #axis for racial demographics
    ax5=fig.add_subplot(gs[1,0])
    
    #axis for gender
    ax6=fig.add_subplot(gs[1,1])
    
    
    #text plot displaying total employee count
    
    image=plt.imread('..\images\input\cincinnati_logo.png')
    ax1.imshow(image)
    
    #removes spines from headcount axis
    for spine in ax1.spines.keys():
        ax1.spines[spine].set_visible(False)
        
    
    ax1.set_xticks([])
    ax1.set_yticks([])
    
    
    #plot of full-time vs part-time employees
    emps_ft_pt.plot.pie(radius=1, ax=ax2, wedgeprops={'width':.3},
                        labels=['FT','PT'],cmap='tab20c')
                                                         
    ax2.set_ylabel('')
    ax2.text(0,0.1,'Total\nHeadcount: \n'+str(len(emps)),
                                               horizontalalignment='center',
                                               verticalalignment='center')
        
    
    
    emps_by_jobclass.plot.barh(ax=ax3,title='Employees by EEO Job Category',
                              color='silver')
    
    
    #to wrap tick labels use the get_text method of the label text to pass the text
    #to a list while replacing spaces with the \n for new line
    #pass the new list to set the tick labels
    wrapped_labels=[label.get_text().replace(' ','\n').replace('-','\n') 
                    for label in ax3.get_yticklabels()]    
        
    ax3.set_yticklabels(wrapped_labels)
    ax3.patches[-1].set_color('darkorange')
    ax3.xaxis.set_major_formatter(mtick.PercentFormatter(1))
    
    
    emp_ages.plot.bar(ax=ax4, title='Age Distribution', rot=0)
    
    
    
    emps_race.index=['Aboriginal+','American Indian+','Unknown','Hispanic+',
                        'Asian+','Black','White']
    emps_race.plot.barh(width=.05,ax=ax5,title='Racial Demographics')
    wrapped_labels=[label.get_text().replace('//','\n') 
                    for label in ax5.get_yticklabels()]
    
    ax5.plot(emps_race.values, emps_race.index,
             marker='o', linestyle='',alpha=0.8, color="orange")
    
    ax5.set_yticklabels(wrapped_labels)
    
    
    
    
    emps_gender.plot.pie(ax=ax6,title='Employee Gender', autopct='%1.0f%%',
                         rot=0, wedgeprops={'width':.3}, pctdistance=.4)
    ax6.yaxis.set_major_formatter(mtick.PercentFormatter(1))
    ax6.set_ylabel(None)
    
    
    fig.savefig('..\images\output\employee_snapshot.png')
    
    
def plot_protective_services_gender(protective_services_gender):
    
    protective_services_gender=protective_services_gender.copy()
    
    fig,ax=plt.subplots()
    
    protective_services_gender.plot.bar(stacked=True,rot=0,
                                          ax=ax,
                                          title='Gender of Protective Service '
                                          'Workers \nvs. General Workforce')
    
    protective_services_gender['Female'].plot(linestyle='--',
                                                color='gray', ax=ax,
                                                label='')
    
    
    ax.legend(bbox_to_anchor=(1,1))
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1))
        
    
    fig.savefig('..\images\output\protective_services_vs_general_gender.png',
                bbox_inches = "tight")
    
    
    
def plot_job_class_gender(job_class_by_gender_pct):
    """
    

    Parameters
    ----------
    job_class_by_gender_pct : df
        DataFrame of the.

    Returns
    -------
    saves figure.

    """

   
    fig,ax=plt.subplots(figsize=(9,7))
    job_class_by_gender_pct.plot.barh(stacked=True,cmap='tab20c',ax=ax
                                      ,title='Employees Segmented by '
                                      'EEO Job Category and Gender')
    ax.xaxis.set_major_formatter(mtick.PercentFormatter(1))
    ax.legend(bbox_to_anchor=(1.1,1))
    ax.axvline(x=.5, color='red')
    
    fig.savefig('..\images\output\employee_job_cat_gender.png')
    

def plot_leader_gender(leadership_by_gender_pct):
    """
    

    Parameters
    ----------
    job_class_by_gender : df
        DESCRIPTION.

    Returns
    -------
    None.

    """

    fig,ax=plt.subplots()
    sns.pointplot(x='Org Level',y='Percent',hue='sex',
                  data=leadership_by_gender_pct,ax=ax,
                  palette=sns.color_palette(['tab:orange','tab:blue']))
        
    ax.set_title('Leadership Representation: Gender')       
    
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1))  

    fig.savefig('..\images\output\leader_gender.png')
    
    
def plot_job_class_race(job_class_by_race_pct):

    
    fig,ax=plt.subplots(figsize=(9,7))
    job_class_by_race_pct.plot.barh(stacked=True,cmap='tab20c',ax=ax
                                      ,title='Employees Segmented by '
                                      'EEO Job Category and Race')
    ax.xaxis.set_major_formatter(mtick.PercentFormatter(1))
    ax.legend(bbox_to_anchor=(1.1,1))
    
    fig.savefig('..\images\output\job_class_race.png')


def plot_top_job_titles(top_job_titles):
    
    
    fig,ax=plt.subplots()
    (top_job_titles.plot.barh(ax=ax,title='Top 10 Job Titles', 
                              color='silver'))
    ax.patches[9].set_color('blue')
    ax.patches[8].set_color('green')
    ax.patches[7].set_color('red')
    
    
    fig.savefig('..\images\output\job_titles.png')
    
        
