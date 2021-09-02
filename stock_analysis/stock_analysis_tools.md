[Back](https://keqideng.github.io/data_analysis_portfolio_project/)
# Stock Market Analysis
Date: Aug 30, 2021

Prepared by ***Keqi Deng***
Guided by Jose Portilla of [Pierian Data Inc.](https://courses.pieriandata.com/bundles/zero-to-data-hero)

## About This Project
This project use public stock market data from [Yahoo Finance](http://ca.finance.yahoo.com). The analysis result is only for case study purpose only.

## Packages Used in this Project
The following packages are imported for this project:
```python
import numpy as np
import matplotlib.pyplot as plt
import pandas_datareader.data as web
from datetime import datetime
```

## Analysis Method
In the guided project, the daily percentage change was plotted for comparison. However, I believe we can do more in depth analysis if we consider the changes of the key indexes: S&P 500, Dow Jones Industrial Average and Nasdaq index. Using the daily percentage change minus the daily change of the index, then analysis the mean and the standard deviation of the change rate difference. This way it would be more clear that which stock is beating the market, and which ones are lagging behind.

### Analyzing Steps:
* Pull end of the day price data of tickers that we want to analyze by using yahoo finance using ```DataReader```.
* Calculate the daily percentage change using ```.pct_change()``` method.
* Pull the daily percentage change rate of three major indexes.
* Use the ticker daily change to minus the daily changes of the major indexes.
* Use scatter plot to show the correlation of standard deviation and average daily change rate difference of each ticker.
* Read visualized plot to analysis risks and reward rate of each stock.

## Coding
The following code is used to realize the analysis:
```python
def stock_anaysis(tick_list, year):
    end = datetime.now()
    start = datetime(end.year - year, end.month,end.day)
    tick_rate_df = web.DataReader(tick_list,'yahoo',start,end)['Adj Close'].pct_change()
    indexes = web.DataReader(['^GSPC','^DJI','^IXIC'], 'yahoo', start, end)['Adj Close'].pct_change()

    for j in tick_rate_df.columns:
        for i in indexes.columns:
            tick_rate_df[f'{j}    {i}'] = tick_rate_df[j] - indexes[i]
    tick_rate_df = tick_rate_df.dropna()

    SNP = tick_rate_df[[f'{tick_list[0]}    ^GSPC',f'{tick_list[1]}    ^GSPC',f'{tick_list[2]}    ^GSPC',f'{tick_list[3]}    ^GSPC']]*100
    SNP.name = 'S&P 500'
    DOW = tick_rate_df[[f'{tick_list[0]}    ^DJI',f'{tick_list[1]}    ^DJI',f'{tick_list[2]}    ^DJI',f'{tick_list[3]}    ^DJI']]*100
    DOW.name = 'Dow Jones Industrial Average'
    Nasdaq = tick_rate_df[[f'{tick_list[0]}    ^IXIC',f'{tick_list[1]}    ^IXIC',f'{tick_list[2]}    ^IXIC',f'{tick_list[3]}    ^IXIC']]*100
    Nasdaq.name = 'Nasdaq'

    draw_a_plot(SNP)
    draw_a_plot(DOW)
    draw_a_plot(Nasdaq)

def draw_a_plot (tick):
    area = np.pi*20
    plt.scatter(tick.mean(), tick.std(),alpha = 0.5,s =area)
    #plt.ylim([0,5])
    #plt.xlim([-0.5,0.5])
    #axis labels are commented because some tickers goes out of range
    plt.title(f'Expected Daily Return Ratio minus {tick.name}')
    plt.xlabel(f'Average Daily Return minus {tick.name}/%')
    plt.ylabel('Risk Level (Standard Deviation)')
    plt.axvline(x=0, linewidth=4, color='g')

    for label, x, y in zip(tick.columns, tick.mean(), tick.std()):
        plt.annotate(
            label[:6],
            xy = (x, y), xytext = (20, 20),
            textcoords = 'offset points', ha = 'left', va = 'bottom',
            arrowprops = dict(arrowstyle = '-', connectionstyle = 'angle,angleA=-90,angleB=180,rad=5'))
    plt.grid()
    plt.show()
```

## In Action
There are four tickers are selected for the demonstration: ```'GOOG','TQQQ','BRK-B','AMC'```

Start the process by inputing the following code:
```python
stock_anaysis(['GOOG','TQQQ','BRK-B','AMC'], year = 3)
```

We can get the following plots:
BRK-B, GOOG, TQQQ, AMC and S&Q 500 Daily Change Rate Difference for the last 3 Years
![BRK-B, GOOG, TQQQ, AMC and S&Q 500 Daily Change Rate Difference for the last 3 Years](brk_goog_tqqq_amc_3_snp)

BRK-B, GOOG, TQQQ, AMC and Dow Jones Industrial Average Daily Change Rate Difference for the last 3 Years
![BRK-B, GOOG, TQQQ, AMC and Dow Jones Industrial Average Daily Change Rate Difference for the last 3 Years](brk_goog_tqqq_amc_3_dow)

BRK-B, GOOG, TQQQ, AMC and Nasdaq Daily Change Rate Difference for the last 3 Years
![BRK-B, GOOG, TQQQ, AMC and Nasdaq Daily Change Rate Difference for the last 3 Years](brk_goog_tqqq_amc_3_nasdaq)

# Project Update
Date: Sept 1, 2021

## Improve Adaptability
There are several improvements has been implemented to make the function more universally adaptable. Now the tickers entered does not limited to four. It could handle less and more tickers for comparison. The charts are also added into one chart to be more straightforward.

The updated code:
```python
def stock_anaysis(tick_list, yr_len, end = datetime.now()):
    start = datetime(end.year - yr_len,end.month,end.day)
    tick_rate_df = web.DataReader(tick_list,'yahoo',start,end)['Adj Close'].pct_change()
    indexes = web.DataReader(['^GSPC','^DJI','^IXIC'], 'yahoo', start, end)['Adj Close'].pct_change()
    
    #Function added to handle multiple ticker entries, not limited to 4
    SNP = rate_difference_df(index = indexes['^GSPC'], tickers = tick_rate_df)*100
    SNP.name = 'S&P 500'
    DOW = rate_difference_df(index= indexes['^DJI'], tickers = tick_rate_df)*100
    DOW.name = 'Dow Jones Industrial Average'
    Nasdaq = rate_difference_df(index = indexes['^IXIC'], tickers = tick_rate_df)*100
    Nasdaq.name = 'Nasdaq'
    
    #Muster subplots into one plot to simplify comparison 
    f = plt.figure(figsize=(10,30))
    f.add_subplot(311)
    draw_a_plot(SNP)
    f.add_subplot(312)
    draw_a_plot(DOW)
    f.add_subplot(313)
    draw_a_plot(Nasdaq)

    plt.show()

def draw_a_plot (tick):
    area = np.pi*10
    plt.scatter(tick.mean(), tick.std(),alpha = 0.5,s =area)
    plt.ylim([0,5])
    plt.xlim([-0.5,0.5])
    plt.title(f'Expected Daily Return Ratio minus {tick.name}')
    plt.xlabel(f'Average Daily Return minus {tick.name}/%')
    plt.ylabel('Risk Level (Standard Deviation)')
    plt.axvline(x=0, linewidth=4, color='g')

    for label, x, y in zip(tick.columns, tick.mean(), tick.std()):
        plt.annotate(
            f'{label}',
            xy = (x, y), xytext = (50, 50),
            textcoords = 'offset points', ha = 'left', va = 'bottom',
            arrowprops = dict(arrowstyle = '-', connectionstyle = 'angle,angleA=-90,angleB=180,rad=5'))
    plt.grid()

#New function help manage multiple ticker entries
def rate_difference_df (index, tickers):
    rate_diff_df = tickers.copy(deep = True)
    for j in tickers.columns:
        rate_diff_df[j] = tickers[j] - index
    rate_diff_df = rate_diff_df.dropna()
    return rate_diff_df
```

Use the above method, input command:
```python
stock_anaysis(['AAPL','GOOG','BRK-B','ATD-B.TO','BCE.TO','VOOG'], year = 2)
```

We can get the following result:
![Stock Compare AAPL, GOOG, BRK-B, ATD-B, BCE, VOOG](tol_compare_6_tickers)

## Year-Month Change Rate Chart with Heatmap
We can also use a heatmap to generate previous monthly data to find out for each stock which months of the year are generally doing better than the general market.

```pandas.pivoit_talbe``` and ```seaborn.heatmap``` are used to produce this result. The change data is calculated against the S&P 500 market daily change rate. The code is as follows:

```python
def annual_analysis(ticker, yearlen = 10, end = datetime.now(), with_number = False):
    sns.set_style('whitegrid')
    start = datetime(end.year - yearlen,1,1)
    tick_rate = web.DataReader(ticker,'yahoo',start,end)['Adj Close'].pct_change()
    snp = web.DataReader('^GSPC', 'yahoo', start, end)['Adj Close'].pct_change()
    tick_diff = (tick_rate-snp)*100
    tick_diff = tick_rate.dropna()
    tick_diff_df = pd.DataFrame(tick_diff)
    tick_diff_df['date'] = tick_diff_df.index
    tick_diff_df['year'] = tick_diff_df.date.dt.year
    tick_diff_df['month'] = tick_diff_df.date.dt.month

    sns.set_theme()
    piv_tick = tick_diff_df.pivot_table(index='month', columns='year', values='Adj Close',aggfunc=np.sum)
    piv_tick = piv_tick.round(decimals=2)
    f, ax = plt.subplots(figsize=(12, 10))
    plt.title(f'{ticker} - S&P 500 Monthly Change Rate for {yearlen} Years')
    sns.heatmap(piv_tick, annot=with_number, linewidths=.5, ax=ax, cmap='RdYlGn')
    plt.show()
```

Use the following command to analysis apple stock's change for the past 10 years.
```python
annual_analysis('AAPL', with_number=True)
```
The following picture is the heatmap result:
![apple for the past 10 years monthly](aapl_monthly_10year_heatmap)