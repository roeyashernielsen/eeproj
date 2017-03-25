import talib
from collections import OrderedDict
from logbook import Logger, StreamHandler
import sys

StreamHandler(sys.stdout).push_application()
log = Logger(__name__)

"""
This file contains the functions that calculate the technical parameters values along time per stock data table
"""

def evaluate_technical_parameters(raw_stock_data, technical_parameters):
    """
    This function extends the table that contains the raw stock data, with the values of the technical indicators
    received as argument. The calculated values are added into new columns (vectors) within that table.
    Notice that the effective length of each of the new vectors is usually shorted than the time vector, since most of
    the technical indicators are functions defined as: R^n --> R, so the first output is function of the first n inputs.
    Those NaN values are still part of the calculated vector, and are treated in the next level (filtering).
    :param raw_stock_data: DataFrame table, contains open, high, low, close and volume vectors (columns).
    :param technical_parameters: list of TechnicalParameter objects, each contains the name of the technical indicator
    and other arguments needed for the calculation.
    :return: the stock_data table with the extra columns
    """
    # first calculate each indicator values and adds the vector to data table
    for technical_parameter in technical_parameters:
        if technical_parameter.is_technical_indicator():  # no calculation for numeric values (e.g)
            values, technical_indicator = calculate_technical_indicator(raw_stock_data, technical_parameter)
            raw_stock_data = extend_stock_table(raw_stock_data, values, technical_parameter.get_title(), technical_indicator)

    return raw_stock_data


def calculate_technical_indicator(stock_data, technical_parameter):
    """
    This function calculate technical indicator values according to the technical parameters.
    The function uses TA-Lib package for the calculations.
    :param stock_data: DataFrame table, contains open, high, low, close and volume vectors (columns).
    :param technical_parameter: TechnicalParameter object, contains the indicator name and the arguments needed for the
    calculation.
    :return: tuple contains: vectors contains the calculated values over time, the technical indicator object (TA-Lib's)
    """
    arguments = talib_adapter(stock_data, technical_parameter)
    technical_indicator = talib.abstract.Function(technical_parameter.get_name())
    technical_values = technical_indicator(arguments, timeperiod=technical_parameter.get_timeperiod()) # TODO this is workaround, fixing talib_adapter should fix it
    return technical_values, technical_indicator


def talib_adapter(stock_data, technical_parameter):
    """
    This function draw the field from the given params and adapt them to the inputs required for talib tools for
    calculation of technical indicators
    :return: OrderedDict contains arguments according to talib needs (....need to be fixed)
    """
    talib_inputs = OrderedDict()
    # set the raw data values
    sd = stock_data
    columns = [sd.Open.values, sd.High.values, sd.Low.values, sd.Close.values, sd.Volume.values]
    raw_data = OrderedDict(zip([title.lower() for title in sd.columns[1:-1]], columns))
    talib_inputs.update(raw_data)
    return talib_inputs
    #TODO fix so all the arguments wil retrieved (not only the raw data array)
    """
    # set common arguments
    if technical_parameter.get_timeperiod():
        period = OrderedDict(timeperiod=technical_parameter.get_timeperiod())
        talib_inputs.update(period)

    # rest arguments should be given as kwargs
    talib_inputs.update(OrderedDict(technical_parameter.kwargs))

    return talib_inputs
    """

def extend_stock_table(stock_data, new_columns, column_name, technical_indicator):
    """
    Adds new_column into stock_data table. Extends table with the additional vector under the given name.
    :param stock_data: DataFrame of stock data
    :param new_columns: vectors contains the new values (the number depends on the amount of output vector of the
    indicator)
    :param column_name: the title will be given to the added values
    :param technical_indicator: TA-Lib instance of the technical indicator
    :return: The extended stock_data
    """
    # put single vector output into list, to fit with the many vectors output
    # TODO add support to multi vectors- starting on UI design level
    if len(technical_indicator.output_names) > 1:
        log.critical("Not support in multi vectors indicator at this point ({})".format(technical_indicator))
        return
    # sanity checks
    log.warn("stock data and the additional vector length are different") if len(stock_data) != len(new_columns) else None
    #log.warn("column {} already exist in stock data".format(column_name)) if stock_data.get(column_name) is not None else None
    stock_data[column_name] = new_columns
    return stock_data

# for tests use TODO relocate
import random

def get_random_indicator():
    all_indicaotrs = talib.get_functions()
    return talib.abstract.Function(random.sample(all_indicaotrs, 1)[0])

