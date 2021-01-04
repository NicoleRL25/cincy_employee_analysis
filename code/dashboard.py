# -*- coding: utf-8 -*-
"""
Created on Sun Nov  1 10:52:07 2020

@author: letti
"""

import numpy as np
import statsmodels.api as sm

import pandas as pd
from pandas.api.types import CategoricalDtype
import matplotlib.pyplot as plt
from matplotlib import ticker as mtick
from matplotlib.gridspec import GridSpec
import seaborn as sns


from datetime import datetime



today=datetime.today()

#To-Do: Fix Racial Demographic Pie Chart


#read csv containing cincinnati employee data into a pandas dataframe
emps=pd.read_csv('..\data\input\cincinnati_employees.csv'
                 ,dtype={'SEX':'category' ,'RACE':'category'
                         ,'DEPTNAME':'category','DEPTID':'str'
                         ,'POSITION_NBR':'str','JOBCODE':'str','GRADE':'str'}
                 ,parse_dates=['JOB_ENTRY_DT','HIRE_DATE'])



#changes column names to lower case
emps.columns=emps.columns.str.lower()

#create an ordered category type for age groups
cat_type = CategoricalDtype(categories=['UNDER 18','18-25','26-30','31-40'
                                        ,'41-50', '51-60', '61-70', 'OVER 70']
                            ,ordered=True)

#casts the age_range as a categorical data type
emps['age_range']=emps.age_range.astype(cat_type)

#creates a dictionary to map eeo job codes to category names
eeo_dict={1:'Officials and Administrators',2:'Professionals',3:'Technicians'
          ,4:'Protective Service Workers',5:'Protective Service Workers'
          ,6:'Administrative Support',7:'Skilled Craft Workers'
          ,8:'Service-Maintenance'}


#maps the eeo codes to the text category
emps['eeo_job_class']=emps.eeo_job_group.map(eeo_dict).fillna('Uncategorized')

#creates a dictionary to map paygroups to a descriptive label
paygroup_dict={'GEN':'General','MGM':'Management','POL':'Police',
               'FIR':'Fire Department','CCL':'City Council'}

#maps the paygroup to a label
emps['paygroup_label']=emps.paygroup.map(paygroup_dict).fillna('Uncategorized')

#change M and F to male and female
emps['sex']=emps.sex.apply(lambda x: 'Male' if x=='M' else 'Female')

#consolidated race groups by assigning Chinese to the Asian/Pacific Islander 
#group and assigned Torres Strait Islander Origin to Aboriginal/Torres Strait 
#Island
#Formatted text to title case
emps['race']=emps.race.str.title()
emps['race']=emps['race'].str.replace('Chinese','Asian/Pacific Islander')
emps['race']=emps['race'].str.replace('Torres Strait Islander Origin'
                                      ,'Aboriginal/Torres Strait Island')

#add a column for full time / part-time based on FTE column
emps['full_time']=emps.fte.apply(lambda x: 'Full-Time' 
                                       if x == 1 else 'Part-Time')

#calculate employee tenure and time in job in years
emps['tenure']=round((datetime.today()-emps.hire_date)/np.timedelta64(1,'Y'),2)


#convert salary to float
emps['annual_rt']=emps.annual_rt.str.replace(',','')
emps['annual_rt']=emps.annual_rt.astype('float')



#####Employee Snapshot Data Visualization#####

fig = plt.figure(figsize=(11,8),constrained_layout=True)
fig.suptitle('City of Cincinnati Employee Snapshot')
gs=GridSpec(3,3,figure=fig)

#axis for headcount text
ax1=fig.add_subplot(gs[0,0])

#axis for full vs part-time
ax2=fig.add_subplot(gs[0,1])

#axis for emps by job category
ax3=fig.add_subplot(gs[:3,-1])

#axis for age distribution
ax4=fig.add_subplot(gs[2,:-1])

#race
ax5=fig.add_subplot(gs[1,0])

#gender
ax6=fig.add_subplot(gs[1,1])


#text plot displaying total employee count

image=plt.imread('cincinnati_logo.png')
ax1.imshow(image)

#removes spines from headcount axis
for spine in ax1.spines.keys():
    ax1.spines[spine].set_visible(False)
    

ax1.set_xticks([])
ax1.set_yticks([])


#plot of full-time vs part-time employees
emps.full_time.value_counts(normalize=True).plot.pie(radius=1,
                                                     ax=ax2,
                                                     wedgeprops={'width':.3},
                                                     labels=['FT','PT'],
                                                    # labeldistance=1.25,
                                                     cmap='tab20c')
                                                     
ax2.set_ylabel('')
ax2.text(0,0.1,'Total\nHeadcount: \n'+str(len(emps)),
                                           horizontalalignment='center',
                                           verticalalignment='center')



#plot of the workforce composition by eeo job category
emps_by_jobclass=emps.eeo_job_class.value_counts(normalize=True).sort_values()

emps_by_jobclass.plot.barh(ax=ax3,title='Employees by Job Class',
                          color='silver')


#to wrap tick labels use the get_text method of the label text to pass the text
#to a list while replacing spaces with the \n for new line
#pass the new list to set the tick labels
wrapped_labels=[label.get_text().replace(' ','\n').replace('-','\n') 
                for label in ax3.get_yticklabels()]    
    
ax3.set_yticklabels(wrapped_labels)
ax3.patches[-1].set_color('darkorange')
ax3.xaxis.set_major_formatter(mtick.PercentFormatter(1))


