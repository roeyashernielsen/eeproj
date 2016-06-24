import talib
"""
This file contains the functions that calculate the technical parameters values along time per stock data table
"""

def evaluate_technical_parameters(raw_stock_data, technical_parameters):
    """
    This function extends the table that contains the raw stock data, with the values of the technical indicators
    received as argument. The calculated values are added into new columns (vectors) within that table.
    Notice that the length of each of the new vectors is usually shorted than the time vector, since most of the
    technical indicators are functions defined as: R^n --> R, so the first output is function of the first n inputs.
    :param raw_stock_data: DataFrame table, contains open, high, low, close and volume vectors (columns).
    :param technical_parameters: list of TechnicalParameter objects, each contains the name of the technical indicator
    and other arguments needed for the calculation.
    :return: the stock_data table with the extra columns
    """
    # first calculate each indicator values and adds the vector to data table
    for technical_parameter in technical_parameters:
        values = calculate_technical_indicator(raw_stock_data, technical_parameter)
        raw_stock_data = extend_stock_table(raw_stock_data, values)

    # normalize data table to unify length (shorten the un fully rows)
    # TODO

    return raw_stock_data


def calculate_technical_indicator(stock_data, technical_parameter):
    """
    This function calculate technical indicator values according to the technical parameters.
    The function uses TA-Lib package for the calculations.
    :param stock_data: DataFrame table, contains open, high, low, close and volume vectors (columns).
    :param technical_parameter: TechnicalParameter object, contains the indicator name and the arguments needed for the
    calculation.
    :return: vectors contains the calculated values over time.

    """

    if technical_parameter.is_raw() or technical_parameter.is_numeric_value():
        return  # no need to calculate anything in this case
    arguments = talib_adapter(stock_data, technical_parameter)



def talib_adapter(stock_data, technical_parameter):
    """
    This function draw the field from the given params and adapt them to the inputs required for talib tools for
    calculation of technical indicators
    :return: OrderedDict contains arguments according to talib needs
    """
    inputs = dict(zip([title.lower() for title in stock_data.columns[:-1]], )


# for tests use TODO relocate
import random

def get_random_indicator():
    all_indicaotrs = talib.get_functions()
    return talib.abstract.Function(random.sample(all_indicaotrs, 1)[0])

