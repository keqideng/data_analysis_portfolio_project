[Back](https://keqideng.github.io/data_analysis_portfolio_project/)
# Titanic Passenger Analysis
Date: Aug 24, 2021

Case Study by ***Keqi Deng***
Guided by Jose Portilla of [Pierian Data Inc.](https://courses.pieriandata.com/bundles/zero-to-data-hero)

## About the data
The data used in this case study is from kaggle: [Titanic - Machine Learning from Disaster](https://www.kaggle.com/c/titanic).

## Set Goal for the Analysis Outcome
* Identify the demographic of the Titanic passengers
  * General demographic identifiers: *Gender*, *Age*
  * Embarked Location
  * Companion information: *Sibling and Spouse*, *Parents and Children*
* The features of the passengers who survived the sinking
    * Age
    * Groups of people (Male, Female, Child)
    * Passenger Class
    * Fare paid

## Understand the Dataset

The following python packages are imported for this project:
```python
import pandas as pd
from pandas import Series, DataFrame
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
```

Using the following command in python to understand the general information of the dataset:

```python
titanic_df = pd.read_csv('train.csv')
print(titanic_df.info())
```
The result reads:
```
RangeIndex: 891 entries, 0 to 890
Data columns (total 12 columns):
 #   Column       Non-Null Count  Dtype  
---  ------       --------------  -----  
 0   PassengerId  891 non-null    int64  
 1   Survived     891 non-null    int64  
 2   Pclass       891 non-null    int64  
 3   Name         891 non-null    object
 4   Sex          891 non-null    object
 5   Age          714 non-null    float64
 6   SibSp        891 non-null    int64  
 7   Parch        891 non-null    int64  
 8   Ticket       891 non-null    object
 9   Fare         891 non-null    float64
 10  Cabin        204 non-null    object
 11  Embarked     889 non-null    object
dtypes: float64(2), int64(5), object(5)
memory usage: 83.7+ KB
```
Keep in mind that the columns for *Age* and *Cabin* is missing a significant amount of data.

Use the following method to separate the survived passengers and the passengers who have passed for further analysis.
```python
survived_df = titanic_df[titanic_df['Survived'] == 1]
passed_df = titanic_df[titanic_df['Survived'] != 1]
print(f'Total Passenger:\t\t{titanic_df.shape[0]}')
print(f'Surviced Passenger:\t\t{survived_df.shape[0]}')
print(f'Passed Passenger:\t\t{passed_df.shape[0]}')
print(f'Overall Survival Rate:\t{survived_df.shape[0]/titanic_df.shape[0]}')
```
We can get some some result and general understanding of the survival rate of this accident
```
Total Passenger:				891
Surviced Passenger:			342
Passed Passenger:				549
Overall Survival Rate:	0.3838383838383838
```
## General information of All Passengers
### Gender and Cabin Distribution
First explore the gender distribution of the passengers:
```python
gender_ds = titanic_df['Sex']
print(pd.value_counts(gender_ds))
```
result:
```
male      577
female    314
Name: Sex, dtype: int64
```
Notice the male passengers are significantly more than female passengers. Plot the chart for visualization:
```python
plt.title('Titanic Passenger Gender Distribution')
sns.countplot(x = 'Sex', data = titanic_df, color = 'black')
plt.show()
```
Passenger Gender Distribution
![Titanic Passenger Gender Distribution](gender_distribution)

The plot also suggests that there are way more male passengers than female passengers.

So what is the gender distribution among different passenger classes? Consider the time of the Titanic voyage, there might be some significant difference of the gender distribution in different classees.

Plot the passenger class information with the gender distribution with the following python code:
```python
plt.title('Titanic Passenger Class and Gender Distribution')
sns.countplot(x = 'Pclass', data = titanic_df, hue = 'Sex', color = 'black', alpha = 0.8)
plt.show()
```
Passenger Class and Gender Distribution
![Titanic Passenger Class and Gender Distribution](gender_class_barh)

The expectation is correct: The gender distribution is more equal in the First and Second classes. But more passengers in the Third class have significantly more male passengers than female passengers.

Maybe the reason for this outcome is due to people from the premium classes are travelling with families, while people from lower classes are travelling alone. Let's plot a cross. To verify this theory:

```python
def with_family (passenger):
    sibsp, parch = passenger
    if sibsp + parch == 0: return False
    else: return True

titanic_df['Person Type'] = titanic_df[['Age','Sex']].apply(person_type_identifier,axis=1)

fig = sns.catplot(x = 'Pclass', y = 'WithFamily', data = titanic_df, kind = 'bar', palette = 'binary')
plt.ylim(0,1)
plt.ylabel('The Rate of People Travel with Family')
plt.xlabel('Class')
plt.show()
```
The Rate of People Travel with Families based on Their Classes
![The Rate of People Travel with Families based on Their Classes](WithFamily_Class)

We can see that there are more people travelling with families in the first and second class, comparing to the third class.

In order to find more information between the adults and the children, based on the time period of the titanic, we made an assumption that **whomever under the age of 16 is considered a child**. A function was defined:
```python
def person_type_identifier (passenger):
    age,gender = passenger
    if age <= 16: return 'child'
    else: return gender

titanic_df['Person Type'] = titanic_df[['Age','Sex']].apply(person_type_identifier,axis=1)
print(pd.value_counts(titanic_df['Person Type']))
```
we could find the output of this result:
```
male      526
female    265
child     100
Name: Person Type, dtype: int64
```
For easier understanding of this data, use ```countplot``` to show the graphic result, and also consider the cabin type of the passenger.
```python
plt.title('Titanic Passenger Class and Person Type Distribution')
sns.countplot(x = 'Pclass', data = titanic_df, hue = 'Person Type', color = 'black', alpha = 0.8)
```
Passenger Class and Person Type Distribution
![Titanic Passenger Class and Person Type Distribution](person_type_and_class_barh)

The result suggests that: despite of the the significant amount of male in the third class, there are also many children in the third class. We know that the evacuation procedure of the Titanic is children and women
comes first. Maybe this demographic feature would effect the survival rate of this class.

### Age Distribution
To understand the age distribution, the Kernel Density Plot ```seaborn.kdeplot``` was used to show the Passengers Age Distribution.

```python
fig = sns.kdeplot(data = titanic_df, x = 'Age', hue = 'Sex', palette = 'colorblind', shade = True)
```
Age and Gender Distribution Chart
![Age and Gender Distribution Chart](age_gender)

```python
fig = sns.kdeplot(data = titanic_df, x = 'Age', hue = 'Sex', palette = 'colorblind', shade = True, multiple = 'fill')
```
Age and Gender Distribution Fill Chart
![Age and Gender Distribution Fill Chart](age_gender_fill)

Notice that there are more male than female in the older age groups.

Similar chart can also be plotted as a histogram ```hist```.
```python
titanic_df['Age'].hist(bins = 70)
```
Histogram of Age Distribution
![Histogram of Age Distribution](age_hist)


### Age and Cabin Class Correlation

It would be interesting to find out whether there would be any correlation between age and classes. Younger people are expected to be in lower classes and older people are expected more to be in higher classes.

```python
fig = sns.kdeplot(data = titanic_df, x = 'Age', hue = 'Pclass', palette = 'colorblind', shade = True)
plt.xlim(0,)
```
Age and Class Distribution
![Age and Class Distribution](age_class_dist)

```python
fig = sns.kdeplot(data = titanic_df, x = 'Age', hue = 'Pclass', palette = 'colorblind', shade = True, multiple = 'fill')
plt.xlim(0,)
```
Age and Class Filled Chart
![Age and Class Filled Chart](age_class_filled)

We can clearly see that the expectation was correct. The average age of the people in higher classes are older than the passengers in lower classes.

To find out the exact number of the Titanic passenger average age, use the following code:
```python
print(titanic_df['Age'].mean())
```
**The average age of all passengers** is ```29.69911764705882```.

Use the following code to find out the average age of different classes:
```python
first_age = titanic_df[titanic_df['Pclass'] == 1]['Age'].mean()
second_age = titanic_df[titanic_df['Pclass'] == 2]['Age'].mean()
third_age = titanic_df[titanic_df['Pclass'] == 3]['Age'].mean()
print(f'First Class Average Age: \t{first_age}')
print(f'Second Class Average Age: \t{second_age}')
print(f'Third Class Average Age: \t{third_age}')
```
We get the average:
```
First Class Average Age: 	38.233440860215055
Second Class Average Age: 	29.87763005780347
Third Class Average Age: 	25.14061971830986
```

### Some Other Interesting Notice
We might want to consider passengers' embark location and the ticket class that they purchased. This might show us some interesting insights of the local economy situation.
```python
fig = sns.countplot(x = 'Embarked', hue = 'Pclass', data = titanic_df, palette = 'binary')
fig.set_xticklabels(['Southampton', 'Cherbourg', 'Queenstown'])
plt.ylabel('count')
plt.xlabel('Embarked Location')
```
Embarking Location of Different Passenger Classes Count
![Embarking Location of Different Passenger Classes Count](embark_class)

We can clearly see that the majority of the passengers boarded from Southampton. The majority of the passengers boarded from Cherbourg purchased ticket for the first and second classes, while almost all passengers boarded from Queenstown purchased ticket for third class.


## Finding the Key of Survival
### Women and Children First
We know that during the evacuation of Titanic, women and children are among the first to be save. So their survival rate is expected to be higher than men.
```python
fig = sns.countplot(x = 'Person Type', hue = 'Survived', data = titanic_df, palette = 'bone')
```
Different Passenger Survival Count
![Person Type Survival Count](person_type_survival_count)

```python
fig = sns.catplot(x = 'Person Type', y = 'Survived', data = titanic_df, kind = 'bar', palette = 'bone')

plt.ylabel('Survival Rate')
plt.xlabel('Person Type')
```
Survival Rate of Different Type of passengers
![Survival Rate of Different Type of passengers](person_type_survival_rate)

It is clear from the chart that the survival rate for male passengers is much lower than those of females and children.

### Survival Rate of Different Classes
In order to find out whether the passengers' cabin class might effect their survival rate, plot the following chart.

```python
fig = sns.catplot(x = 'Pclass', y = 'Survived', data = titanic_df, kind = 'bar', palette = 'bone')
fig.set_xticklabels(['First Class', 'Second Class', 'Third Class'])
plt.ylim(0,1)
plt.ylabel('Survival Rate')
plt.xlabel('Passenger Class')
```
Survival Rate of Passengers from Different Classes
![Survival Rate of Passengers From Different Classes](class_survival)

To find out more about different groups of people's survival rate, add ```hue = 'Person Type'``` to see whether the survival rate is significantly effected by women and children.
```python
fig = sns.catplot(x = 'Pclass', y = 'Survived', data = titanic_df, hue = 'Person Type', kind = 'bar', palette = 'bone')
```
Survival Rate of Different Types of Passengers in Different Classes
![Survival Rate of Different Types of Passengers in Different Classes](class_survival_persontype)

The plot shows first and second class women and children have significant higher chance of survival comparing to the ones in third class. Male passengers have much higher rate of survival if they are in the first class. Interestingly, male passengers from third class have higher survival rate than the males from second class.

If we do a headcount of the people survived the tragic.
```python
fig = sns.countplot(x = 'Pclass', hue = 'Person Type', data = titanic_df[titanic_df['Survived'] == 1], palette = 'bone')

fig.set_xticklabels(['First Class', 'Second Class', 'Third Class'])
plt.ylabel('Survival Count')
plt.xlabel('Passenger Class')
plt.grid(linestyle = '--')
```
Survived Passenger Count
![Survived Passenger Count](count_pclass_personType)

The amount of females survived is decreasing from the first to the third class, while the amount of children are increasing. The amount of male whom survived is similar in the first and third classes, but significantly lower in second class.

### Price Paid and Survival Rate

It would also be interesting to find out if the price they paid has any effect on their survival rate.

First find out the range of the price:
```python
fig = sns.kdeplot(data = titanic_df, x = 'Fare', palette = 'bone', shade = True)
plt.xlim(0,)
```
Price Range
![Price Range](fare_kdp)

Most of the people paid less than 50 dollars. In fact, **94%** of the passengers paid less than 100 for the ticket.
```python
lower_than_100, higher = pd.value_counts(titanic_df['Fare'] <= 100)
print(f'Rate of Passengers Paid Less Than 100 Fare: \t {lower_than_100/(lower_than_100 + higher)}')
'''sns.violinplot(data = titanic_df, y = 'Fare', x = 'Survived', palette = 'bone')'''
```
Result:
```
Rate of Passengers Paid Less Than 100 Fare: 	 0.9405162738496072
```

So we can focus on the price range between 0 to 100.

```python
price_range=[10,25,50,100]
fig = sns.lmplot(x = 'Fare', y = 'Survived', data=titanic_df,palette='bone',x_bins=price_range)
plt.xlim(0,120)
plt.ylim(0,1)
plt.grid()
plt.show()
```
Trend of Survival Rate vs. Fare Price
![Trend of Survival Rate vs. Fare Price](survival_fare_lm)

It is clear that there is a an increasing trend of the survival rate when the fare paid goes up.

If we consider different groups of people.

```python
fig = sns.lmplot(x = 'Fare', y = 'Survived', hue = 'Person Type', data=titanic_df,palette='bone',x_bins=price_range)
```
Trend of Survival Rate vs. Fare and Person Types
![Trend of Survival Rate vs. Fare and Person Types](survival_fare_personType_lm)

It is clear that for male and female passengers, the survival rate is increasing with the fare paid goes up; while the survival rate for children does not have strong correlation to the fare been paid.

### Survival Rate of Different Age Groups
Continuing to use ```lmplot``` for further analysis. Let's try to find whether age of a person effect it's survival rate.
```python
fig = sns.lmplot(x = 'Age', y = 'Survived', data=titanic_df, palette='bone', x_bins=generations)
plt.xlim(0,)
plt.ylim(0,1)
plt.grid()
```
Survival Trend vs. Age
![Survival Trend vs. Age](survival_age_lm)

It is clear that the survival rate goes down with age increases.

When we consider people of different gender:
```python
fig = sns.lmplot(x = 'Age', y = 'Survived', hue = 'Sex', data=titanic_df, palette='bone', x_bins=generations)
```
Survival Trend vs. Age and Gender
![Survival Trend vs. Age and Gender](survival_age_gender_lm)

The result suggests older women have higher chance of survival than younger women, while the trend is reversed for male passengers.

### Comparing Passengers Travel W/O Families
Using the ```lmplot``` to analysis the difference of the survival rate when the passengers are travelling with/without families.
```python
fig = sns.lmplot(x = 'Age', y = 'Survived', hue = 'WithFamily', data=titanic_df, palette='bone', x_bins=generations)
```
Survival Trend vs. Age and Whether Travel With Family
![Survival Trend vs. Age and Whether Travel With Family](survival_age_withFam_lm)

The overall survival rate for passengers is higher comparing to the passengers without families.

### Other Interesting Plots

```python
age_pclass_survival_plot = sns.violinplot(data = titanic_df, y = 'Age', x = 'Pclass', hue = 'Survived', split = True, palette = 'viridis', alpha = 0.8)
plt.title('Survival Passengers of Different Classes and Age Groups')
```
Survival Passengers of Different Classes and Age Groups
![Survival Passengers of Different Classes and Age Groups](age_pclass_survival_plot)

```python
age_gender_survival_plot = sns.violinplot(data = titanic_df, y = 'Age', x = 'Sex', hue = 'Survived', split = True, palette = 'colorblind')
plt.title('Survival Passengers of Different Gender and Age Groups')
```
Survival Passengers of Different Gender and Age Groups
![Survival Passengers of Different Gender and Age Groups](age_gender_survival_plot)

```python
age_gender_survival_plot = sns.violinplot(data = titanic_df, y = 'Age', x = 'Survived', hue = 'Sex', split = True, palette = 'colorblind')
plt.title('Survival Passengers of Different Gender and Age Groups')
```
Survival Passengers of Different Gender and Age Groups
![Survival Passengers of Different Gender and Age Groups](age_servived_sex_violin)

```python
def with_family (passenger):
    sibsp, parch = passenger
    if sibsp + parch == 0: return False
    else: return True
titanic_df['WithFamily'] = titanic_df[['SibSp','Parch']].apply(with_family, axis = 1)
age_companion_survival_plot = sns.violinplot(data = titanic_df, y = 'Age', x = 'Survived', hue = 'WithFamily', split = True, palette = 'colorblind')
plt.title('Survival Passengers with/without Companion and Age Groups')
```
Survival Passengers with/without Companion and Age Groups
![Survival Passengers with/without Companion and Age Groups](age_compa_surv_plot)

## Conclusion

After analysis the dataset of the Titanic passengers, we have found out:
* Women, especially older women have significant higher survival rate.
* Adult passengers in the first and second classes have higher survival rate.
  * This trend was also shown in the correlation of fare paid and survival rate. People in the more premium cabin pay more fare.
* Passengers travel with their families (Spouse, Sibling, Parents, Children) have slight higher survival rate than people travel alone.
* Male passengers from the second class have the lowest survival rate of all types of passengers.
