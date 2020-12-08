# -*- coding: utf-8 -*-
"""
Created on Sun Nov  1 10:52:07 2020

@author: letti
"""

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import ticker as mtick
from bokeh.io import output_file, show
from bokeh.plotting import figure

from datetime import datetime



today=datetime.today()


cols=['Employee_Name','EmpID','Salary','Position','State','Zip','DOB','Sex'
      ,'MaritalDesc','CitizenDesc','HispanicLatino','RaceDesc','DateofHire'
      ,'DateofTermination','TermReason','EmploymentStatus','Department'
      ,'ManagerName','ManagerID','RecruitmentSource','PerformanceScore'
      ,'EngagementSurvey','EmpSatisfaction','SpecialProjectsCount'
      ,'LastPerformanceReview_Date','DaysLateLast30','Absences']

emps=pd.read_csv('..\data\input\cincinnati_employees.csv'
                 ,dtype={'SEX':'category','RACE':'category'
                         ,'DEPTNAME':'category','DEPTID':'str'
                         ,'POSITION_NBR':'str','JOBCODE':'str','GRADE':'str'}
                 ,parse_dates=['JOB_ENTRY_DT','HIRE_DATE'])

emps.columns=emps.columns.str.lower()




#change M and F to male and female
emps['sex']=emps.sex.apply(lambda x: 'Male' if x=='M' else 'Female')

#



















