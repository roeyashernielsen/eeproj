from utils.general_utils import *
from trade_system.trade_system import TradeSystem
from pandas import DataFrame, Series
from utils.enums import STOCK_DATA_COLUMNS as COLUMNS  # the columns name in stock_data table
from logbook import Logger, StreamHandler
from utils import enums
import sys
from math import isnan

StreamHandler(sys.stdout).push_application()
log = Logger(__name__)
"""
This module is liable for the trades searching, that defined by Trad System. Basically it receive Trade System (open and
close rules) and stock data (represented in data frame) and locking for lines (i.e. trading days) that match the trade
system rules. by doing that it filters the data so finally what left are the trades that fits the trade system.
"""


def filter_stock_data(trade_system, stock_data):
    """
    This function receive trade system and data, and looking for potential trades, by the defined rules of the trade
    system. It going through all the data table, and try to apply the rules on each row of the table. rows that applies
    the rules are marked by the type of trigger (open trade or close trade), and finally it clear the table from all
    the unmarked rows. So at the end we have shrunk version of the table, contains the trades rows only.
    :param trade_system: TradeSystem object- define the trade system uses for filtering
    :param stock_data: DataFrame table, contains the stock's indicator values
    :return: shrunk stock data table, contains the rows marked by trade triggers
    """
    type_checking(TradeSystem, trade_system)
    type_checking(DataFrame, stock_data)

    # add columns to mark whether the line applies the trade system rules or not, by trigger type. Initialized to False
    stock_data[COLUMNS.open_trigger] = Series(False, index=stock_data.index)
    stock_data[COLUMNS.close_trigger] = Series(False, index=stock_data.index)

    _mark_trigger_lines(trade_system, stock_data)

    filtered_stock_data = _remove_untriggered_lines(stock_data)

    return filtered_stock_data


def _remove_untriggered_lines(stock_data):
    """
    remove rows that aren't match the trade system (according to the mark column)
    :return: new table without the dropped rows.
    """
    for row in stock_data.index:
        if not stock_data.get_value(row, COLUMNS.open_trigger) and not stock_data.get_value(row, COLUMNS.close_trigger):
            stock_data = stock_data.drop(row)
    return stock_data


def _mark_trigger_lines(trade_system, stock_data):
    """
    Test every line in stock_data to see if it matches the trade system, and mark it accordingly.
    Stateful mode- no allows only single open position at a time.
    Checks an enforces stop loss
    """
    entering_price = None  # the entering price of the current position, if there's open one.

    for row in stock_data.index[:-1]:  # ignore the last day (war mode) # TODO fix in order to get live triggers
        date = stock_data.get_value(row, COLUMNS.date)
        symbol = None  # TODO symbol from metadata on the logs prints
        for rule in [trade_system.get_open_rule(), trade_system.get_close_rule()]:

            # check closing due to stop loss
            if entering_price and row > 0:
                current_price = stock_data.get_value(row, COLUMNS.close)
                previous_price = stock_data.get_value(row - 1, COLUMNS.close) if row > 0 else None
                if is_stop_loss_reached(current_price, entering_price, trade_system.get_stop_loss(), trade_system.get_direction()) or \
                        is_stop_loss_reached(current_price, previous_price, trade_system.get_moving_stop_loss(), trade_system.get_direction()):
                    log.info("Trade reached stop-loss point, setting close trigger. symbol: {}, date: {}".format(symbol, date))
                    stock_data.set_value(row, COLUMNS.close_trigger, True)
                    entering_price = None

            # check open position triggers
            if rule is trade_system.get_open_rule():
                open_trigger = is_rule_applied_by_stock(rule, stock_data, row)
                if open_trigger:
                    if entering_price:
                        log.error("Received open trigger while having open position. Trigger is ignored. Date: {} symbol: {}".format(date, symbol))
                    else:
                        stock_data.set_value(row+1, COLUMNS.open_trigger, open_trigger)
                        entering_price = stock_data.get_value(row+1, COLUMNS.open) if row+1 < len(stock_data) else None
                        log.info("Open trigger was marked for TODO_ADD_SYMBOL at {}".format(row, date))

            # check close position triggers
            if rule is trade_system.get_close_rule():
                close_trigger = is_rule_applied_by_stock(rule, stock_data, row)
                if not entering_price:
                    log.error("Received close trigger while no position is open. Trigger is ignored. Date: {} symbol: {}".format(date, symbol))
                else:
                    stock_data.set_value(row+1, COLUMNS.close_trigger, close_trigger)
                    entering_price = None
                    log.info("Close trigger was marked for TODO_ADD_SYMBOL at {}".format(stock_data.get_values(row, date)))

        # check for open and close triggers on the same day
        if stock_data.get_value(row, COLUMNS.open_trigger) and stock_data.get_value(row, COLUMNS.close_trigger):
            log.warning("Stock {} were trigger for open and close at the same day ({})".format(symbol, date))




