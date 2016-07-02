import os
import pandas as pd
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

start_date = None
end_date = None
trading_days = 0

def main(trade_system):
    """
    :param trade_system: TradeSystem instance as defined by the user input
    :return:
    """
    path = "./data/long_run/"
    all_stocks = get_all_stocks(path)
    indicators = get_indicators(trade_system)

    start_date, end_date, trade_days = general_utils.get_system_times(all_stocks)

    # processing stages
    # extend stock tables with the required technical parameters
    extended = dict((symbol, evaluate_technical_parameters(stock, indicators)) for symbol, stock in all_stocks.items())
    # filter stock tables to reveal the trades
    filtered = dict((symbol, filter_stock_data(trade_system, symbol,  stock)) for symbol, stock in extended.items())

    # statistics stage
    stats_dict = get_stat_dict(all_stocks, filtered)
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


# Depracated, use csv_to_dataframe in general_utils TODO delete after no one uses
def get_all_stocks(path):
    stocks = {}
    for csv_file in os.listdir(path):
        if csv_file.endswith(".csv"):
            stocks[csv_file.rsplit('.', 1)[0]] = pd.read_csv(path + csv_file)
    return stocks


def get_indicators(trade_system):
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
    return remove_duplicate_indicators(indicators)


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
        if len(filtered.get(k)):
            l = len(full.get(k))
            res[k] = (filtered.get(k), full.get(k).iloc[0, 0], full.get(k).iloc[l - 1, 0], l)
    return res


def list_to_dataframe(field_dict, obj_list):

    list_row = []
    for obj in obj_list:
        row = {}
        for field, col in field_dict.items():
            if hasattr(obj, field):
                row[col] = getattr(obj, field)
        list_row.append(row)

    return pd.DataFrame(list_row, columns=(field_dict.values()))

if __name__ == "__main__":
    sys.exit(main())
