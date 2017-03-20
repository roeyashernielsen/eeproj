from processor.calculate_technical_parameters import *
from processor.filtering import *
from utils import general_utils
import timeit

start_date = None
end_date = None
trading_days = 0

def run_system_on_market(trade_system):
    path = "./data/bench_short/"
    all_stocks = general_utils.get_all_stocks(path)
    indicators = general_utils.get_indicators(trade_system)

    global start_date, end_date, trading_days
    start_date, end_date, trading_days = general_utils.get_system_times(all_stocks)

    # processing stages
    # extend stock tables with the required technical parameters
    start_time = timeit.default_timer()
    extended = dict((symbol, evaluate_technical_parameters(stock, indicators)) for symbol, stock in all_stocks.items())
    end_time = timeit.default_timer()
    print ("Elpased time for Extension process is: {}".format(end_time - start_time))
    # filter stock tables to reveal the trades
    start_time = timeit.default_timer()
    filtered_shrunk = dict((symbol, filter_stock_data(trade_system, symbol, stock)[0]) for symbol, stock in extended.items())
    end_time = timeit.default_timer()
    print ("Elpased time for Filtering process is: {}".format(end_time - start_time))


