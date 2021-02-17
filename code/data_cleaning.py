# -*- coding: utf-8 -*-
"""
Created on Sun Jan 10 09:12:02 2021

@author: letti
"""

import pandas as pd
from pandas.api.types import CategoricalDtype
import numpy as np


from datetime import datetime



def clean_emp_list(file_name=None):
    """
    Reads the cincinnati employee csv file and outputs a clean file

    Returns
    -------
    None.

    """
    if file_name==None:
        file_name='..\data\input\cincinnati_employees.csv'
        
    today=datetime.today()


    try:
        
        #read csv containing cincinnati employee data into a pandas dataframe
        emps=pd.read_csv(file_name,
                         dtype={'SEX':'category' ,'RACE':'category',
                                 'DEPTNAME':'category','DEPTID':'str',
                                 'POSITION_NBR':'str','JOBCODE':'str',
                                 'GRADE':'str'},
                         parse_dates=['JOB_ENTRY_DT','HIRE_DATE'])
    
    
        #changes column names to lower case
        emps.columns=emps.columns.str.lower()
        
        #create an ordered category type for age groups
        cat_type = CategoricalDtype(categories=['UNDER 18','18-25','26-30',
                                                '31-40','41-50','51-60', 
                                                '61-70', 'OVER 70'],
                                    ordered=True)
        
        #casts the age_range as a categorical data type
        emps['age_range']=emps.age_range.astype(cat_type)
        
        #creates a dictionary to map eeo job codes to category names
        eeo_dict={1:'Officials and Administrators',2:'Professionals',
                  3:'Technicians' ,4:'Protective Service Workers',
                  5:'Protective Service Workers' ,6:'Administrative Support',
                  7:'Skilled Craft Workers',8:'Service-Maintenance'}
        
        
        #maps the eeo codes to the text category
        emps['eeo_job_class']=(emps.eeo_job_group.map(eeo_dict)
                               .fillna('Uncategorized'))
        
        #creates a dictionary to map paygroups to a descriptive label
        paygroup_dict={'GEN':'General','MGM':'Management','POL':'Police',
                       'FIR':'Fire Department','CCL':'City Council'}
        
        #maps the paygroup to a label
        emps['paygroup_label']=(emps.paygroup.map(paygroup_dict)
                                .fillna('Uncategorized'))
        
        #change M and F to male and female
        emps['sex']=emps.sex.apply(lambda x: 'Male' if x=='M' else 'Female')
        
        #consolidated race groups by assigning Chinese to the 
        #Asian/Pacific Islander group and assigned Torres Strait Islander 
        #Origin to Aboriginal/Torres Strait Island
        #Formatted text to title case
        emps['race']=emps.race.str.title()
        emps['race']=emps['race'].str.replace('Chinese',
                                              'Asian/Pacific Islander')
        emps['race']=emps['race'].str.replace('Torres Strait Islander Origin',
                                              'Aboriginal/Torres Strait Island')
        
        #add a column for full time / part-time based on FTE column
        emps['full_time']=emps.fte.apply(lambda x: 'Full-Time' 
                                               if x == 1 else 'Part-Time')
        
        #calculate employee tenure and time in job in years
        emps['tenure']=round((today-emps.hire_date)/np.timedelta64(1,'Y'),2)
        
        
        #convert salary to float
        emps['annual_rt']=emps.annual_rt.str.replace(',','')
        emps['annual_rt']=emps.annual_rt.astype('float')
        

                       
        
        return emps
        
    
    except Exception as e:
        print(e)
        
        
def save_emp_list(emps):
    """
    outputs cleaned file to output folder

    """
    try:
        
        emps.to_csv('..\data\output\cleaned_cincy_emp_list.csv',index=False)

    
    except Exception as e:
        print(e)
        
    