emps.age_range.value_counts(sort=False).plot.bar(ax=ax4,
                                                 title='Age Distribution',
                                                 rot=0)


emps_by_race=emps.race.value_counts().sort_values()
emps_by_race.index=['Aboriginal+','American Indian+','Unknown','Hispanic+',
                    'Asian+','Black','White']
emps_by_race.plot.barh(width=.05,ax=ax5,title='Racial Demographics')
wrapped_labels=[label.get_text().replace('//','\n') 
                for label in ax5.get_yticklabels()]

ax5.plot(emps_by_race.values, emps_by_race.index,
         marker='o', linestyle='',alpha=0.8, color="orange")

ax5.set_yticklabels(wrapped_labels)




emps.sex.value_counts(normalize=True).plot.pie(ax=ax6,title='Employee Gender',
                                               autopct='%1.0f%%',rot=0,
                                               wedgeprops={'width':.3})
ax6.yaxis.set_major_formatter(mtick.PercentFormatter(1))
ax6.set_ylabel(None)


fig.savefig('..\docs\employee_snapshot.pdf')


         

#are women and men equally represented at the management level?
#28% of female and 19% of male employees are in management positions
count_women=emps.sex.value_counts()['Female']
count_men=emps.sex.value_counts()['Male']
female_mgrs=(emps.loc[emps.eeo_job_class=='Officials and Administrators']
                        .sex.value_counts()['Female'])
male_mgrs=(emps.loc[emps.eeo_job_class=='Officials and Administrators']
                         .sex.value_counts()['Male'])


successes=np.array([female_mgrs,male_mgrs])
samples=np.array([count_women,count_men])

p_value=sm.stats.proportions_ztest(successes,samples,alternative='larger')[1]

if p_value<0.05:
    print('We reject the null hypothesis that women and men are represented'
          ' equally at the management level')
else:
    print('We fail to reject the null hypothesis that women are in management '
          'at a rate equal to men')

#does this hypotheis hold when we exclude part-time employees?
fte_by_job_class=(emps.loc[emps.full_time=='Full-Time']
                 .pivot_table(index='eeo_job_class',columns='sex',
                              values='name',aggfunc='count',margins=True))


count_women_full_time=fte_by_job_class.loc[('All','Female')]


full_time_female_mgrs=fte_by_job_class.loc[('Officials and Administrators'
                                           ,'Female')]

count_men_full_time=fte_by_job_class.loc[('All','Male')]

full_time_male_mgrs=fte_by_job_class.loc[('Officials and Administrators'
                                          ,'Male')]

successes=np.array([full_time_female_mgrs,full_time_male_mgrs])

samples=np.array([count_women_full_time,count_men_full_time])

p_value=sm.stats.proportions_ztest(successes,samples,alternative='larger')[1]

print(sm.stats.proportions_ztest(successes,samples,alternative='larger')[0])




if p_value<0.05:
    print('We reject the null hypothesis that women and men are represented'
          ' equally at the management level')
else:
    print('We fail to reject the null hypothesis that women '
          ' are in management levels at a rate equal to men')


#Police Officers and Parks/Recreation Program Leaders are the largest job 
#roles. Followed by Fire Fighters
fig1,ax1=plt.subplots()
(emps.business_title.value_counts()[:10].sort_values()
 .plot.barh(ax=ax1,title='Top 10 Job Titles',
            color='silver'))
ax1.patches[9].set_color('blue')
ax1.patches[8].set_color('green')
ax1.patches[7].set_color('red')




#When looking at a breakdown of job category by gender, we see that there
#is an underrepresentation of women as Technicians, Skilled Craft Workers and 
#Protective Service Workers (Police and Firefighters)
#and an overrepresentation in administrative support
job_class_by_gender=emps.pivot_table(index='eeo_job_class',values='name'
                                     , columns='sex',aggfunc='count')
                                     

job_class_by_gender_pct=job_class_by_gender.div(job_class_by_gender.sum(axis=1)
                                                ,axis=0)

fig4,ax4=plt.subplots(figsize=(9,7))
job_class_by_gender_pct.plot.barh(stacked=True,cmap='tab20c',ax=ax4
                                  ,title='Gender by Job Category')
ax4.xaxis.set_major_formatter(mtick.PercentFormatter(1))
ax4.legend(bbox_to_anchor=(1.1,1))
ax4.axvline(x=.5, color='red')




job_class_by_race=emps.pivot_table(index='eeo_job_class',values='name'
                                     , columns='race',aggfunc='count')


race_col_list=list(emps.race.value_counts().index)                                     

job_class_by_race_pct=job_class_by_race.div(job_class_by_race.sum(axis=1)
                                                ,axis=0)

job_class_by_race_pct=job_class_by_race_pct.reindex(columns=race_col_list)
fig6,ax6=plt.subplots(figsize=(9,7))
job_class_by_race_pct.plot.barh(stacked=True,cmap='tab20c',ax=ax6
                                  ,title='Race by Job Category')
ax6.xaxis.set_major_formatter(mtick.PercentFormatter(1))
ax6.legend(bbox_to_anchor=(1.1,1))


#plots tenure
fig7,ax7=plt.subplots()
sns.histplot(emps.tenure,kde=True,ax=ax7)
ax7.set_title('Tenure Distribution')


#plot of salary distribution
fig8,ax8=plt.subplots()
sns.histplot(emps.annual_rt,kde=True,ax=ax8)
ax8.set_title('Salary Distribution')
ax8.set_xlabel('Salary')






























