from utils import general_utils as gu
from trade_system.technical_parameter import TechnicalParameter
from utils.enums import SUPPORTED_INDICATORS as IND, NUMERIC_VALUE as NV
from logbook import Logger, StreamHandler
from trade_system.rule import Rule, Clause
from utils.enums import RELATIONS, TRADE_DIRECTIONS
from trade_system.trade_system import TradeSystem
from processor.calculate_technical_parameters import calculate_technical_indicator, talib_adapter, evaluate_technical_parameters
from trade_system.term import Term
from statistics.system_statistics import calculate_system_statistics
from management.main import get_all_stocks, get_indicators
import sys
from management.main import get_stat_dict
from processor.filtering import filter_stock_data
from ipdb import set_trace
from copy import copy
from management.main import main
from utils.general_utils import get_system_times

import ipdb

StreamHandler(sys.stdout).push_application()
log = Logger(__name__)

"""i
This file testing the algorithm of extending stock data table with columns of technical parameters.
The goals is to test the interface, and the correctness of the results.
Testing the functions in calculate_technical_parameter.py
"""

sample_file = './tests/sample_file.csv'
sample_data = gu.csv_file_to_data_frame(sample_file)

# Hard coded technical indicators
rsi10 = TechnicalParameter(IND.rsi, timeperiod=10)
rsi10_s2 = TechnicalParameter(IND.rsi, timeperiod=10, shifting=2)
rsi21 = TechnicalParameter(IND.rsi, timeperiod=21)
ema4 = TechnicalParameter(IND.ema, timeperiod=4)
ema2 = TechnicalParameter(IND.ema, timeperiod=2)
ema80 = TechnicalParameter(IND.ema, timeperiod=80)
ema100 = TechnicalParameter(IND.ema, timeperiod=100)
ma1 = TechnicalParameter(IND.ma, timeperiod=1)
ema15 = TechnicalParameter(IND.ema, timeperiod=15)
const25 = TechnicalParameter(NV.numeric_value, value=25)
const5 = TechnicalParameter(NV.numeric_value, value=5)
adx4 = TechnicalParameter(IND.adx, timeperiod=4)

all_parameters = [rsi10, rsi10_s2, rsi21, ema4, ema15, const25, const5]

def test_calculate_technical_indicator(sample_data):
    data = copy(sample_data)
    rsi10_v = calculate_technical_indicator(data, rsi10)
    rsi10_s2_v = calculate_technical_indicator(data, rsi10_s2)

    rsi21_v = calculate_technical_indicator(data, rsi21)
    ema4_v = calculate_technical_indicator(data, ema4)
    ema15_v =calculate_technical_indicator(data, ema15)


    extended_table = evaluate_technical_parameters(sample_data, [rsi10])

    extended_table = evaluate_technical_parameters(sample_data, [rsi21])
    print extended_table


def run_flow(sample_data, trade_system, parameters):
    table = copy(sample_data)
    # extend
    extended = evaluate_technical_parameters(table, parameters)
    # filter
    filtered = filter_stock_data(trade_system, 'sample', copy(extended))
    return filtered, extended,

def run_full_flow(dir, trade_system, parameters):
    all_stocks = get_all_stocks(dir)
    fil, ext = run_flow(sample_data, trade_system, parameters)
    stocks = get_all_stocks(dir)
    indicators = get_indicators(trade_system)
    extended = dict((symbol, evaluate_technical_parameters(stock, indicators)) for symbol, stock in stocks.items())
    filtered = dict((symbol, filter_stock_data(trade_system, symbol, stock)) for symbol, stock in extended.items())
    start, end, period = get_system_times(all_stocks)
    stats_dict = get_stat_dict(stocks, filtered)
    stats = calculate_system_statistics(stats_dict, trade_system, start, end, period)
    set_trace()


def trade_definer_1():
    # technical parameters in use
    used_parameters = [rsi21, ma1]
    # system definer
    open_term = Term(rsi21, RELATIONS.greater, const5)
    close_term = Term(ma1, RELATIONS.less, const25)
    open_clause = Clause(open_term)
    close_clause = Clause(close_term)
    open_rule = Rule(open_clause)
    close_rule = Rule(close_clause)
    trade_system = TradeSystem('tester', open_rule, close_rule, TRADE_DIRECTIONS.long)
    return trade_system, used_parameters


def trade_definer_2():
    # technical parameters in use
    used_parameters = [rsi21, adx4, rsi10]
    # system definer
    open_term = Term(ma1, RELATIONS.crossover_above, rsi10)
    close_term = Term(adx4, RELATIONS.crossover_below, rsi10)
    open_clause = Clause(open_term)
    close_clause = Clause(close_term)
    open_rule = Rule(open_clause)
    close_rule = Rule(close_clause)
    trade_system = TradeSystem('tester', open_rule, close_rule, TRADE_DIRECTIONS.long)

    return trade_system, used_parameters

def trade_definer_3():
    # technical parameters in use
    used_parameters = [ema100, ema80, ema2]
    # system definer
    open_term = Term(ema100, RELATIONS.crossover_below, ema2)
    close_term = Term(ema100, RELATIONS.crossover_below, ema80)
    open_clause = Clause(open_term)
    close_clause = Clause(close_term)
    open_rule = Rule(open_clause)
    close_rule = Rule(close_clause)
    trade_system = TradeSystem('tester', open_rule, close_rule, TRADE_DIRECTIONS.long)

    return trade_system, used_parameters


def manual_tester():
    sys, params = trade_definer_1()
    fil, ext = run_flow(sample_data, sys, params)

def run_main():
    main(trade_definer_1())





if __name__ == "__main__":
    #test_calculate_technical_indicator(sample_data)
    #manual_tester()
    run_full_flow('./data/few_symbols/', trade_definer_3()[0], trade_definer_3()[1])
    #run_main()







