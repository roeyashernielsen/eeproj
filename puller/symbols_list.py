import urllib2
import os



class Market():
    """
    Market class, contains the market name and the source url which for symbols list
    """
    def __init__(self, name, source):
        self.name = name
        self.soruce = source


nasdaq_url = 'http://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nasdaq&render=download'
nyse_url = 'http://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nyse&render=download'

nasdaq = Market('NASDAQ', nasdaq_url)
nyse = Market('NYSE', nyse_url)

markets = [nasdaq, nyse]


def get_stocks_symbols(create_files=True):
    """
    Return list contains all the symbols of stocks in the markets
    When create_files is true, create file with the companies data (name, industry, sector, market cap, etc...)
    for each market.
    """
    all_symbols = []

    for market in markets:
        symbols = []
        request = urllib2.Request(market.soruce)
        try:
            result = urllib2.urlopen(request)
        except urllib2.URLError as e:
            print "url error #{}: {}".format(e.errno, e.strerror)
            return

        data = result.readlines()

        # save all data to file
        if create_files:
            filepath = make_filepath(market.name, "data/markets_companies")
            companies = open(filepath, 'w')
            for line in data:
                companies.write(str(line))

        # parse the data to get list of symbols

        for company in data:
            symbol = company.split(',')[0][1:-1]
            symbols.extend([symbol])

        symbols.pop(0)  # exclude the first line - description line
        all_symbols.extend(symbols)

    return all_symbols


def make_filepath(filename, directory, extension=None):
    dir = "./" + directory + "/"
    if not os.path.exists(dir):
        os.makedirs(dir)
        print('new directory created at {}'.format(dir))
    filepath = dir + filename
    if extension:
        filepath += "." + extension
    return filepath


get_stocks_symbols()