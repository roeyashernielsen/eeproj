from pandas import DataFrame
from utils.enums import STOCK_DATA_COLUMNS
import os
import shutil
from datetime import datetime
import ipdb
import pandas
import random
import numpy

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


def get_technical_parameters(trade_system):
    """
    This function retrieves all the technical parameters out of trade system
    """
    technical_parameters = []
    for rule in [trade_system.get_open_rule(), trade_system.get_close_rule()]:
        for clause in rule.get_clauses():
            for term in clause.get_terms():
                technical_parameters.extend([term.get_technical_parameter_1(), term.get_technical_parameter_2()])


def get_all_stocks(path):
    stocks = {}
    for csv_file in os.listdir(path):
        if csv_file.endswith(".csv"):
            stocks[csv_file.rsplit('.', 1)[0]] = pandas.read_csv(path + csv_file)
    return stocks


def get_indicators(trade_system, remove_duplication=True):
    indicators = []
    terms = []
    clauses = trade_system.get_open_rule().get_clauses() + trade_system.get_close_rule().get_clauses()

    for clause in clauses:
        for term in clause.get_terms():
            terms.append(term)

    for term in terms:
        tp1 = term.get_technical_parameter_1()
        tp2 = term.get_technical_parameter_2()
        if tp1.is_technical_indicator():
            indicators.append(tp1)
        if tp2.is_technical_indicator():
            indicators.append(tp2)
    if remove_duplication:
        return remove_duplicate_indicators(indicators)
    else:
        return indicators


def indicator_equality(indicator1, indicator2):
    if indicator1.get_name == indicator2.get_name:
        if indicator1.get_timeperiod == indicator2.get_timeperiod:
            return True
    return False


def remove_duplicate_indicators(indicators):
    """
    The function get list of indicators and return list of indicators without any duplicate items.
    The equality of items set by indicator_equality function
    :param indicators: list of indicators
    :return: list without duplicate indicators
    """
    res = []
    for indicator1 in indicators:
        flag = True
        for indicator2 in res:
            if indicator_equality(indicator1, indicator2):
                flag = False
        if flag:
            res.append(indicator1)
    return res


def get_stat_dict(full, filtered):
    res = {}
    for k in filtered.keys():
        filtered_table = filtered.get(k)
        l = len(filtered_table)
        if l:
            start = filtered_table.iloc[0, 0]
            end = filtered_table.iloc[l - 1, 0]
            start_date = datetime.strptime(start, "%Y-%m-%d")
            end_date = datetime.strptime(end, "%Y-%m-%d")
            term = numpy.busday_count(start_date, end_date)
            res[k] = (filtered_table, start_date, end_date, term)
    return res


def list_to_dataframe(field_dict, obj_list):

    list_row = []
    for obj in obj_list:
        row = {}
        for field, col in field_dict.items():
            if hasattr(obj, field):
                row[col] = getattr(obj, field)
        list_row.append(row)

    return pandas.DataFrame(list_row, columns=(field_dict.values()))


def copy_subset_of_files_to_dir(ammount, dir):
    target = dir + "subset"
    files = [file for file in os.listdir(dir) if os.path.isfile(os.path.join(dir, file))]
    if not os.path.exists(target):
        os.makedirs(target)
    samples = set()
    while len(samples) <= ammount:
        index = random.randint(0, len(files))
        if index not in samples:
            if (os.path.isfile(dir + files[index]) and os.path.isfile("./data/demo_current/symbols/" + files[index])):
                shutil.copy2(dir + files[index], "./data/subset_past/")
                shutil.copy2("./data/demo_current/symbols/" + files[index], "./data/subset_present/")
                samples.add(index)
                print files[index] + "was added"



if __name__ == '__main__':
    copy_subset_of_files_to_dir(202,"./data/demo_past/symbols/")