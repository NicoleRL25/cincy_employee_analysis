# Cincinnati Employee Demographic Analysis
### Background
The number of municipalities participating in the Open Data movement has grown in recent years which has led to increased transparency into the financial and human resource operations of local governments. As a result of the increased accessibility of this information, constituents have greater insight into municipal employee data such as demographics and compensation.  This has led to the realization that many municipal workforces have racial and gender demographics that don’t mirror the communities that they serve. And this dissimilarity has become even more meaningful at a time of renewed focus on racial and gender inequalities in the workplace.

Cincinnati, Ohio’s largest city, launched its open data portal [CincyInsights](https://data.cincinnati-oh.gov/) in 2016 and has become a leading publisher of municipal data which includes employee data from CHRIS the city’s human resources information system.  This project uses the [City of Cincinnati Employees w/ Salaries](https://data.cincinnati-oh.gov/Efficient-Service-Delivery/City-of-Cincinnati-Employees-w-Salaries/wmj4-ygbf) dataset as of December 2020 to take a deeper look into the racial and gender composition of its municipal workforce.

### Methods
The City provides data on all active employees that includes their department, position title, gender, race, annual salary, EEO job category and more. Using this information, I completed two separate analyses.  The first seeks to understand how [women are represented in Cincinnati's workforce](https://github.com/NicoleRL25/cincy_employee_analysis/blob/main/code/cincinnati_employee_analysis.ipynb). I use hypothesis testing to determine if:
the percent of women in the workforce, excluding Protective Service Workers, is reflective of the community at large
women in Protective Service Worker categories are present at rates equal to or greater than the national average
women are in senior level Official positions at the same rate as men

I also took interest in the [racial demographics of Cincinnati's municipal workforce](https://github.com/NicoleRL25/cincy_employee_analysis/blob/main/code/racial_demographics_cincinnati_municipal_workforce.ipynb).  Like many cities, Cincinnati has become more racially and ethnically diverse in recent years. I perform chi-square testing to decide if:
the racial composition of the workforce is a reflection of the community at large and if
there is an association between someone’s race and the type of job that they hold.

### Limitations
Although this analysis details the workforce and city demographics as of December 2020, we  don’t have insight into hiring trends, the applicant pool or candidate availability for these roles.
