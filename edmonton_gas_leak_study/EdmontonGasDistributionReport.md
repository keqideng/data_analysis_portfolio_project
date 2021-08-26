[Back](https://keqideng.github.io/data_analysis_portfolio_project/)
# Edmonton Gas Distribution Analysis
Date: Aug 25, 2021

Case Study by ***Keqi Deng***
Data Provided by __*Daryl Bandstra*__ of [***Integral Engineering***](https://www.integraleng.ca)
**Sample Data for Study Purpose Only**
The dataset used in this case study is the intellectual property of [***Integral Engineering***](https://www.integraleng.ca). Daryl Bandstra authorized keqi Deng to use the dataset for analytical study only. All other usages of this dataset are not permitted.


## Analysis Objective
* Select 100 km's from the pipeline network for replacement in order to achieve the most leak reduction
* Plot the GIS information on the map

## Understand the Dataset
Import the following packages for analysis:
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
import contextily as cx
```

Import the dataset:
```python
#Import the dataset and check for the basic information
edmt_gas_df = pd.read_csv('distribution_example_case.csv')
print(edmt_gas_df.info())
```
Get the information of the dataset:
```
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 32034 entries, 0 to 32033
Data columns (total 11 columns):
 #   Column         Non-Null Count  Dtype  
---  ------         --------------  -----  
 0   Unnamed: 0     32034 non-null  int64  
 1   segment_id     32034 non-null  int64  
 2   length_m       32034 non-null  float64
 3   install_year   32034 non-null  int64  
 4   material       31073 non-null  object 
 5   activity_zone  32034 non-null  int64  
 6   diameter       31073 non-null  float64
 7   pressure       31073 non-null  float64
 8   geometry       32034 non-null  object 
 9   leaked_2019    32034 non-null  int64  
 10  leaked_2020    32034 non-null  int64  
dtypes: float64(3), int64(6), object(2)
memory usage: 2.7+ MB
```
Use chart to understand the distribution of each attribute.
### Length Distribution
```python
#Length Distribution
fig = sns.kdeplot(x = 'length_m', data = edmt_gas_df, color = 'black')
plt.xlim(0,)
plt.title('Length Distribution')
```
Length Distribution
![Length Distribution](length_kdp)

The chart shows that most of the section length are less than 500 metres. 
```python
less_than_500, more_than_500 = pd.value_counts(edmt_gas_df['length_m'] <= 500)
print(f'{less_than_500/(less_than_500+more_than_500)} of pipe sections are less than 500 metres')
```
The result suggests that: ```0.9881063869638509 of pipe sections are less than 500 metres```.

Creat a function to simplify the future usage of this plotting method.
```python
def kdp_easyPlot (attribute):
    fig = sns.kdeplot(x = attribute, data = edmt_gas_df, color = 'black')
    plt.xlim(edmt_gas_df[attribute].min(),edmt_gas_df[attribute].max())
    plt.title(f'{attribute} kernel density plot')
    plt.grid()
    plt.show()
```

### Install Year
Since this attribute is categorical, different chart is used for the analysis of material types. We can use ```seaborn.countplot``` to analysis its feature.

A function is made here for ease future plotting.
```python
def cot_easyPlot (attribute):
    fig = sns.countplot(x = attribute, data = edmt_gas_df, palette = 'bone')
    plt.title(f'{attribute} count plot')
    plt.grid(axis = 'y')
    plt.show()
```
Here we use install year for analysis.
```python
cot_easyPlot('install_year')
```
Distribution of the Year been Installed
![Installed year distribution](installYear_cotplt)

Notice that the installation of the pipes are between 1920 and 2000.
### Material

Plot for the material attribute:
```python
cot_easyPlot('material')
```
Material Count Chart
![material count chart](material_cotplt)

Notice that there are slight more steel made pipe than plastic made pipe.

### Activity Zone
Use the previous function for easier plot.
```python
cot_easyPlot('activity_zone')
```
Activity Zone Count Plot
![activity zone count plot](activityZone_cotplt)

### Diameter
Use previous functions for easier plot.
```python
cot_easyPlot('diameter')
```
Diameter Count Plot
![diameter count plot](diameter_cotplt)

### Pressure
Use function for easier plot
```python
cot_easyPlot('pressure')
```
Pressure Count
![pressure count](pressure_cotplt)

## Further Analysis

### Geometry
Using ```geopandas``` and ```contextiily``` packages, and the Coordinate Reference System (CRS) information provided:
```python
edmt_gas_gdf = gpd.read_file('distribution_example_case.csv', GEOM_POSSIBLE_NAMES="geometry", KEEP_GEOM_COLUMNS="NO")
edmt_gas_gdf = edmt_gas_gdf.set_crs('EPSG:26911')
ax = edmt_gas_gdf.plot(figsize = (20,20), alpha = 0.5)
cx.add_basemap(ax, crs = edmt_gas_gdf.crs)
plt.show()
```
Edmonton Gas Pipeline Map
![edmonton gas pipeline map](edmot_gas_map)

### Leakages
In order to find out how often does leakages occur, combine the data of ```leaked_2019``` and ```leaked_2020``` to an attribute ```leaked```.
```python
def leaked(pipe):
    nineteen, twenty = pipe
    if nineteen == 0 and twenty == 0: return False
    else: return  True

edmt_gas_df['leaked'] = edmt_gas_df[['leaked_2019','leaked_2020']].apply(leaked, axis = 1)
```
To count the leakage sections of the 2019 and 2020, also calculate the leakage rate of these years:
```python
print(pd.value_counts(edmt_gas_df['leaked']))
```
And the data count of the leaked attribute shows:
```
False    31290
True       744
Name: leaked, dtype: int64
```
Plot pie chart for visualization:
```python
plt.pie(pd.value_counts(edmt_gas_df['leaked']), labels = ['Not Leaked', 'Leaked'], autopct='%.1ff%%')
plt.title('Leakage Percentage of 2019 and 2020')
```
Leakage Percentage of 2019 and 2020
![leakage chart](leakage_pie)

#### Leakage vs. Installed Year
```python
fig = sns.catplot(y = 'leaked', x = 'install_year', data = edmt_gas_df, kind = 'bar', palette = 'bone')
```
Leakage and Installed Year
![leakage and year](leakage_installYear_catplt)

#### Leakage vs. Installed Year and Material
```python
fig = sns.catplot(y = 'leaked', x = 'install_year', hue = 'material', data = edmt_gas_df, kind = 'bar', palette = 'bone')
```
Leakage vs. Installed Year and Material
![leakage installed year and material](leakage_installYear_material_catplt)
From this chart, we can clearly see that plastic pipe's leakage rate is highly depended on the year of usage.

#### Leakage vs. Installed Year and Diameter
```python
fig = sns.catplot(y = 'leaked', x = 'install_year', hue = 'diameter', data = edmt_gas_df, kind = 'bar', palette = 'bone')
```
#### Leakage vs. Activity Zone
```python
fig = sns.catplot(y = 'leaked', x = 'activity_zone', data = edmt_gas_df, kind = 'bar', palette = 'bone')
```
Activity Zone Leakage Rate
![activityZone leakage rate](leakage_activityZone_catplt)

#### Leakage vs. Activity Zone and Material
```python
fig = sns.catplot(y = 'leaked', x = 'activity_zone', hue = 'material', data = edmt_gas_df, kind = 'bar', palette = 'bone')
```
Activity Zone and Material Leakage Rate
![activityZone and material leakage](leakage_actvZone_material_catplt)

#### Leakage Rate vs. Diameter
```python
fig = sns.catplot(y = 'leaked', x = 'diameter', data = edmt_gas_df, kind = 'bar', palette = 'bone')
```
Diameter and Material Leakage Rate
![diameter leakage](leakage_diameter_catplt)


#### Leakage Rate vs. Diameter and Material Type
```python
fig = sns.catplot(y = 'leaked', x = 'diameter', hue = 'material', data = edmt_gas_df, kind = 'bar', palette = 'bone')
```
Diameter and Material Leakage Rate
![diameter and material leakage](leakage_diameter_material_catplt)
Notice thin steel pipe is more likely to leak.

### Optimize the Replacement Selection
Assume all the categorical attributes effect the leakage rate of the pipe.
First, creat a new column:
```python
def leaked_numerical(pipe):
    nineteen, twenty = pipe
    return nineteen + twenty
edmt_gas_df['leaked_num'] = edmt_gas_df[['leaked_2019','leaked_2020']].apply(leaked_numerical, axis = 1)
```
Check the result of the numerical leakage data:
```python
print(pd.value_counts(edmt_gas_df['leaked_num']))
```
Result shows:
```
0    31290
1      734
2       10
Name: leaked_num, dtype: int64
```
Since there are 10 sections experienced leakage in both 2019 and 2020. It is very likely that the leakage would happen again. The sections experienced leakages should be prioritized during the pipe replacement.

For the rest of the sections, use pivot table to help us decide:
```python
edmt_piv = pd.pivot_table(data = edmt_gas_df, values = ['leaked_num','length_m'], index = ['install_year','material','activity_zone','diameter','pressure'], aggfunc = {'leaked_num': np.mean, 'length_m': np.sum})
```
We get the result:
```
                                                       leaked_num     length_m
install_year material activity_zone diameter pressure                         
1920         Plastic  1             2.0      30.0        0.000000  5164.943551
                                             50.0        0.000000  1295.922115
                                    4.0      30.0        0.000000  1969.426068
                                             50.0        0.000000  1581.428351
                      2             2.0      30.0        0.000000  3725.448334
...                                                           ...          ...
2000         Steel    2             2.0      30.0        0.062500  1546.534515
                      3             2.0      30.0        0.000000  4137.775010
                      4             2.0      30.0        0.034483  3351.034391
                                    4.0      30.0        0.000000    23.129415
                      5             2.0      30.0        0.000000   216.060049

[378 rows x 2 columns]
```

Since the budget only allow us to replace 100km of pipes, sort the result and select 100km pipe at the highest risk:
```python
edmt_piv_sorted = edmt_piv.sort_values('leaked_num', ascending= False)
edmt_piv_sorted['cumulative_length_m'] = np.cumsum(edmt_piv_sorted.length_m)
edmt_piv_sorted_selected = edmt_piv_sorted[edmt_piv_sorted.cumulative_length_m <= 100000]
```
The selected types of pipelines are as follow:
```
                                                       leaked_num  ...  cumulative_length_m
install_year material activity_zone diameter pressure              ...                     
1950         Plastic  2             6.0      50.0        0.200000  ...          1132.544173
1960         Plastic  1             6.0      50.0        0.200000  ...          3238.513389
1950         Plastic  3             4.0      50.0        0.157895  ...          6259.079651
1960         Steel    5             6.0      30.0        0.153846  ...          9181.056893
1950         Plastic  4             6.0      50.0        0.142857  ...          9790.168508
1940         Plastic  5             2.0      50.0        0.138211  ...         30123.459169
1930         Plastic  5             2.0      50.0        0.132911  ...         68841.680561
                      4             2.0      50.0        0.127273  ...         95348.732560
1970         Steel    5             4.0      50.0        0.111111  ...         96794.129590

[9 rows x 3 columns]
```
Selected sections:
```python
selected_sections = pd.DataFrame
def section_select(install_year,material,activity_zone,diameter,pressure):
    return edmt_gas_df.loc[(edmt_gas_df['install_year'] == install_year) &
                          (edmt_gas_df['material'] == material) &
                          (edmt_gas_df['activity_zone'] == activity_zone) &
                          (edmt_gas_df['diameter'] == diameter) &
                          (edmt_gas_df['pressure'] == pressure)]

selected_sections = section_select(1950,'Plastic',2,6.0,50.0)
selected_sections = selected_sections.append(section_select(1960,'Plastic',1,6.0,50.0))
selected_sections = selected_sections.append(section_select(1950,'Plastic',3,4.0,50.0))
selected_sections = selected_sections.append(section_select(1960,'Steel',5,6.0,30.0))
selected_sections = selected_sections.append(section_select(1950,'Plastic',4,6.0,50.0))
selected_sections = selected_sections.append(section_select(1940,'Plastic',5,2.0,50.0))
selected_sections = selected_sections.append(section_select(1930,'Plastic',5,2.0,50.0))
selected_sections = selected_sections.append(section_select(1930,'Plastic',4,2.0,50.0))
selected_sections = selected_sections.append(section_select(1970,'Steel',5,4.0,50.0))
selected_sections = selected_sections.sort_values('segment_id')
```
Get 717 sections need to be replaced:
```
<class 'pandas.core.frame.DataFrame'>
Int64Index: 717 entries, 31 to 31848
Data columns (total 13 columns):
 #   Column         Non-Null Count  Dtype  
---  ------         --------------  -----  
 0   Unnamed: 0     717 non-null    int64  
 1   segment_id     717 non-null    int64  
 2   length_m       717 non-null    float64
 3   install_year   717 non-null    int64  
 4   material       717 non-null    object 
 5   activity_zone  717 non-null    int64  
 6   diameter       717 non-null    float64
 7   pressure       717 non-null    float64
 8   geometry       717 non-null    object 
 9   leaked_2019    717 non-null    int64  
 10  leaked_2020    717 non-null    int64  
 11  leaked         717 non-null    bool   
 12  leaked_num     717 non-null    int64  
dtypes: bool(1), float64(3), int64(7), object(2)
memory usage: 73.5+ KB
```
Export the selected sections to csv file:
```python
selected_sections.to_csv('selected_sections.csv')
```
Plot out the sections that needs to be replaced on map, try different map provider:
```python
edmt_gas_gdf = gpd.read_file('selected_sections.csv', GEOM_POSSIBLE_NAMES="geometry", KEEP_GEOM_COLUMNS="NO")
edmt_gas_gdf = edmt_gas_gdf.set_crs('EPSG:26911')
ax = edmt_gas_gdf.plot(figsize = (20,20), alpha = 0.8, color = 'teal')
cx.add_basemap(ax, crs = edmt_gas_gdf.crs, source=cx.providers.Stamen.TonerLite)
```
Map of the Replacement Pipeline Sections
![map of the replacement](map_replace)

