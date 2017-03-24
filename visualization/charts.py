"""
Plot the candle stick charts with all the additional data (technical parameters plots)
"""
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
from matplotlib.finance import candlestick_ochl
import matplotlib
import pylab
from utils.general_utils import csv_file_to_data_frame, get_indicators
from utils import general_utils

import ipdb

matplotlib.rcParams.update({'font.size': 9})

# list of indicators that are drawn on the price chart (beside the candles). The alternative is to draw in a separate plot.
ON_GRAPH_INDICATORS = ['EMA', 'MA', 'SMA']

# mapping between the number of outer indicators (those that printed alongside the chart) to plots heights.
# heights[0], heights[1] = candles chart height, indicators plot height.
subplot_heights_mapping = {0:(100,0), 1:(80,20), 2:(70,15), 3:(70,10), 4:(60,10), 5:(50,10)}

height, width = 0, 0
date = []
start_point = 0

chart_dir = './charts'


def draw_candlestick_chart(symbol, stock_data_table, trade_system):
    """
    This function retrieve the data from the stock table and trade system, to send to the function that does the draws.
    Basically it's a wrapper (adapter) to allow linkage between the application level to the drawing function.
    """
    labeled= lambda(indicator): indicator.get_name() + '(' + str(indicator.get_timeperiod()) + ')'
    indicators = dict([(labeled(ind), stock_data_table[ind.get_title()]) for ind in get_indicators(trade_system)])
    close_triggers = stock_data_table.CLOSE_TRIGGER[stock_data_table.CLOSE_TRIGGER].index.values
    open_triggers = stock_data_table.OPEN_TRIGGER[stock_data_table.OPEN_TRIGGER].index.values
    return _draw_candlestick_chart(symbol, stock_data_table, close_triggers, open_triggers, indicators=indicators)


def _draw_candlestick_chart(symbol, stock_data_table, open_triggers=None, close_triggers=None, indicators=None):
    """
    :param symbol: the symbol of the stock
    :param stock_data_table: pandas Dataframe table contains raw data column
    :param open_triggers, close_triggers: pandas series contains the index of the date which will be marked.
    e.g. if open_trigger[3]=20 then date[20] will be mark
    :param indicators: dictionary of: indicator(key) --> values(value), values are pandas series
     indicator is of format: NAME(period), e.g EMA(50) is EMA with time period of 50
    :return:
    """

    # calculate plots measure, by the amount of final plots
    global height, width
    height = subplot_heights_mapping[0][0]  # the first place is also the maximum
    width = int(height * 1.6)
    outer_plots = [ind for ind in indicators.keys() if ind.split('(')[0] not in ON_GRAPH_INDICATORS]
    inner_plots = [ind for ind in indicators.keys() if ind.split('(')[0] in ON_GRAPH_INDICATORS]
    main_chart_height = subplot_heights_mapping.get(min(len(outer_plots), 5))[0]
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
    # TODO change colors and use variables for this
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
    plt.suptitle(symbol.upper(), color='silver')

    global start_point
    start_point = 0  # TODO change or delete if it can stay 0

    # plot indicators
    for indicator in inner_plots:  # must draw the on chart plots first
        draw_indicator_on_chart(ax1, indicator, indicators.get(indicator).values)
    y_loc = main_chart_height  # the first y-loc is right after the main chart
    for indicator in outer_plots:
        axis = draw_indicator_below_chart(ax1, indicator, indicators.get(indicator).values, y_loc, outer_plot_height, figure, symbol)
        y_loc += outer_plot_height
        # rotate labels on the axis of the last (lowest) chart
        for label in axis.xaxis.get_ticklabels():
            label.set_rotation(45)
            label.set_size(7)

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

    # mark open and close triggers
    if open_triggers.any():
        [mark_trigger(ax1, date[trigger], lowp[trigger], 'OPEN', figure) for trigger in open_triggers]
    if close_triggers.any():
        [mark_trigger(ax1, date[trigger], highp[trigger], 'CLOSE', figure) for trigger in close_triggers]

    # final adjustments
    plt.subplots_adjust(left=.09, bottom=.14, right=.94, top=.95, wspace=.20, hspace=0)
    # config the date labels at the bottom of the chart
    if not outer_plots:  # use the main chart date labels
        for label in ax1.xaxis.get_ticklabels():
            label.set_rotation(45)
            label.set_size(7)
    else:
        for label in ax1.xaxis.get_ticklabels():
            label.set_size(0)  # inelegant way to remove dates labels

    # plt.show()
    return figure
    #
    # # save plot file as picture
    # file_name = general_utils.make_filepath(chart_dir, symbol, 'png')
    # figure.savefig(file_name, facecolor=figure.get_facecolor())
    # print ("Chart of symbol {} was saved".format(symbol))


i = 0


def snapshot(name, figure):
    global i
    print "snapshot {}".format(i)
    file_name = general_utils.make_filepath(chart_dir, name+str(i), 'png')
    figure.savefig(file_name, facecolor=figure.get_facecolor())
    i += 1


def mark_trigger(axis, x_loc, y_loc, trigger, figure):
    if trigger == 'OPEN':
        axis.annotate('open', xy=(x_loc, y_loc), xycoords='data', xytext=(0, -25), textcoords='offset points',
                      arrowprops=dict(facecolor='green', arrowstyle='simple'), fontsize=6, color='w', horizontalalignment='center', verticalalignment='bottom')
    if trigger == 'CLOSE':
        axis.annotate('close', xy=(x_loc, y_loc), xycoords='data', xytext=(0, 25), textcoords='offset points',
                      arrowprops=dict(facecolor='red', arrowstyle='simple'), fontsize=6, color='w', horizontalalignment='center', verticalalignment='top')


def draw_indicator_on_chart(subplot, label, values):
    global height, width, date, start_point
    color = '#e1edf9'  # TODO choose random colors or iterate over few
    #color = '#e1ed' +
    subplot.plot(date[-start_point:], values[-start_point:], color, label=label, linewidth=1)
    ma_leg = plt.legend(loc=9, ncol=2, prop={'size': 7}, fancybox=True, borderaxespad=0.)
    ma_leg.get_frame().set_alpha(0.4)
    text_ed = pylab.gca().get_legend().get_texts()
    pylab.setp(text_ed[0:5], color='w')


def draw_indicator_below_chart(axis, label, values, row_loc, row_span, figure, symbol):
    # TODO test support in multi plots indicators (as MACD)
    global height, width, date, start_point
    ax0 = plt.subplot2grid((height, width), (row_loc, 0), sharex=axis, rowspan=row_span, colspan=width, axisbg='#07000d')
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
    for label in ax0.xaxis.get_ticklabels():
        label.set_size(0)  # inelegant way to remove this label
    return ax0

