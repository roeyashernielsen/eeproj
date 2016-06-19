import
"""
This file contains the functions that calculate the technical parameters values along time per stock data table
"""

def calculate_technical_indicator(raw_stock_data, technical_parameters):
    """
    This function extends the table that contains the raw stock data, with the values of the technical indicators
    received as argument. The calculated values are added into new columns (vectors) within that table.
    Notice that the length of each of the new vectors is usually shorted than the time vector, since most of the
    technical indicators are functions defined as: R^n --> R, so the first output is function of the first n inputs.
    :param raw_stock_data: DataFrame table, contains open, high, low, close and volume vectors (columes).
    :param technical_parameters: list of TechnicalParameter objects, each contains the name of the technical indicator
    and other arguments needed for the calculation.
    :return: the stock_data table with the extra columns
    """
