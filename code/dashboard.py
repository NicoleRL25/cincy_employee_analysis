# -*- coding: utf-8 -*-
"""
Created on Sun Nov  1 10:52:07 2020

@author: letti
"""

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import ticker as mtick
from datetime import datetime


today=datetime.today()


cols=['Employee_Name','EmpID','Salary','Position','State','Zip','DOB','Sex'
      ,'MaritalDesc','CitizenDesc','HispanicLatino','RaceDesc','DateofHire'
      ,'DateofTermination','TermReason','EmploymentStatus','Department'
      ,'ManagerName','ManagerID','RecruitmentSource','PerformanceScore'
      ,'EngagementSurvey','EmpSatisfaction','SpecialProjectsCount'
      ,'LastPerformanceReview_Date','DaysLateLast30','Absences']

emps=pd.read_csv('..\data\input\hr_dataset_v14.csv',usecols=cols
                 ,dtype={'EmpID':'str','Zip':'str','Sex':'category'
                         ,'MaritalDesc':'category','CitizenDesc':'category'
                         ,'RaceDesc':'category','Department':'category'}
                 ,parse_dates=['DOB','DateofHire','DateofTermination'
                               ,'LastPerformanceReview_Date'])


#replaces M and F with Male and Female
emps['Sex']=(emps.Sex.str.strip().str.replace(r'F\b','Female',regex=True)
.str.replace(r'M\b','Male',regex=True))


emps['HispanicLatino']=emps.HispanicLatino.str.title()

active_emps=emps.loc[emps.EmploymentStatus=='Active'].copy()

active_emps['tenure']=(active_emps.DateofHire
           .apply(lambda x: today.year - x.year
           -((today.month,today.day)<(x.month,x.year))))


emps_by_department_race_gender=(active_emps
                                .pivot_table(index=['Department','RaceDesc']
                                ,columns='Sex',values='EmpID',aggfunc='count'))



fig1,ax1=plt.subplots(figsize=(5,7))


active_emps.Department.value_counts().plot.pie(radius=1
                                   ,autopct=lambda p: f'{p:.1f}%'
                                   ,labels=None
                                   ,cmap='tab20c'
                                   ,wedgeprops={'width':.2}
                                   ,title='Employees by Department'
                                   ,ax=ax1)



ax1.legend(bbox_to_anchor=(1.1,1)
,labels=active_emps.Department.value_counts().index)



fig2,ax2=plt.subplots(figsize=(5,7))
(active_emps.Sex.value_counts(normalize=True)
.plot.bar(cmap='tab20c',title='Employee Gender',ax=ax2))

ax2.set_xticklabels(ax2.get_xticklabels(),rotation='horizontal')
ax2.yaxis.set_major_formatter(mtick.PercentFormatter(1))



fig3,ax3=plt.subplots()
active_emps.tenure.plot.hist(ax=ax3,title='Employee Tenure')
ax3.set_xlabel('Tenure (in Years)')
fig3.text(1,.5,'The average tenure is '
          +str(int(active_emps.tenure.mean()))+ ' years')


fig4,ax4=plt.subplots(figsize=(6,7))
(active_emps.RaceDesc.value_counts(normalize=True)
.plot.pie(radius=1.1,autopct='%.1f%%',cmap='twilight',ax=ax4
          ,labels=None,wedgeprops={'width':.3}))









