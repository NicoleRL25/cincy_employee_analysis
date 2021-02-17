# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 19:49:06 2020

@author: letti
"""


import matplotlib.pyplot as plt
from matplotlib import ticker as mtick
from matplotlib.gridspec import GridSpec


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
    
    emps=emps.copy()
    emps_by_jobclass=emps_by_jobclass.copy()
    emps_ft_pt=emps_ft_pt.copy()
    emp_ages=emp_ages.copy()
    emps_race=emps_race.copy()
    emps_gender=emps_gender.copy()
    
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
    
    
    #ax displaying logo
    
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
    
    
    plot_employee_gender(emps_gender,ax6)
    
    
    fig.savefig('..\images\output\employee_snapshot.png')
    
    
    
def plot_gender_snapshot(job_class_by_gender_pct, emps_gender):
    
    
    
    fig=plt.figure(figsize=(14,8),constrained_layout=True)
    
    gs=GridSpec(3, 3, figure=fig)
    
    ax1=fig.add_subplot(gs[0,0])
    #ax2=fig.add_subplot(gs[1:,0])
    ax3=fig.add_subplot(gs[0:,1:])
    
    
    
    #plot of logo
    image=plt.imread('..\images\input\cincinnati_logo.png')
    ax1.imshow(image)
    
    #removes spines from headcount axis
    for spine in ax1.spines.keys():
        ax1.spines[spine].set_visible(False)
        
    
    ax1.set_xticks([])
    ax1.set_yticks([])
    
    #plot of job class by gender
    plot_job_class_gender(job_class_by_gender_pct, ax=ax3)
    
   # plot_employee_gender(emps_gender,ax=ax2)
    
    
    
    
    
def plot_protective_services_gender(protective_services_gender,
                                    ax=None,save_fig=False):
    
    protective_services_gender=protective_services_gender.copy()
    
    fig=plt.figure()
    
    if ax==None:
        ax=fig.add_subplot()
    
    
    protective_services_gender.plot.bar(stacked=True,rot=0,
                                          ax=ax,
                                          title='Gender of Protective Service '
                                          'Workers \nvs. General Workforce')
    
    protective_services_gender['Female'].plot(linestyle='--',
                                                color='gray', ax=ax,
                                                label='')
    
    
    ax.legend(bbox_to_anchor=(1,1))
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1))
        
    
    if save_fig:
        fig.savefig('..\images\output\protective_services_vs_general_gender.png',
                    bbox_inches = "tight")
        
        
def plot_employee_gender(emps_gender,ax=None,save_fig=False):
    
    fig=plt.figure()
    
    if ax==None:
        ax=fig.add_subplot()
    
    emps_gender.plot.pie(ax=ax,title='Employee Gender', autopct='%1.0f%%',
                         rot=0, wedgeprops={'width':.3}, pctdistance=.4)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1))
    ax.set_ylabel(None)
        
    if save_fig:
        fig.savefig('..\images\output\gender_ratio.png')
    
def plot_job_class_gender(job_class_by_gender_pct, ax=None,save_fig=False):
    """
    

    Parameters
    ----------
    job_class_by_gender_pct : df
        DataFrame of the.

    Returns
    -------
    saves figure.

    """

    fig=plt.figure(figsize=(9,7))
    
    if ax==None:
        ax=fig.add_subplot()
    
    job_class_by_gender_pct.plot.barh(stacked=True,cmap='tab20c',ax=ax
                                      ,title='Employees Segmented by '
                                      'EEO Job Category and Gender')
    ax.xaxis.set_major_formatter(mtick.PercentFormatter(1))
    ax.legend(bbox_to_anchor=(1.1,1))
    ax.axvline(x=.5, color='red')
    ax.set_ylabel('EEO Job Category')
    
    if save_fig:
        fig.savefig('..\images\output\employee_job_cat_gender.png',
                    bbox_inches='tight')
    

def plot_leader_gender(leadership_by_gender_pct,ax = None,save_fig=False):
    """
    

    Parameters
    ----------
    job_class_by_gender : df
        DESCRIPTION.

    Returns
    -------
    None.

    """
    
    fig=plt.figure()
    
    if ax==None:
        ax=fig.add_subplot()
    
    leadership_by_gender_pct.loc[:,'Leadership'].plot.bar(ax=ax,
                                                          rot=0)                                                          
        
    ax.set_xlabel('Gender')
    
    ax.set_title('Leadership Representation')       
    
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1))  
    ax.patches[0].set_color('darkorange')
    ax.patches[1].set_color('gray')

    if save_fig:
        fig.savefig('..\images\output\leader_gender.png')
    
    
    
    
def plot_job_class_race(job_class_by_race_pct,ax = None,save_fig=False):

    
    fig=plt.figure(figsize=(9,7))
    
    if ax==None:
        ax=fig.add_subplot()
        
    job_class_by_race_pct.plot.barh(stacked=True,cmap='tab20c',ax=ax
                                      ,title='Employees Segmented by '
                                      'EEO Job Category and Race')
    ax.axvline(.48,color='red')
    ax.xaxis.set_major_formatter(mtick.PercentFormatter(1))
    ax.legend(bbox_to_anchor=(1.1,1))
    
    
    if save_fig:
        fig.savefig('..\images\output\job_class_race.png',
                    bbox_inches='tight')


def plot_top_job_titles(top_job_titles, ax=None, save_fig=False):
    
    fig=plt.figure()
    
    if ax==None:
        ax=fig.add_subplot()
    
    (top_job_titles.plot.barh(ax=ax,title='Top 10 Job Titles', 
                              color='silver'))
    ax.patches[9].set_color('blue')
    ax.patches[8].set_color('green')
    ax.patches[7].set_color('red')
    
    if save_fig:
        fig.savefig('..\images\output\job_titles.png')
        
        
def plot_racial_composition(race_counts,ax=None,save_fig=False):
    
    fig=plt.figure()
    
    if ax==None:
        ax=fig.add_subplot()
    
    percents=race_counts.div(race_counts.sum())
    percent_labels=['{:.2%}'.format(p) for p in percents]

    percents.plot.pie(radius=1,wedgeprops={'width':.3},
                      labels=percents.index + ': ' + percent_labels,
                      labeldistance=None,
                      cmap='Blues',ax=ax)
    
    ax.legend(bbox_to_anchor=(1,.75))    
    ax.set_title('Racial and Ethnic Composition of '
                 'Cincinnati\'s Municipal Workforce')
    ax.set_ylabel('Race')
    
    if save_fig:
        fig.savefig('..\images\output\emp_racial_composition.png',
                    bbox_inches='tight')
        
def plot_observed_vs_expected(df,ax=None,save_fig=False):
    
        
    fig=plt.figure(figsize=(10,6))
    
    if ax==None:
        ax=fig.add_subplot()
        
    df.plot.barh(ax=ax,title='Observed vs Expected',rot=0)
    
    ax.legend(['Observed','Expected'],
              bbox_to_anchor=(1,1))    
    ax.set_ylabel('Race')
    
    annotate_plot(ax.patches, ax)

    if save_fig:
        fig.savefig('..\images\output\observed_vs_expected.png',
                    bbox_inches='tight')
        
        
def annotate_plot(rects, ax,offset_text=True, horizontal=True):
    for p in rects:
        """
        offset_text: 
            True positions text at the end of the bar for the centered 
            stacked bar chart; False centers text

        horizontal:
            True indicates a horizontal bar chart; False is vertical

        """

        width=p.get_width() 
        height=p.get_height() 
        x=p.get_xy()[0] #gets the x coordinate of the bar
        y=p.get_xy()[1] #gets the y coordinate of the bar

        #if the text should be offset and not centered
        #variable sets the offset so it's negative if the width value is negative
        offset=0 if not offset_text else 15 if width >0 else -10 
        
        #sets the x-location to be centered if not offset
        x_loc=x+width/2 if not offset_text else x+width

        #converts width and height to string values
        horizontal_text='' if width ==0 else str(abs(int(width)))
        vertical_text ='' if height == 0 else str(abs(int(height)))
        
        text = horizontal_text if horizontal else vertical_text        
        
        ax.annotate(text,xy=(x_loc,y+height/2), 
                     xytext=(offset,0),
                    textcoords='offset points',
                    ha='center',va='center')
