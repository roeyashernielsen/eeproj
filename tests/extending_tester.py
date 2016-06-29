from utils import general_utils as gu
from trade_system.technical_parameter import TechnicalParameter
from utils.enums import SUPPORTED_INDICATORS as IND, NUMERIC_VALUE as NV
from logbook import Logger, StreamHandler
from trade_system.rule import Rule, Clause
from utils.enums import RELATIONS, TRADE_DIRECTIONS
from trade_system.trade_system import TradeSystem
from processor.calculate_technical_parameters import calculate_technical_indicator, talib_adapter, evaluate_technical_parameters
from trade_system.term import Term
import sys
from processor.filtering import filter_stock_data
from pandas import DataFrame
from ipdb import set_trace
from copy import copy

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
ema15 = TechnicalParameter(IND.ema, timeperiod=15)
const25 = TechnicalParameter(NV.numeric_value, value=25)
const55 = TechnicalParameter(NV.numeric_value, value=55)

all_parameters = [rsi10, rsi10_s2, rsi21, ema4, ema15, const25, const55]

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

def test_flow(sample_data):
    #technical parameters

    parameters = [rsi21, ema15, const55, const25]

    # system definer
    open_term = Term(rsi21, RELATIONS.greater, const55)
    close_term = Term(ema15, RELATIONS.less, const25)
    open_clause = Clause(open_term)
    close_clause = Clause(close_term)
    open_rule = Rule(open_clause)
    close_rule = Rule(close_clause)
    trade_system = TradeSystem('tester', open_rule, close_rule, TRADE_DIRECTIONS.long)

    # start flow
    table = copy(sample_data)
    # extend
    ext_table = evaluate_technical_parameters(table, parameters)

    filtered = filter_stock_data(trade_system, copy(ext_table))
    set_trace()



if __name__ == "__main__":
    #test_calculate_technical_indicator(sample_data)
    test_flow(sample_data)






