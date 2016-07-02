from pandas import DataFrame
from utils.enums import STOCK_DATA_COLUMNS
import os

import ipdb

#from logbook import Logger
"""
file to put all the general utils in it
"""
#from logger.__init__  import log_handler
#log_handler.push_application()
#log = Logger(__name__)

def type_checking(expected_type, *objects):
    """
    Checks that each object in objects is of the expected type, otherwise raise TypeError
    @:param expected_type: also can be a list of type. Is so, it sufficient that one of the types is fit with the objects
    """
    assert objects
    if type(expected_type) is list or type(expected_type) is tuple:
        if any([object_i for object_i in objects if [not isinstance(object_i, e_type) for e_type in expected_type]]):
            raise TypeError
    else:
        if any([object for object in objects if not isinstance(object, expected_type)]):
            raise TypeError


def csv_file_to_data_frame(path):
    return DataFrame.from_csv(path, index_col=None, infer_datetime_format=True)


def make_filepath(directory, filename, extension=None):
    """
    Create file in path = directory/filename.extension. Also create the directory it doesn't exist.
    :return: The file path
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
        # log.info('New directory was created at {}'.format(os.path.abspath('.')+'/'+directory))
    filepath = directory + '/' + filename
    if extension:
        filepath += "." + extension
    return filepath


def get_system_times(stock_data_table_dict):
    """
    Retrieves the start date, end date and period of the system out of the data from stock_data_table_dict.
    Take the earliest start date, latest end date and the max period time among the stocks.
    :param stock_data_table_dict: dictionary of  symbol--> stock data table
    :return: tuple of (start_date, end_date, period)
    """
    start_dates = [stock_data.head(1).Date.values for stock_data in stock_data_table_dict.values()]
    end_dates = [stock_data.tail(1).Date.values for stock_data in stock_data_table_dict.values()]
    periods = [len(stock_data) for stock_data in stock_data_table_dict.values()]
    return min(start_dates)[0], max(end_dates)[0], max(periods)

