from pandas.io.data import DataReader
from datetime import datetime, timedelta
from symbols_list import make_filepath, get_stocks_symbols
from logbook import Logger
from symbols_list import DATA_PATH


log = Logger(__name__)


def pull_stocks_data(retries=3, start_date=None, end_date=None):
    """
    Pulling stocks raw data, of the stocks in the symbol list.
    :param retries: number of retries for getting each stock's data
    :param start_date: the first day of the data (datetime format), default value is 2 years before end_date.
    :param end_date: the last day of the data (datetime format), default value is today
    """
    symbols = get_stocks_symbols(write_to_files=False)
    log.notice("Starting to pull stocks data")
    end_date = datetime.today() if end_date is None else end_date
    start_date = end_date - timedelta(365*10)  # take 10 years backwards

    for retry in range(retries):
        for symbol in symbols:
            filepath = make_filepath(DATA_PATH+"symbols", symbol, 'csv')  # optimize by avoiding calling this function every time
            try:
                data = DataReader(symbol,  'yahoo', start_date, end_date, retry_count=3)
            except IOError as e:
                log.error("IOError for data query of symbol: {}\n\tError msg: {}".format(symbol, e))
                continue
            data.to_csv(filepath)
            symbols.pop(symbols.index(symbol))
        log.warning("Unable to get {} symbols on try #{}".format(len(symbols), retry+1))

    log.error("Unable to get {} symbols after {} retries:\n{}".format(len(symbols), retries, symbols))



if __name__ == '__main__':
    pull_stocks_data()



##############
##  PLAN B  ##
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
