import urllib2
import os
from logbook import Logger, StreamHandler
import sys
from .__init__ import *
StreamHandler(sys.stdout).push_application()
log = Logger(__name__)



class MarketData():
    """
    Market class, contains the market name and the source url which for symbols list
    """
    def __init__(self, name, source):
        self.name = name
        self.soruce = source


nasdaq_url = 'http://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nasdaq&render=download'
nyse_url = 'http://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nyse&render=download'

nasdaq = MarketData('NASDAQ', nasdaq_url)
nyse = MarketData('NYSE', nyse_url)

markets = [nasdaq, nyse]


def get_stocks_symbols(write_to_files=True):
    """
    Return list contains all the symbols of stocks in the markets
    When write_to_files is true, create file with the companies data (name, industry, sector, market cap, etc...)
    for each market.
    """
    all_symbols = []
    log.info("Pulling markets symbols")
    for market in markets:
        symbols = []
        request = urllib2.Request(market.soruce)
        try:
            result = urllib2.urlopen(request)
        except urllib2.URLError as e:
            log.error("url error #{}: {}".format(e.errno, e.strerror))
            return

        data = result.readlines()

        # save all data to file
        if write_to_files:
            filepath = make_filepath(DATA_PATH+"companies", market.name)
            companies = open(filepath, 'w')
            for line in data:
                companies.write(str(line))

        # parse the data to get list of symbols
        for company in data:
            symbol = company.split(',')[0][1:-1]
            symbols.extend([symbol])

        symbols.pop(0)  # exclude the first line - the description line (at the head of the table)
        all_symbols.extend(symbols)

    return all_symbols


def make_filepath(directory, filename, extension=None):
    """
    Create file in path = directory/filename.extension. Also create the directory it doesn't exist.
    :return: The file path
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
        log.info('New directory was created at {}'.format(os.path.abspath('.')+'/'+directory))
    filepath = directory + '/' + filename
    if extension:
        filepath += "." + extension
    return filepath


if __name__ == '__main__':
    get_stocks_symbols()
