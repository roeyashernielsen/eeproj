from .trades_statistics import calculate_trades_statistics

"""
This file liable for the statistics calculation of the trading system.
It uses the statistic calculations of each trade in trading period of stock to retrieve the stock statistics, and
based on those, it derives the statistics of the whole trading system.

LIST OF ALL STATISTICS:
System Statistics:
all the stock statistics plus:
    + average open trades at single point over time
    + max open trades on single point of time

Stock Statistics:
    + start date, close date
    + time period (days)
    + total number of trades
    + average gain ($/%) + stdev
    + profit/loss ratio ($:$)
    + %/# of winning trades
    + %/# of losing trades
    + max winning trade ($/%)
    + max losing trade ($/%)
    + average winning trade ($/%) + stdev
    + average losing trade ($/%) + stdev
    + average term of holding
    + % time of open position
"""


def calculate_system_statistics(stock_trade_table_list, direction):
    """
    This function does the calculation of the systems and the stocks statistics.
    :param stock_trade_table_list: list of DataFrame objects, each represents the trading history of a stock.
    :param direction: the direction of the trade - long/short (define in the right enum)
    :return:
    """

    # retrieve all the trade of all the stocks in the trade system
    system_trades = []  # list of lists of stock trades
    for stock_trade_table in stock_trade_table_list:
        system_trades.extend([calculate_trades_statistics(stock_trade_table_list, direction)])