def is_rule_applied_by_stock(rule, stock_data, index):
    """
    Check if the trade system rule is applied by the stock data at the particular row.
    :param rule: Rule class instance, in SOP boolean formula format
    :param stock_data: table contains the daily stock data
    :param index: the current time index that is tested
    :return: True if the rule satisfied (at least one of the clauses), False otherwise
    """
    for clause in rule.get_clauses():
        # since the rule is SOP boolean formula, it is sufficient that single clause will be satisfied.
        if is_clause_applied_by_stock(clause, stock_data, index):
            return True


def is_clause_applied_by_stock(clause, stock_data, index):
    """
    Check if the trade system clause is applied by the stock data at the particular row.
    :param clause: Clause class instance.
    For the rest of the arguments see "is_rule_applied_by_stock()"
    :return: True if the clause satisfied (i.e. all of the terms are satisfied), False otherwise
    """
    # clauses contains terms with AND between, therefore all the terms must be satisfied
    return all([is_term_applied_by_stock(term, stock_data, index) for term in clause.get_terms()])


def is_term_applied_by_stock(term, stock_data, index):
    """
    Check if the trade system term is applied by the stock data at the particular row.
    :param term: Term class instance.
    For the rest of the arguments and return value see "is_rule_applied_by_stock()"
    :return: True if the term is satisfied, False otherwise
    """
    # retrieve the data of both technical params
    param_1_values = _get_relevant_stock_data_sections(term.get_technical_parameter_1(), stock_data, index)
    if term.get_technical_parameter_2().is_numeric_value():
        numeric_value = term.get_technical_parameter_2().get_numeric_value()
        param_2_values = numeric_value, numeric_value  # tuple of same value
    else:
        param_2_values = _get_relevant_stock_data_sections(term.get_technical_parameter_2(), stock_data, index)

    #if any([value for value in param_1_values+param_2_values if isnan(value)]):  # some (indicators) values may be NaN
     #   return False

    relation = term.get_relation()
    # check relations logic
    if relation is enums.RELATIONS.greater:
        return param_1_values[1] > param_2_values[1]
    if relation is enums.RELATIONS.less:
        return param_1_values[1] < param_2_values[1]
    if relation is enums.RELATIONS.crossover_below:
        return param_1_values[0] < param_2_values[0] and param_1_values[1] > param_2_values[1]
    if relation is enums.RELATIONS.crossover_above:
        return param_1_values[0] > param_2_values[0] and param_1_values[1] < param_2_values[1]
    if relation is enums.RELATIONS.crossover:  # == crossover_below or crossover_above
        return (param_1_values[0] < param_2_values[0] and param_1_values[1] > param_2_values[1]) or \
               (param_1_values[0] > param_2_values[0] and param_1_values[1] < param_2_values[1])


def is_stop_loss_reached(current_price, referenced_price, stop_loss_percentage, direction):
    """
    Check if the current price of the trade reached the stop lost limitations
    :param current_price: closure price of the current day
    :param referenced_price: the reference price which stop loss is tested by
    :param stop_loss_percentage: percentages value of the stop loss
    :param direction: type of trade - long/short
    :return: True in case current price reached the stop loss limitation, False otherwise.
    """
    if direction == enums.TRADE_DIRECTIONS.short:
        return ((current_price - referenced_price) / referenced_price) * 100.0 > stop_loss_percentage
    if direction == enums.TRADE_DIRECTIONS.long:
        return ((referenced_price - current_price) / referenced_price) * 100.0 > stop_loss_percentage


def _get_relevant_stock_data_sections(technical_param, stock_data, index):
    """
    Get the relevant values of the technical parameter from stock data at given index.
    The needed values are of the specific day plus the day before.
    Basically this function retrieve the values out of that stock data table at the intended column and row.
    :param technical_param: TechnicalParameter class object
    For the rest of the arguments and return value see "is_rule_applied_by_stock()"
    :return: tuple with the needed values, in form: (day_before_value, wanted_day_value)
             If wanted day is the first day, then day_before_value is None.
    """
    wanted_day_index = index - technical_param.get_shifting()  # retrieve the row index
    wanted_day_param = technical_param.get_title()  # retrieve the column index
    wanted_day_value = stock_data.get_value(wanted_day_index, wanted_day_param)
    try:
        previous_day_value = stock_data.get_value(wanted_day_index-1, wanted_day_param)
    except KeyError:  # out of bounds
        previous_day_value = None
    return previous_day_value, wanted_day_value





def csv_to_data_frame(path):
    DataFrame.from_csv(path, index_col=None, infer_datetime_format=True)