def get_data_for_plots(emps):
    
    data_dict={}
    race_categories=['White','Black','Asian/Pacific Islander', 'Hispanic',
                 'American Indian/Alaskan Native']
    
    emps=emps.copy()
    
    if emps.empty:
        pass
    
    else:
        
        race_df=emps.loc[emps.race.isin(race_categories)].copy()
        
        data_dict['race_df']=race_df
        
        #Creates list of eeo job classes
        eeo_job_classes=list(emps.eeo_job_class.unique())
        
        #Copies list of eeo job classes and removes officials
        emps_non_officials=eeo_job_classes.copy()
        emps_non_officials.remove('Officials and Administrators')
        
        
        #Copies list of eeo job classes and removes protective service workers
        emps_non_protective=eeo_job_classes.copy()
        emps_non_protective.remove('Protective Service Workers')
        
        #counts of full-time and part time employees
        emps_ft_pt=emps.full_time.value_counts(normalize=True)
        data_dict['full_time']=emps_ft_pt
    
        #counts by age group       
        emp_ages=emps.age_range.value_counts(sort=False)
        data_dict['age_groups']=emp_ages
        
        #counts by race
        emps_race=emps.race.value_counts().sort_values()
        data_dict['race']=emps_race
        
        #percent of employees by gender
        emps_gender=emps.sex.value_counts(normalize=True)
        data_dict['gender']=emps_gender
        
                
        #percent of employees by job class
        emps_by_jobclass=(emps.eeo_job_class.value_counts(normalize=True)
                          .sort_values())
        data_dict['job_class']=emps_by_jobclass
        
        #count of employees in each job class segmented by gender
        job_class_by_gender=emps.pivot_table(index='eeo_job_class',
                                             values='name',columns='sex',
                                             aggfunc='count')
        data_dict['jobs_by_gender']=job_class_by_gender
                                             
        #percent of employees in each job class segmented by gender
        job_class_by_gender_pct=job_class_by_gender.div(job_class_by_gender
                                                        .sum(axis=1), axis=0)
        data_dict['jobs_by_gender_pct']=job_class_by_gender_pct
    
              
        
        #gets the total of employees in non-leadership roles
        emps_non_official=(job_class_by_gender.loc[emps_non_officials].copy()
                           .sum())
        
        emps_officials=(job_class_by_gender.loc['Officials and Administrators']
                        .copy())
        
        #count of employees in leadership and non-leadership roles
        #segmented by gender
        leadership_by_gender=(pd.concat([emps_non_official,emps_officials],
                                        axis=1)
                              .rename(columns={0:'Non-Leadership',
                                               'Officials and Administrators':
                                                   'Leadership'}))
        data_dict['leaders_by_gender']=leadership_by_gender
            
        #percent of employees in leadership and non-leadership roles
        #segmented by gender
        leadership_by_gender_pct=(leadership_by_gender
                                  .div(leadership_by_gender.sum()))

        data_dict['leaders_by_gender_pct']=leadership_by_gender_pct
        
        
        
        emps_non_protective_df=job_class_by_gender.loc[emps_non_protective]
        emps_protective_df=job_class_by_gender.loc['Protective Service Workers']

        protective_vs_general=(pd.concat([emps_protective_df,
                                     emps_non_protective_df.sum()],
                                     axis=1)
                       .rename(columns=({0:'General Workforce'})))
        
        data_dict['pro_vs_general_gender']=protective_vs_general.T
        
        protective_vs_general_gender_pct=(protective_vs_general
                                      .div(protective_vs_general.sum(),axis=1))
        
        data_dict['pro_vs_gen_gender_pct']=protective_vs_general_gender_pct.T
        
        gender_police_fire=(emps.pivot_table(index='paygroup_label',
                                            columns='sex',values='name',
                                            aggfunc='count')
                            .loc[['Fire Department','Police']])
        
        data_dict['gender_police_fire']=gender_police_fire
        
        
        #count of employees in each job class segmented by race
        job_class_by_race=emps.pivot_table(index='eeo_job_class',
                                           values='name', columns='race',
                                           aggfunc='count')
        
        data_dict['job_class_race']=job_class_by_race
        
        race_col_list=list(emps.race.value_counts().index)                                     

        #percent of employees in each job class segmented by race
        job_class_by_race_pct=(job_class_by_race
                               .div(job_class_by_race.sum(axis=1)
                                                        ,axis=0))
        
        job_class_by_race_pct=(job_class_by_race_pct
                               .reindex(columns=race_col_list))
        
        data_dict['job_class_race_pct']=job_class_by_race_pct

        #count of the top 10 most frequent job titles
        top_job_titles=emps.business_title.value_counts()[:10].sort_values()
        
        data_dict['top_jobs']=top_job_titles
        
        data_dict['cincy_race_demos']=get_cincinnati_racial_demographics()
        
        expected_counts=(round(data_dict['cincy_race_demos']['expected']
                               *data_dict['race_df'].race.value_counts()
                               .sum(),0))
        
        
        observed_counts=(data_dict['race_df'].race.value_counts()
                         .rename("observed"))
        
        
        
        data_dict['chi_square']=(pd.concat([observed_counts,
                                           expected_counts],axis=1)
                                 .sort_values(by='expected'))
        
        data_dict['chi_square']['std_residual']=(data_dict['chi_square']
                                             .apply(lambda x: (x.observed
                                                               -x.expected)
                                                    /np.sqrt(x.expected),
                                                    axis=1))
        
        data_dict['chi_square']['r_squared']=(data_dict['chi_square']
                                                 .apply(lambda x: 
                                                        ((x.observed
                                                          -x.expected)**2)
                                                        /x.expected,axis=1))
        
                
        
    return data_dict
        
        
        
        
def get_cleaned_emp_list(file_name=None):
    """
    Reads the cleaned Cincinnati employee list into a Pandas dataframe

    Returns
    -------
    emps : df
        Pandas dataframe of Cincinnati employees.

    """
    if file_name==None:
        file_name='..\data\output\cleaned_cincy_emp_list.csv'
    
    try:
        
        #create an ordered category type for age groups
        cat_type = CategoricalDtype(categories=['UNDER 18','18-25','26-30',
                                                '31-40','41-50','51-60', 
                                                '61-70', 'OVER 70']
                                    ,ordered=True)
        
        
        emps=pd.read_csv(file_name)
        
        
        #casts the age_range as a categorical data type
        emps['age_range']=emps.age_range.astype(cat_type)
        
    except Exception as e:
        print(e)
    else:
        return emps
    
    
    
def get_cincinnati_racial_demographics():
    
    
    
    cincy_pop_estimate=303940
    cincy_race_distribution={'White':0.482,'Black':0.423,
                             'Asian/Pacific Islander':0.023,
                             'Hispanic':0.038,
                             'American Indian/Alaskan Native':.001}
    
    df=(pd.DataFrame.from_dict(list(cincy_race_distribution.items()))
        .rename(columns={0:'race',1:'percent'}))
    
    df.set_index('race',inplace=True)
    
    df['count']=round(df['percent']*cincy_pop_estimate,0)
    
    df['expected']=df['count'].div(df['count'].sum())
    
    
    return df

    
