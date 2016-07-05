import matplotlib

"""
Plot the candle stick charts with all the additional data (technical parameters plots)
"""

# THIS VERSION IS FOR PYTHON 2 #
import urllib2
import time
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
from matplotlib.finance import candlestick_ochl
import matplotlib
import pylab
import ipdb
from utils.general_utils import csv_file_to_data_frame

matplotlib.rcParams.update({'font.size': 9})

# list of indicators that are drawn on the price chart (beside the candles). The alternative is to draw in a separate plot.
ON_GRAPH_INDICATORS = ['EMA', 'MA', 'SMA']

# mapping between the number of outer indicators (those that printed alongside the chart) to plots heights.
# heights[0], heights[1] = candles chart height, indicators plot height.
subplot_heights_mapping = {0:(100,0), 1:(80,20), 2:(70,15), 3:(70,10), 4:(60,10), 5:(50,10)}

height, width = 0, 0
date = []
start_point = 0

def draw_candlestick_chart(stock_data_table, **indicators):
    """

    :param stock_data_table:
    :param indicators: dictionary of: indicator --> values (pandas series)
     indicator is of format: NAME(period), e.g EMA(50) is EMA with time period of 50
    :return:
    """

    # calculate plots measure, by the amount of final plots
    global height, width
    height = subplot_heights_mapping[0]  # the first place is also the maximum
    width = height * 1.6
    outer_plots = [ind for ind in indicators if ind.split('(') not in ON_GRAPH_INDICATORS]
    main_chart_height = subplot_heights_mapping.get(min(len(outer_plots),5))[0]
    outer_plot_height = subplot_heights_mapping.get(min(len(outer_plots), 5))[1]

    # retrieve raw data
    global date
    date = stock_data_table.Date.apply(mdates.datestr2num).values
    openp = stock_data_table.Open.values
    highp = stock_data_table.High.values
    lowp = stock_data_table.Low.values
    closep = stock_data_table.Close.values
    volume = stock_data_table.Volume.values

    # arrange raw date
    timeline = []
    for i in xrange(len(date)):
        appendLine = date[i], openp[i], closep[i], highp[i], lowp[i], volume[i]
        timeline.append(appendLine)

    # create the main figure (candle stick chart)
    figure = plt.figure(facecolor='#07000d')
    ax1 = plt.subplot2grid((height, width), (0, 0), rowspan=main_chart_height, colspan=width, axisbg='#07000d')
    candlestick_ochl(ax1, timeline, width=.6, colorup='#53c156', colordown='#ff1717')  # plot the candle stick chart

    # figure design and specifications
    ax1.grid(True, color='w')
    ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax1.yaxis.label.set_color("w")
    ax1.spines['bottom'].set_color("#5998ff")
    ax1.spines['top'].set_color("#5998ff")
    ax1.spines['left'].set_color("#5998ff")
    ax1.spines['right'].set_color("#5998ff")
    ax1.tick_params(axis='y', colors='w')
    plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='upper'))
    ax1.tick_params(axis='x', colors='w')
    plt.ylabel('Stock price and Volume')

    global start_point
    start_point = 0  # TODO change or delete if it can stay 0
    # plot volumes
    vol_min = 0
    ax1_vol = ax1.twinx()
    ax1_vol.fill_between(date[-start_point:], vol_min, volume[-start_point:], facecolor='#00ffe8', alpha=.4)
    ax1_vol.axes.yaxis.set_ticklabels([])
    ax1_vol.grid(False)
    # set volume bar measures
    ax1_vol.set_ylim(0, 3 * volume.max())
    ax1_vol.spines['bottom'].set_color("#5998ff")
    ax1_vol.spines['top'].set_color("#5998ff")
    ax1_vol.spines['left'].set_color("#5998ff")
    ax1_vol.spines['right'].set_color("#5998ff")
    ax1_vol.tick_params(axis='x', colors='w')
    ax1_vol.tick_params(axis='y', colors='w')

    # plot indicators
    y_loc = main_chart_height  # the first y-loc is right after the main chart
    for indicator in indicators:
        if indicator not in outer_plots:
            draw_indicator_on_chart(figure, indicator, indicators.get(indicator).values, ax1)
        else:
            draw_indicator_below_chart(figure, indicator, indicators.get(indicator).values, ax1, y_loc)
            y_loc += outer_plot_height

    # mark triggers # TODO
    ax1.annotate('Big news!', (date[50], Av1[50]),
                 xytext=(0.8, 0.9), textcoords='axes fraction',
                 arrowprops=dict(facecolor='white', shrink=0.05),
                 fontsize=10, color='w',
                 horizontalalignment='right', verticalalignment='bottom')

    # final adjusments
    plt.subplots_adjust(left=.09, bottom=.14, right=.94, top=.95, wspace=.20, hspace=0)
    plt.show()
    figure.savefig('mine.png', facecolor=figure.get_facecolor())


def draw_indicator_on_chart(chart, label, values, axis):
    global height, width, date, start_point
    color = '#e1edf9'  # TODO chose random colors or iterate over few
    axis.plot(date[-start_point:], values[-start_point:], color, label=label, linewidth=1)
    ma_leg = plt.legend(loc=9, ncol=2, prop={'size': 7}, fancybox=True, borderaxespad=0.)
    ma_leg.get_frame().set_alpha(0.4)
    text_ed = pylab.gca().get_legend().get_texts()
    pylab.setp(text_ed[0:5], color='w')


def draw_indicator_below_chart(chart, label, values, axis, row_loc):
    # TODO add support in multi plots indicators (as MACD)
    global height, width, date, start_point
    ax0 = plt.subplot2grid((height, width), (row_loc, 0), sharex=axis, rowspan=1, colspan=4, axisbg='#07000d')
    color = '#c1f9f7'
    pos_color = '#386d13'
    neg_color = '#8f2020'

    ax0.plot(date[start_point:], values[start_point:], color, linewidth=1.5)
    ax0.axhline(70, color=neg_color)
    ax0.axhline(30, color=pos_color)
    ax0.fill_between(date[-start_point:], values[-start_point:], 70, where=(values[-start_point:] >= 70), facecolor=neg_color, edgecolor=neg_color,
                     alpha=0.5)
    ax0.fill_between(date[-start_point:], values[-start_point:], 30, where=(values[-start_point:] <= 30), facecolor=pos_color, edgecolor=pos_color,
                     alpha=0.5)
    ax0.set_yticks([30, 70])
    ax0.yaxis.label.set_color("w")
    ax0.spines['bottom'].set_color("#5998ff")
    ax0.spines['top'].set_color("#5998ff")
    ax0.spines['left'].set_color("#5998ff")
    ax0.spines['right'].set_color("#5998ff")
    ax0.tick_params(axis='y', colors='w')
    ax0.tick_params(axis='x', colors='w')
    plt.ylabel(label)


if __name__ == '__main__':
    draw_candlestick_chart(csv_file_to_data_frame('./data/sample3'))

