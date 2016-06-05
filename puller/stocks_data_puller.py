
##############
#  OPTION A  #
##############
import time

from pandas.io.data import DataReader
from datetime import datetime, timedelta
from symbols_list import get_stocks_symbols, make_filepath
print "Global scope stocks_data_puller.py"
symbols = get_stocks_symbols(create_files=True)

#TODO add smart way to get stock symbols

def pull_stocks_data(retries=3, start_date=None, end_date=None):
    """
    Pulling stocks raw data, of the stocks in the symbol list.
    :param retries: number of retries for getting each stock's data
    :param start_date: the first day of the data (datetime format), default value is 2 years before end_date.
    :param end_date: the last day of the data (datetime format), default value is today
    """
    print "Starting to pull stocks data"
    end_date = datetime.today() if end_date is None else end_date
    start_date = end_date - timedelta(365*2)

    for symbol in symbols:
        filepath = make_filepath(symbol, 'data/symbols', 'csv')  # optimize by avoiding calling this function every time
        try:
            data = DataReader(symbol,  'yahoo', start_date, end_date)
        except IOError as e:
            print "IOError for data query of symbol: {}.\nError msg: {}".format(symbol, e)
            continue
        data.to_csv(filepath)
        symbols.pop(symbols.index(symbol))
    end = time.time()

    print "Unable to get {} symbols:\n{}".format(len(symbols), symbols)



if __name__ == '__main__':
    import timeit
    print ("Pulled stocks data.\n This took {} seconds".format(pull_stocks_data()))



##############
#  OPTION B  #
##############

# import urllib
# import os
#
# base_url = "http://ichart.finance.yahoo.com/table.csv?s="
# def make_url(ticker_symbol):
#     return base_url + ticker_symbol
#
# output_path = "~/trendy/dev/puller/data"
# def make_filename(ticker_symbol, directory="S&P"):
#     dir = output_path + "/" + directory + "/"
#     filepath = dir + ticker_symbol + ".csv"
#     if not os.path.exists(dir):
#         os.makedirs(dir)
#     return filepath
#
#
# def pull_historical_data(ticker_symbol, directory="S&P"):
#     try:
#         urllib.urlretrieve(make_url(ticker_symbol), make_filename(ticker_symbol, directory))
#     except urllib.ContentTooShortError as e:
#         outfile = open(make_filename(ticker_symbol, directory), "w")
#         outfile.write(e.content)
#         outfile.close()
