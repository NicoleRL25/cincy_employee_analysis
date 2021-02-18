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
        
               
        
        plots.plot_top_job_titles(data['top_jobs'])
        
        plots.plot_racial_composition(data['race'])
        
        plots.plot_observed_vs_expected(data['chi_square'])

        plots.plot_job_class_race(data['job_class_race_pct'],save_fig=True)








if __name__=="__main__": run_analysis()








































