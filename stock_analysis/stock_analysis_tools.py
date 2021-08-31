import numpy as np
import matplotlib.pyplot as plt
import pandas_datareader.data as web
from datetime import datetime

def stock_anaysis(tick_list, year):
    end = datetime.now()
    start = datetime(end.year - year,end.month,end.day)
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
    plt.title(f'Expected Daily Return Ratio minus {tick.name}')
    plt.xlabel(f'Average Daily Return minus {tick.name}/%')
    plt.ylabel('Risk Level (Standard Deviation)')
    plt.axvline(x=0, linewidth=4, color='g')

    for label, x, y in zip(tick.columns, tick.mean(), tick.std()):
        plt.annotate(
            label[:6],
            xy = (x, y), xytext = (15, 25),
            textcoords = 'offset points', ha = 'left', va = 'bottom',
            arrowprops = dict(arrowstyle = '-', connectionstyle = 'angle,angleA=-90,angleB=180,rad=5'))
    plt.grid()
    plt.show()

stock_anaysis(['GOOG','TQQQ','BRK-B','AMC'], year = 3)