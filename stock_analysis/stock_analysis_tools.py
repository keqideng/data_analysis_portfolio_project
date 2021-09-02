import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pandas_datareader.data as web
from datetime import datetime
import seaborn as sns

def stock_anaysis(tick_list, yr_len, end = datetime.now()):
    start = datetime(end.year - yr_len,end.month,end.day)
    tick_rate_df = web.DataReader(tick_list,'yahoo',start,end)['Adj Close'].pct_change()
    indexes = web.DataReader(['^GSPC','^DJI','^IXIC'], 'yahoo', start, end)['Adj Close'].pct_change()

    SNP = rate_difference_df(index = indexes['^GSPC'], tickers = tick_rate_df)*100
    SNP.name = 'S&P 500'
    DOW = rate_difference_df(index= indexes['^DJI'], tickers = tick_rate_df)*100
    DOW.name = 'Dow Jones Industrial Average'
    Nasdaq = rate_difference_df(index = indexes['^IXIC'], tickers = tick_rate_df)*100
    Nasdaq.name = 'Nasdaq'

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

def rate_difference_df (index, tickers):
    rate_diff_df = tickers.copy(deep = True)
    for j in tickers.columns:
        rate_diff_df[j] = tickers[j] - index
    rate_diff_df = rate_diff_df.dropna()
    return rate_diff_df

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

annual_analysis('AAPL', with_number=True)