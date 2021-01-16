# -*- coding: utf-8 -*-
"""
Created on Sun Nov  1 10:52:07 2020

@author: letti
"""

import data_cleaning as dc
import plots


def run_analysis():
    

    emps=dc.get_cleaned_emp_list()
    
    if not emps.empty:
        
    
        data=dc.get_data_for_plots(emps)
        
        plots.plot_employee_snapshot(emps,data['job_class'],
                                     data['full_time'],data['age_groups'],
                                     data['race'],data['gender'])
        
        plots.plot_protective_services_gender(data['pro_vs_gen_gender_pct'])
        
        plots.plot_job_class_gender(data['jobs_by_gender_pct'])
        
        plots.plot_leader_gender(data['leaders_by_gender_pct'])
        
        plots.plot_job_class_race(data['job_class_race_pct'])
        
        plots.plot_top_job_titles(data['top_jobs'])




if __name__=="__main__": run_analysis()


"""
#are women and men equally represented at the management level?
#while we do see a decrease in the nunber of women from the general workforce
#to the Leadership level, the difference isn't statistically significant
#but there is room for improvement
#using a hypothesis test we see that our p-value is greater than 0.05
#so we fail to reject the null hypothesis

t_stat,p_value=sm.stats.proportions_ztest(leadership_by_gender.Leadership,
                                   leadership_by_gender.sum(axis=1),
                                   alternative='two-sided')

if p_value<0.05:
    print('We reject the null hypothesis that women and men are represented'
          ' equally at the management level')
else:
    print('We fail to reject the null hypothesis that women are in management '
          'at a rate equal to men')
    
#are women and men paid equally at the leadership level?



female_ldr_comp=emps.loc[(emps.eeo_job_class=='Officials and Administrators')&
                         (emps.sex=='Female'),'annual_rt']

male_ldr_comp=emps.loc[(emps.eeo_job_class=='Officials and Administrators')&
                         (emps.sex=='Male'),'annual_rt']



t_stat,p_value,df=sm.stats.ttest_ind(female_ldr_comp,
                                     male_ldr_comp,
                                     alternative='smaller',
                                     usevar='unequal')

if p_value<0.05:
    print('We reject the null hypothesis that men and women are paid equally'
          ' at the management level')
else:
    print('We faily to reject the null hypothesis that women and men are '
          'paid equally at the management level')
    

"""






































