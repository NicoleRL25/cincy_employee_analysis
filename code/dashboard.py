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



#####Data Visualization


#what is the composition of the workforce?
emps_by_paygroup=emps.paygroup_label.value_counts(normalize=True)

fig,ax=plt.subplots(figsize=(5,8))
emps_by_paygroup.plot.pie(ax=ax,title='Employees by Pay Group',
                          cmap='twilight_shifted',radius=1.1,
                          autopct='%1.1f%%',
                          wedgeprops={'width':0.3},
                          startangle=45)
ax.set_ylabel(None)

#Employees in the General Pay Group make up approx. 48% of the workforce
#The 10 roles below account for roughly 50% of the employees in that group
#The majority are Parks/Recreation Program Leaders
fig1,ax1=plt.subplots()
(emps.loc[emps.paygroup_label=='General','business_title']
 .value_counts()[:10].sort_values()
 .plot.barh(ax=ax1,title='Top 10 General Job Titles',
            color='silver'))
ax1.patches[9].set_color('darkorange')


#The majority of employees are between 41 and 60 years of age
#plot of the age distribution
fig2,ax2=plt.subplots()
emps.age_range.value_counts(sort=False).plot.bar(ax=ax,
                                                 title='Age Distribution')
ax2.set_xticklabels(labels=ax2.get_xticklabels(),rotation='horizontal')

#The workforce is roughly 60% male
#plot of employee gender distribution
fig3,ax3=plt.subplots()
emps.sex.value_counts(normalize=True).plot.bar(ax=ax3,title='Employee Gender'
                                               ,rot=0)
ax3.yaxis.set_major_formatter(mtick.PercentFormatter(1))


#When looking at a breakdown of job category by gender, we see that there
#is an underrepresentation of women as Technicians, Skilled Craft Workers and 
#Protective Service Workers (Police and Firefighters)
job_class_by_gender=emps.pivot_table(index='eeo_job_class',values='name'
                                     , columns='sex',aggfunc='count')
                                     

job_class_by_gender_pct=job_class_by_gender.div(job_class_by_gender.sum(axis=1)
                                                ,axis=0)

fig8,ax8=plt.subplots(figsize=(9,7))
job_class_by_gender_pct.plot.barh(stacked=True,cmap='tab20c',ax=ax8
                                  ,title='Gender by Job Category')
ax8.xaxis.set_major_formatter(mtick.PercentFormatter(1))
ax8.legend(bbox_to_anchor=(1.1,1))


#plot of racial demographics
fig4,ax4=plt.subplots(figsize=(8,6))
emps.race.value_counts().plot.pie(cmap='tab20c',ax=ax4
                                  ,radius=1.5,wedgeprops={'width':.5}
                                  ,labeldistance=None
                                  ,autopct='%1.1f%%'
                                  ,pctdistance=1.2)
ax4.legend(bbox_to_anchor=(1.2,.75))
fig4.suptitle('Racial Demographics')

job_class_by_race=emps.pivot_table(index='eeo_job_class',values='name'
                                     , columns='race',aggfunc='count')


race_col_list=list(emps.race.value_counts().index)                                     

job_class_by_race_pct=job_class_by_race.div(job_class_by_race.sum(axis=1)
                                                ,axis=0)

job_class_by_race_pct=job_class_by_race_pct.reindex(columns=race_col_list)
fig9,ax9=plt.subplots(figsize=(9,7))
job_class_by_race_pct.plot.barh(stacked=True,cmap='tab20c',ax=ax9
                                  ,title='Gender by Job Category')
ax9.xaxis.set_major_formatter(mtick.PercentFormatter(1))
ax9.legend(bbox_to_anchor=(1.1,1))


#plots tenure
fig5,ax5=plt.subplots(3,1)
sns.histplot(emps.tenure,kde=True,ax=ax4)
ax5.set_title('Tenure Distribution')


#plot of salary distribution
fig6,ax6=plt.subplots()
sns.histplot(emps.annual_rt,kde=True,ax=ax6)
ax6.set_title('Salary Distribution')
ax6.set_xlabel('Salary')

#plot of full-time vs part-time employees
fig7,ax7=plt.subplots()
emps.full_time.value_counts(normalize=True).plot.pie(radius=1.3
                                                     ,ax=ax7
                                                     ,wedgeprops={'width':.3}
                                                     ,labeldistance=None
                                                     ,cmap='summer')
ax7.set_title('Full_Time vs Part-Time',pad=20)
ax7.set_ylabel('')
ax7.legend(bbox_to_anchor=(1.25,.65))




























