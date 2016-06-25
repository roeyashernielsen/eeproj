import os
import pandas as pd
from trade_system.rule import *
from trade_system.term import *
from processor.calculate_technical_parameters import *
from processor.filtering import *
from utils import enums
from puller.__init__ import *


def main(argv=None):
    path = DATA_PATH + 'few_symbols/'
    stocks = get_all_stocks(path)
    trade_system = get_mock_trade_system()
    indicators = get_indicators(trade_system)
    a = dict((name, evaluate_technical_parameters(stock, indicators)) for name, stock in stocks.items())
    b = dict((name, filter_stock_data(trade_system, stock)) for name, stock in stocks.items())
    print(a)
    print(b)
    import pdb;
    pdb.set_trace()


def get_mock_trade_system():
    # tp1 = TechnicalParameter(enums.SUPPORTED_INDICATORS.ema, 10, 0)
    # tp2 = TechnicalParameter(enums.SUPPORTED_INDICATORS.ema, 30, 0)
    # term1 = Term(get_mock_technical_parameter(), enums.RELATIONS.crossover_below, get_mock_technical_parameter())
    # term2 = Term(get_mock_technical_parameter(), enums.RELATIONS.crossover_above, get_mock_technical_parameter())
    open_rule = Rule(Clause(get_mock_term()))
    close_rule = Rule(Clause(get_mock_term()))
    return TradeSystem(open_rule, close_rule, enums.TRADE_DIRECTIONS.long)


def get_mock_term():
    tp1 = get_mock_technical_parameter()
    tp2 = get_mock_technical_parameter()
    rel = random.choice(list(enums.RELATIONS.values()))
    return Term(tp1, rel, tp2)


def get_mock_technical_parameter():
    indicator = random.choice(list(enums.SUPPORTED_INDICATORS.values()))
    period = random.randint(10, 50)
    return TechnicalParameter(indicator, period, 0)


def get_all_stocks(path):
    stocks = {}
    for file in os.listdir(path):
        if file.endswith(".csv"):
            stocks[file.rsplit('.', 1)[0]] = pd.read_csv(path + file)
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


if __name__ == "__main__":
    sys.exit(main())
