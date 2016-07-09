import os

from trade_system.rule import *
from trade_system.term import *
from processor.calculate_technical_parameters import *
from processor.filtering import *
from statistics.system_statistics import *
from utils import enums
from statistics.system_statistics import *
from collections import OrderedDict
from visualization.stats_tables import *
from utils import general_utils

import ipdb;

start_date = None
end_date = None
trading_days = 0

def main(trade_system):
    """
    :param trade_system: TradeSystem instance as defined by the user input
    :return:
    """
    path = "./data/appy/"
    all_stocks = general_utils.get_all_stocks(path)
    indicators = general_utils.get_indicators(trade_system)

    global start_date, end_date, trading_days
    start_date, end_date, trading_days = general_utils.get_system_times(all_stocks)

    # processing stages
    # extend stock tables with the required technical parameters
    extended = dict((symbol, evaluate_technical_parameters(stock, indicators)) for symbol, stock in all_stocks.items())
    # filter stock tables to reveal the trades
    filtered = dict((symbol, filter_stock_data(trade_system, symbol, stock)) for symbol, stock in extended.items())

    # statistics stage
    stats_dict = general_utils.get_stat_dict(all_stocks, filtered)
    stats = calculate_system_statistics(stats_dict, trade_system, start_date, end_date, trading_days)

    # data to show by UI
    active_stocks = [s.name for s in stats[1]]
    stocks_stats_df = dict((s.name, (list_to_dataframe(general_details, [s]), list_to_dataframe(performances, [s]), list_to_dataframe(averages_and_bounds, [s]))) for s in stats[1])
    return all_stocks, filtered, active_stocks, stocks_stats_df, list_to_dataframe(full_statistics, [stats[0]] + stats[1])








# TODO move to a better place

def get_mock_trade_system():
    # tp1 = TechnicalParameter(enums.SUPPORTED_INDICATORS.ema, 10, 0)
    # tp2 = TechnicalParameter(enums.SUPPORTED_INDICATORS.ema, 30, 0)
    # term1 = Term(get_mock_technical_parameter(), enums.RELATIONS.crossover_below, get_mock_technical_parameter())
    # term2 = Term(get_mock_technical_parameter(), enums.RELATIONS.crossover_above, get_mock_technical_parameter())
    open_rule = Rule(Clause(get_mock_term()))
    close_rule = Rule(Clause(get_mock_term()))
    return TradeSystem("test", open_rule, close_rule, enums.TRADE_DIRECTIONS.long)


def get_mock_term():
    tp1 = get_mock_technical_parameter()
    tp2 = get_mock_technical_parameter()
    rel = random.choice(list(enums.RELATIONS.values()))
    return Term(tp1, rel, tp2)


def get_mock_technical_parameter():
    indicator = random.choice(list(enums.SUPPORTED_INDICATORS.values()))
    period = random.randint(10, 50)
    return TechnicalParameter(indicator, period, 0)


if __name__ == "__main__":
    sys.exit(main())
