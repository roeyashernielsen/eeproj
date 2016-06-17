from utils.general_utils import *
from utils import enums
from trade_system.trade_system import TradeSystem
from pandas import DataFrame, Series
from utils.enums import STOCK_DATA_COLUMNS as COLUMNS  # the columns name in stock_data table
"""
This module is liable for the trades searching, that defined by Trad System. Basically it receive Trade System (open and
close rules) and stock data (represented in data frame) and locking for lines (i.e. trading days) that match the trade
system rules. by doing that it filters the data so finally what left are the trades that fits the trade system.
"""


def filter_stock_data(trade_system, stock_data):
    """
    ???
    :param trade_system: TradeSystem object- define the trade system uses for filtering
    :param stock_data: DataFrame table, contains the stock's indicator values
    :return:
    """
    type_checking(TradeSystem, trade_system)
    type_checking(DataFrame, stock_data)

    # add columns to mark whether the line applies the trade system rules or not. Initialized to False
    stock_data[COLUMNS.OPEN_TRIGGER] = Series(False, index=stock_data.index)
    stock_data[COLUMNS.CLOSE_TRIGGERr] = Series(False, index=stock_data.index)

    _mark_trigger_lines(trade_system, stock_data)

    _remove_untriggered_lines(stock_data)


def _remove_untriggered_lines(stock_data):
    """
    remove rows that aren't match the trade system (according to the mark column)
    """
    for row in range(len(stock_data.index)):
        if not (stock_data.loc[row][COLUMNS.OPEN_TRIGGER] or stock_data.loc[row][COLUMNS.CLOSE_TRIGGER]):
            stock_data.drop(row)


def _mark_trigger_lines(trade_system, stock_data):
    """
    test every line in stock_data to see if it matches the trade system, and mark it accordingly.
    """
    for rule in [trade_system.get_open_rule(), trade_system.get_close_rule()]:
        for row in range(len(stock_data.index)):
            if rule is trade_system.get_open_rule():
                stock_data.set_value(row, COLUMNS.OPEN_TRIGGER, is_rule_applied_by_stock(rule, stock_data, row))
            if rule is trade_system.get_close_rule():
                stock_data.set_value(row, COLUMNS.CLOSE_TRIGGER, is_rule_applied_by_stock(rule, stock_data, row))


def is_rule_applied_by_stock(rule, stock_data, index):
    """
    Check if the trade system rule is applied by the stock data at the particular row.
    :param rule: Rule class instance, in SOP boolean formula format
    :param stock_data: tables contains the stock data over time
    :param index: the current time index that is tested
    :return: True if the rule satisfied, False otherwise
    """
    for clause in rule.get_clauses():
        # since the rule is SOP boolean formula, it is sufficient that single clause will be satisfied.
        if is_clause_applied_by_stock(clause, stock_data, index):
            return True


def is_clause_applied_by_stock(clause, stock_data, index):
    """
    Check if the trade system clause is applied by the stock data at the particular row.
    :param clause: Clause class instance.
    :param stock_data: tables contains the stock data over time
    :param index: the current time index that is tested
    :return: True if the rule satisfied, False otherwise
    """
    '''
    clause = Technical_param relation Technical_param/value
    '''
    # TODO
    #first_param_value = get





def csv_to_data_frame(path):
    DataFrame.from_csv(path, index_col=None, infer_datetime_format=True)




