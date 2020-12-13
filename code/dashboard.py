# -*- coding: utf-8 -*-
"""
Created on Sun Nov  1 10:52:07 2020

@author: letti
"""

import numpy as np

import pandas as pd
from pandas.api.types import CategoricalDtype
import matplotlib.pyplot as plt
from matplotlib import ticker as mtick
import seaborn as sns
from bokeh.io import output_file, show
from bokeh.plotting import figure

from datetime import datetime



today=datetime.today()


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

emps['age_range']=emps.age_range.astype(cat_type)

#creates a dictionary to map eeo job codes 

eeo_dict={1:'Officials and Administrators',2:'Professionals',3:'Technicians'
          ,4:'Protective Service Workers',5:'Protective Service Workers'
          ,6:'Administrative Support',7:'Skilled Craft Workers'
          ,8:'Service-Maintenance'}

#maps the eeo codes to the text category
emps['eeo_job_class']=emps.eeo_job_group.map(eeo_dict).fillna('Uncategorized')

#change M and F to male and female
emps['sex']=emps.sex.apply(lambda x: 'Male' if x=='M' else 'Female')

#consolidated race groups by assigning Chinese to the Asian/Pacific Islander
#assigned Torres Strait Islander Origin to Aboriginal/Torres Strait Island
#Formatted text to title case
emps['race']=emps.race.str.title()
emps['race']=emps['race'].str.replace('Chinese','Asian/Pacific Islander')
emps['race']=emps['race'].str.replace('Torres Strait Islander Origin'
                                      ,'Aboriginal/Torres Strait Island')

#add a column for full time / part-time
emps['full_time']=emps.fte.apply(lambda x: 'Full-Time' 
                                       if x == 1 else 'Part-Time')

#calculate employee tenure and time in job in years
emps['tenure']=round((datetime.today()-emps.hire_date)/np.timedelta64(1,'Y'),2)


#convert salary to float
emps['annual_rt']=emps.annual_rt.str.replace(',','')
emps['annual_rt']=emps.annual_rt.astype('float')


#plot of the age distribution
fig,ax=plt.subplots()
emps.age_range.value_counts(sort=False).plot.bar(ax=ax,title='')
ax.set_xticklabels(labels=ax.get_xticklabels(),rotation='horizontal')


#plot of employee gender distribution
fig1,ax1=plt.subplots()
emps.sex.value_counts(normalize=True).plot.bar(ax=ax1,title='Employee Gender')
ax1.set_xticklabels(labels=ax1.get_xticklabels(),rotation='horizontal')
ax1.yaxis.set_major_formatter(mtick.PercentFormatter(1))


#plot of racial demographics
fig2,ax2=plt.subplots()
emps.race.value_counts().plot.pie(cmap='twilight_shifted',ax=ax2
                                  ,radius=1.5,wedgeprops={'width':.5}
                                  ,labeldistance=None
                                  ,title='Racial Demographics')
ax2.legend(bbox_to_anchor=(1.2,.75))


#review of job titles
number_of_job_titles=len(emps.jobtitle.value_counts().index)
emp_count=emps.jobtitle.value_counts().sum()

fig3,ax3=plt.subplots()
(emps.jobtitle.value_counts()[:15]
 .plot.barh(ax=ax3,title='Top 15 Jobs by Count'))
fig3.text(1,.5,'There are '+str(number_of_job_titles)+ ' job titles\n'
          + 'Filled by '+str(emp_count)+' employees')


#plots tenure
fig4,ax4=plt.subplots()
sns.histplot(emps.tenure,kde=True,ax=ax4)
ax4.set_title('Tenure Distribution')

#tenure by gender
tenure_by_gender=emps.pivot_table(values='tenure',columns='sex'
                                  ,index=emps.index)

fig5,axes=plt.subplots(2,1,sharex=True)
sns.histplot(tenure_by_gender['Female'],kde=True,ax=axes[0])
axes[0].set_title('Tenure for Female Employees')
sns.histplot(tenure_by_gender['Male'],kde=True,ax=axes[1])
axes[1].set_title('Tenure for Male Employees')
axes[1].set_xlabel('Tenure')


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




job_class_by_gender=emps.pivot_table(index='eeo_job_class',values='name'
                                     , columns='sex',aggfunc='count')
                                     

job_class_by_gender_pct=job_class_by_gender.div(job_class_by_gender.sum(axis=1)
                                                ,axis=0)

fig8,ax8=plt.subplots(figsize=(9,7))
job_class_by_gender_pct.plot.barh(stacked=True,cmap='tab20c',ax=ax8
                                  ,title='Gender by Job Category')
ax8.xaxis.set_major_formatter(mtick.PercentFormatter(1))
ax8.legend(bbox_to_anchor=(1.1,1))




#create plots and widgets


#add callbacks


#arrange plots and widgets in layouts


















