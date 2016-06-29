from utils.enums import STOCK_DATA_COLUMNS as COLUMNS
from .trade import Trade
import ipdb

"""
This file liable for the statistics calculations of each trade among all the trades that been done on stock.
Those trades are represented by the stock data table post the processing progress (shrunk table contains only rows
contains the open and close triggers).
The trade statistics are holden within Trade class objects.
"""


def calculate_trades_statistics(stock_trades_table, direction):
    """
    This function calculates statistics of each trade over the stock trading history
    :param stock_trades_table: DataFrame table filled with the rows of the open days and close days (the filtered
    stock_data_table).
    :param direction: the direction of the trade - long/short (define in the right enum)
    :return: list of all historical trades on this stock, each represented by Trade object, that contains some basic
    data will be needed for the stock and system statistics calculations.
    """
    check_filtered_data(stock_trades_table)
    stock_trades = retrieve_trades(stock_trades_table, direction)
    return stock_trades


def check_filtered_data(stock_trades_table):
    """
    Check basic assumption, that are needed for the rest of the statistics calculation on the table represents the
    trades history.
    :param stock_trades_table: DataFrame table filled with the rows of the open days and close days (the filtered
    stock_data_table).
    :return:
    """
    # check that every open trade has closurez
    opens, closes = 0,0
    for row in stock_trades_table.index:
        if stock_trades_table.get_value(row, COLUMNS.open_trigger):
            opens += 1
        if stock_trades_table.get_value(row, COLUMNS.close_trigger):
            closes += 1
    assert closes == opens or closes == opens-1  # at most there is one unclosed trade

    # TODO add more checks


def retrieve_trades(stock_trades_table, direction):
    """
    retrieve all the closed trades from the data table and put them into list of Trades objects.
    :param stock_trades_table: DataFrame table filled with the rows of the open days and close days (the filtered
    stock_data_table).
    :param direction: the direction of the trade - long/short (define in the right enum)
    :return: list of Trade objects, each contains the opening and closing day data and more.
    """
    def try_to_add_closed_trade(trade_and_index):
        """
        add the trade to all_trades only if it closed and reset the current trade
        :param trade_and_index: tuple of (trade_data, table index)
        """
        if trade_and_index[0] and trade_and_index[1]:  # both are not None
            all_trades.extend([Trade(trade_and_index[0], trade_and_index[1], direction)])  # stamp the trade as close and add it to trades list

            return [None, None]  # reset trade_and_index
        return trade_and_index

    all_trades = []
    trade = [None, None]  #[trade, index]
    for index in stock_trades_table.index:
        if stock_trades_table.get_value(index, COLUMNS.close_trigger):
            trade[1] = (stock_trades_table.loc[index], index)  # a tuple of the data and the index
            trade = try_to_add_closed_trade(trade)
        if stock_trades_table.get_value(index, COLUMNS.open_trigger):
            trade[0] = (stock_trades_table.loc[index], index)  # a tuple of the data and the index
            trade = try_to_add_closed_trade(trade)
    return all_trades








