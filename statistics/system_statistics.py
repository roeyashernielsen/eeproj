from .trades_statistics import calculate_trades_statistics
from numpy import std, average

"""
This file liable for the statistics calculation of the trading system.
It uses the statistic calculations of each trade in trading period of stock to retrieve the stock statistics, and
based on those, it derives the statistics of the whole trading system.

LIST OF ALL STATISTICS:
System Statistics:
all the stock statistics plus:
    + start date, close date
    + period (days)
    + average open trades at single point over time
    + max open trades on single point of time

Stock Statistics:
    + total number of trades
    + average gain ($/%) + stdev
    + profit/loss ratio ($:$)
    + %/# of winning trades
    + %/# of losing trades
    + max winning trade ($/%)
    + max losing trade ($/%)
    + average winning trade ($/%) + stdev
    + average losing trade ($/%) + stdev
    + period (days)
    + % time of open position
    + average days of holding per trade


"""

"""
TODOs:
    1. finish SystemStatistics class, additional fields and override the calculation method
    2. write function that convert statistics to dataframe (or other represented frame)
    3. add documentation
    
"""

def calculate_system_statistics(stock_trade_table_dict, direction, period_days, start_date, end_date, system_name):
    """
    This function does the calculation of the systems and the stocks statistics.
    :param stock_trade_table_dict: dictionary where the key is the stock symbol, and the value is DataFrame object
    table that contains all the trades on that stock
    :param direction: the direction of the trade - long/short (define in the right enum)
    :return:
    """

    # retrieve all the trade of all the stocks in the trade system
    system_trades = {}  # dictionary with stock symbols as keys and list of all trades of that stock as value
    for stock in stock_trade_table_dict:
        system_trades.update({stock: calculate_trades_statistics(stock_trade_table_dict[stock], direction)})

    stocks_statistics_list = []
    system_statistics = SystemStatistics(system_name, period_days, [], [], [], start_date, end_date)
    for stock in system_trades:
        stock_statistics = StockStatistics(stock, period_days, [trade.get_duration() for trade in system_trades[stock]],
                                           [trade.get_profit_points() for trade in system_trades[stock]],
                                           [trade.get_profit_percentage() for trade in system_trades[stock]])
        stock_statistics.calculate_statistics()
        stocks_statistics_list.extend([stock_statistics])

        # extend system stats vectors with the stock's vector
        system_statistics.durations_vector += stock_statistics.durations_vector
        system_statistics.yields_points_vector += stock_statistics.yields_points_vector
        system_statistics.yields_percentages_vector += stock_statistics.yields_percentages_vector
    system_statistics.calculate_statistics()

    return system_name, stocks_statistics_list


class StockStatistics:
    """
    Class to store the statistics of stock
    """
    def __init__(self, symbol, period, durations_vector, yields_points_vector, yields_percentages_vector):

        self.name = symbol  # the symbol of the stock
        self.period = period
        # All statistics calculations are based on the next 3 vectors:
        self.durations_vector = durations_vector
        self.yields_points_vector = yields_points_vector
        self.yields_percentages_vector = yields_percentages_vector
        
        # Derived vectors (order 0 stats)
        self.profit_points_vector = [y for y in yields_points_vector if y > 0]
        self.profit_percentages_vector = [y for y in yields_percentages_vector if y > 0]
        self.loss_points_vector = [y for y in yields_points_vector if y < 0]
        self.loss_percentages_vector = [y for y in yields_percentages_vector if y < 0]

        # Accumulating fields (order 1 stats)
        self.trades = 0  # total amount of trades
        self.total_holding_period = 0
        self.yield_points = 0.0  # in point ($)
        self.yield_percentages = 0.0  # in percentage (%)
        self.winning_trades = 0  # number of winning trades
        self.losing_trades = 0  # number of losing trades

        # Calculative fields (order 2 stats)
        self.profit_loss_ratio_points = 0.0  # profit/loss ($/$)
        self.profit_loss_ratio_percentages = 0.0  # profit/loss (%/%)
        self.max_profit_points = 0.0  # the most profitable trade ($)
        self.max_loss_points = 0.0  # the most losing trade ($)
        self.max_profit_percentages = 0.0  # the most profitable trade (%)
        self.max_loss_percentages = 0.0  # the most losing trade (%)
        self.average_yield_points = 0.0
        self.stdev_yield_points = 0.0
        self.average_yield_percentages = 0.0
        self.stdev_yield_percentages = 0.0
        self.average_holding_period = 0.0
        self.stdev_holding_period = 0.0

    def calculate_statistics(self):
        """
        TODO
        :return:
        """
        # first make the vector immutable
        self.durations_vector = tuple(self.durations_vector)
        self.yields_points_vector = tuple(self.yields_points_vector)
        self.yields_percentages_vector = tuple(self.yields_percentages_vector)
        self.profit_points_vector = tuple(self.profit_points_vector)
        self.profit_percentages_vector = tuple(self.profit_percentages_vector)
        self.loss_points_vector = tuple(self.loss_points_vector)
        self.loss_percentages_vector = tuple(self.loss_percentages_vector)

        # calculate first order statistics
        self.trades = len(self.yields_points_vector)
        self.total_holding_period = sum(self.durations_vector)
        self.yield_points = sum(self.yields_points_vector)
        self.yield_percentages = sum(self.yields_percentages_vector)
        self.winning_trades = len(self.profit_points_vector)
        self.losing_trades = len(self.loss_points_vector)

        # calculate second order statistics
        self.profit_loss_ratio_percentages = sum(self.profit_percentages_vector) / sum(self.loss_percentages_vector)
        self.profit_loss_ratio_points = sum(self.profit_points_vector) / sum(self.loss_points_vector)
        self.max_profit_points = max(self.yields_points_vector)
        self.max_loss_points = min(self.yields_points_vector)
        self.max_profit_percentages = max(self.yields_percentages_vector)
        self.max_loss_percentages = min(self.yields_percentages_vector)
        self.average_yield_points = average(self.yields_points_vector)
        self.stdev_yield_points = std(self.yields_points_vector)
        self.average_yield_percentages = average(self.yields_percentages_vector)
        self.stdev_yield_percentages = std(self.yields_percentages_vector)

        self.average_holding_period = average(self.durations_vector)
        self.stdev_holding_period = std(self.durations_vector)


    def to_dataframe(self):
        pass
        # TODO



class SystemStatistics(StockStatistics):
    def __init__(self, system_name, period, durations_vector, yields_points_vector, yields_percentages_vector,
                 start_date, end_date):

        StockStatistics.__init__(self, system_name, period, durations_vector, yields_points_vector,
                                 yields_percentages_vector)

        self.start_date = start_date
        self.end_date = end_date
        # TODO add the additional fields


    def calculate_statistics(self):
        # TODO override and calculate the additional fields
        pass
