from .trades_statistics import calculate_trades_statistics
from numpy import std, average


"""
This file liable for the statistics calculation of the trading system.
It uses the statistic calculations of each trade in trading period of stock to retrieve the stock statistics, and
based on those, it derives the statistics of the whole trading system.
"""


def calculate_system_statistics(stock_data_table_dict, trade_system, start_date, end_date, period):
    """
    This function does the calculation of the systems and the stocks statistics.
    :param stock_data_table_dict: dictionary where the key is the stock symbol, and the value is tuple of:
    (trades_table, start_date, end_date, period_days)- all are match to the specific stock.
    trades_table is a DataFrame table contains all the trades on that stock,
    start_date and end_date are the first and the last day of original stock table (before the filtering),
    period is the total amount of trading days between the start and the end.
    So the format is: {SYMBOL1=(trades_table1, start_date1, end_date1, period_days1), SYMBOL2=...}
    :param trade_system: TradeSystem instance
    :param start_date: the earliest date that the system start being analyzed at
    :param end_date: the latest date of the analysis.
    :param period: the total amount of trading days.
    :return: tuple of: (SystemStatistics, [StockStatistics]), the second item is list contains all stock statistics.
    """
    direction = trade_system.get_direction()
    system_name = trade_system.get_name()

    # retrieve all the trade of all the stocks in the trade system
    system_trades = {}
    for stock in stock_data_table_dict:
        stock_trades = stock_data_table_dict.get(stock)[0]
        stock_start_date = stock_data_table_dict.get(stock)[1]
        stock_end_date = stock_data_table_dict.get(stock)[2]
        stock_period = stock_data_table_dict.get(stock)[3]
        # dictionary with stock symbols as keys and tuple of:(list of all trades of that stock as value, start_date, end_date, period) #TODO make it more friendly
        system_trades.update({stock: (calculate_trades_statistics(stock_trades, direction), stock_start_date,
                                      stock_end_date, stock_period)})

    stocks_statistics_list = []
    system_statistics = SystemStatistics(system_name, start_date, end_date, period, [], [], []) # init with empty vectors
    # iterate over all stocks create StockStatistics objects

    for stock in system_trades:
        trades_list, start, end, period = system_trades.get(stock)
        stock_statistics = StockStatistics(stock, start, end, period,
                                           [trade.get_duration() for trade in trades_list],
                                           [trade.get_profit_points() for trade in trades_list],
                                           [trade.get_profit_percentage() for trade in trades_list])
        stock_statistics.calculate_statistics()  # calculate each stock's statistics
        if not stock_statistics.is_empty():
            stocks_statistics_list.extend([stock_statistics])  # add it to the output list

        # extend system stats vectors with the stock's vector
        system_statistics.durations_vector += stock_statistics.durations_vector
        system_statistics.yields_points_vector += stock_statistics.yields_points_vector
        system_statistics.yields_percentages_vector += stock_statistics.yields_percentages_vector
    system_statistics.calculate_statistics()  # finally calculate the system stats, based on the concatenated vectors of all stocks

    return system_statistics, stocks_statistics_list


class StockStatistics:
    """
    Class that store the statistics of stock, and does the calculation of them.
    Some of the class statistics:
    + total number of trades
    + average gain ($/%) + stdev
    + profit/loss ratio ($:$)
    + %/# of winning trades
    + %/# of losing trades
    + max winning trade ($/%)
    + max losing trade ($/%)
    + average winning trade ($/%) + stdev
    + average losing trade ($/%) + stdev
    + % time of open position
    + average days of holding per trade

    """
    def __init__(self, symbol, start_date, end_date, period, durations_vector, yields_points_vector, yields_percentages_vector):

        self.name = symbol  # the symbol of the stock
        self.start_date = start_date
        self.end_date = end_date
        self.period = period
        self.empty = False  # flag to indicates if no trades have been done (possible when there's only open trigger)
        # All statistics calculations are based on the next 3 vectors:
        self.durations_vector = durations_vector
        self.yields_points_vector = yields_points_vector
        self.yields_percentages_vector = yields_percentages_vector
        
        # Derived vectors (order 0 statistics)
        self.profit_points_vector = []
        self.profit_percentages_vector = []
        self.loss_points_vector = []
        self.loss_percentages_vector = []

        # All following fields are calculated later on, by calling to calculate_statistics()
        # Accumulating fields (order 1 statistics)
        self.trades = 0  # total amount of trades
        self.total_holding_period = 0
        self.yield_points = 0.0  # in point ($)
        self.yield_percentages = 0.0  # in percentage (%)
        self.winning_trades = 0  # number of winning trades
        self.losing_trades = 0  # number of losing trades

        # Calculative fields (order 2 statistics)
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
        self.efficiency = 0.0  # % of time of open position

    def calculate_statistics(self):
        """
        This method calculates the stock statistics, that are based on the data vectors.
        It should be called once, only after all the data were collected into those vectors (basically this should be
        done on the class creation).
        """
        # first make the vector immutable
        self.durations_vector = tuple(self.durations_vector)
        self.yields_points_vector = tuple(self.yields_points_vector)
        self.yields_percentages_vector = tuple(self.yields_percentages_vector)
        assert len(self.durations_vector) == len(self.yields_points_vector) == len(self.yields_percentages_vector)
        if len(self.durations_vector) == 0:  # no trade- probably received open trigger without close trigger
            self.empty = True
            return

        self.profit_points_vector = [y for y in self.yields_points_vector if y > 0]
        self.profit_percentages_vector = [y for y in self.yields_percentages_vector if y > 0]
        self.loss_points_vector = [y for y in self.yields_points_vector if y < 0]
        self.loss_percentages_vector = [y for y in self.yields_percentages_vector if y < 0]

        self.profit_points_vector = tuple(self.profit_points_vector)
        self.profit_percentages_vector = tuple(self.profit_percentages_vector)
        self.loss_points_vector = tuple(self.loss_points_vector)
        self.loss_percentages_vector = tuple(self.loss_percentages_vector)

        # calculate first order statistics
        self.trades = len(self.durations_vector)
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
        self.efficiency = 1.0 * self.total_holding_period / self.period * 100.0

    def is_empty(self):
        return self.empty

    def to_dataframe(self):
        """ This class creates pandas DataFrame object containing the statistics for display"""
        pass
        # TODO


class SystemStatistics(StockStatistics):
    """
    This is the system statistics class, it extends the stock statistics class.
    [At the moment there is no different between them, so it is just the infrastructure]
    """
    # TODO add fields: average open trades at single point over time, max open trades on single point of time (may required to add dates per trade)