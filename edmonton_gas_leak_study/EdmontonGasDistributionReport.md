# Edmonton Gas Distribution Analysis

Date: Aug 25, 2021
Case Study by ***Keqi Deng***
Data Provided by __*Daryl Bandstra*__ of [***Integral Engineering***](https://www.integraleng.ca)
**Sample Data for Study Purpose Only**


## Project Description
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