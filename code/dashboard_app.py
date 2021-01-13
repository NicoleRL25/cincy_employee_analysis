# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 16:32:36 2020

@author: letti
"""

import numpy as np
import pandas as pd
from pandas.api.types import CategoricalDtype
from datetime import datetime

#imports for building bokeh dashboard
from bokeh.io import output_file, show, curdoc
from bokeh.plotting import figure
from bokeh.layouts import widgetbox, column, row
from bokeh.models import Slider, ColumnDataSource, Paragraph, Div
from bokeh.transform import factor_cmap, cumsum
from bokeh.palettes import inferno, magma, Blues256, brewer,plasma
from bokeh.models.tools import HoverTool




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



#create plots and widgets

output_file('dashboard.html')


div_image = Div(text="""<img src="cincinnati_logo.png  
                "Current Headcount: "+str(len(emps))
                alt="div_image" >""",
                width=200, height=150)

#show(div_image)

headcount_text=Paragraph(text="CURRENT HEADCOUNT: " + str(len(emps)),
                         width=185,height=150)
headcount_text.align='end'

#show(headcount_text)


show(column(div_image,headcount_text))



#passes dataframe to source using ColumnDataSource
#can 
source=ColumnDataSource(emps.age_range.value_counts(sort=False)
                        .reset_index())

#passes index values as a list
age_groups=source.data['index'].to_list()

#creates a categorical color map to give each category a different color.
#the chart below uses the inferno color palette.  the number of categories
#has to get passed to the palette as a parameter
#if all bars can be the same color, the color string can be passed to the
#color parameter in the chart

color_map=factor_cmap('index', inferno(len(age_groups)), age_groups)

a=figure(title='Age Distribution', x_range=age_groups,
         x_axis_label='Age Range',y_axis_label='Employee Count',
         tools='hover',tooltips=[("count","@age_range")])
a.title.align='center'
a.vbar(x='index',top='age_range',source=source,width=0.7,color=color_map)

#remove logo from toolbar
a.toolbar.logo=None

#sdisables the chart pan tool 
a.toolbar.active_drag=None

#a.toolbar_location=None - hids the toolbar from view

#hover=HoverTool()
#hover.tooltips=[("count","@age_range")]
#a.add_tools(hover)

show(a)


gender_source=ColumnDataSource(emps.sex.value_counts(normalize=True).reset_index())
gender_source.data['angle'] = gender_source.data['sex']/gender_source.data['sex'].sum() * 2*3.14

gender=gender_source.data['index'].to_list()

color_map=factor_cmap('index', plasma(len(emps.sex.value_counts())),
                      gender)

p=figure(title='Gender Distribution',toolbar_location=None,
         tools='hover',tooltips="@index, @sex{00%}")
p.annular_wedge(x=0, y=1, inner_radius=0.2, outer_radius=0.4,
                start_angle=cumsum('angle', include_zero=True),
                end_angle=cumsum('angle'),
                line_color="white", fill_color=color_map, legend_field='index',
                source=gender_source)

p.axis.axis_label=None
p.axis.visible=False
p.grid.grid_line_color = None

show(p)



race_source=ColumnDataSource(emps.race.value_counts()
                             .reset_index()
                             .rename(columns={'index':'race'
                                              ,'race':'count'}))
race_source.data['angle'] = (race_source.data['count']
                             /race_source.data['count'].sum() 
                             * 2*3.14)

races=list(race_source.data['race'])

color_map=factor_cmap('race',
                      plasma(len(races)),
                      races)
                      
r=figure(title='Racial Demographics', toolbar_location=None,
         tools='hover',tooltips="@race,@count",
         height=350,width=600)          

r.title.align='center'
r.annular_wedge(x=0,y=1,inner_radius=0.4, outer_radius=0.8,
                start_angle=cumsum('angle',include_zero=True)
                ,end_angle=cumsum('angle'),line_color='white',
                fill_color=color_map,legend_field='race',
                source=race_source)     

r.add_layout(r.legend[0], 'right')
r.axis.axis_label=None
r.axis.visible=False
r.grid.grid_line_color=None

show(r)       



#add callbacks


#arrange plots and widgets in layouts