from pylab import *
import matplotlib.pyplot as plt
from datetime import datetime
import time
from matplotlib.dates import  DateFormatter, WeekdayLocator, HourLocator, \
     DayLocator, MONDAY
from matplotlib.finance import _candlestick
import pandas as pd


def plotTest(df):
     mondays = WeekdayLocator(MONDAY)        # major ticks on the mondays
     alldays = DayLocator()              # minor ticks on the days
     weekFormatter = DateFormatter('%b %d')  # e.g., Jan 12
     dayFormatter = DateFormatter('%d')      # e.g., 12
     funcy = lambda x: date2num(datetime.strptime(x, "%Y-%m-%d"))

     # df = pd.read_csv("/Users/roeya/Desktop/stock/BDE.csv")
     df = df[['Date', 'Open', 'Close', 'High', 'Low']]
     df.columns = ['date', 'open', 'close', 'high', 'low']
     df[['date']] = df['date'].map(funcy)

     fig, ax = plt.subplots()
     fig.subplots_adjust(bottom=0.2)
     # ax.xaxis.set_major_locator(mondays)
     # ax.xaxis.set_minor_locator(alldays)
     ax.xaxis.set_major_formatter(weekFormatter)
     _candlestick(ax, [tuple(x) for x in df.head(n=100).values], width=0.6)
     ax.xaxis_date()
     ax.autoscale_view()
     plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')

     plt.show()
