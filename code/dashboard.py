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
                 ,dtype={'SEX':'category'
                         ,'RACE':'category'
                         ,'DEPTNAME':'category','DEPTID':'str'
                         ,'POSITION_NBR':'str','JOBCODE':'str','GRADE':'str'}
                 ,parse_dates=['JOB_ENTRY_DT','HIRE_DATE'])


#create an ordered category type for age groups
cat_type = CategoricalDtype(categories=['UNDER 18','18-25','26-30','31-40'
                                        ,'41-50', '51-60', '61-70', 'OVER 70']
                            ,ordered=True)

emps['AGE_RANGE']=emps.AGE_RANGE.astype(cat_type)

emps.columns=emps.columns.str.lower()

#change M and F to male and female
emps['sex']=emps.sex.apply(lambda x: 'Male' if x=='M' else 'Female')

#consolidated race groups by assigning Chinese to the Asian/Pacific Islander
#assigned Torres Strait Islander Origin to Aboriginal/Torres Strait Island
#Formatted text to title case
emps['race']=emps.race.str.title()
emps['race']=emps['race'].str.replace('Chinese','Asian/Pacific Islander')
emps['race']=emps['race'].str.replace('Torres Strait Islander Origin'
                                      ,'Aboriginal/Torres Strait Island')

#calculate employee tenure and time in job in years
emps['tenure']=round((datetime.today()-emps.hire_date)/np.timedelta64(1,'Y'),2)



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
female_tenure=emps.loc[emps.sex=='Female','tenure'].copy()
male_tenure=emps.loc[emps.sex=='Male','tenure'].copy()

fig5,axes=plt.subplots(2,1,sharex=True)
sns.histplot(female_tenure,kde=True,ax=axes[0])
axes[0].set_title('Tenure for Female Employees')
sns.histplot(male_tenure,kde=True,ax=axes[1])
axes[1].set_title('Tenure for Male Employees')























