from trade_system.technical_parameter import TechnicalParameter
from utils.enums import SUPPORTED_INDICATORS as IND, NUMERIC_VALUE as NV
from utils.enums import RELATIONS, TRADE_DIRECTIONS
import talib
from collections import OrderedDict


technical_indicator = talib.abstract.Function(technical_parameter.get_name())
technical_values = technical_indicator(arguments, timeperiod=technical_parameter.get_timeperiod()) # TODO this is workaround, fixing talib_adapter should fix it
columns = [sd.Open.values, sd.High.values, sd.Low.values, sd.Close.values, sd.Volume.values]
raw_data = OrderedDict(zip([title.lower() for title in sd.columns[1:-1]], columns))
talib_inputs.update(raw_data)


# Hard coded technical indicators
rsi10 = TechnicalParameter(IND.rsi, timeperiod=10)
rsi10_s2 = TechnicalParameter(IND.rsi, timeperiod=10, shifting=2)


def emas_trade_system():
    ema8 = TechnicalParameter(IND.ema, timeperiod=8)
    ema8_minus1 = TechnicalParameter(IND.ema, timeperiod=8, timeshifting=1)
    ema8_minus2 = TechnicalParameter(IND.ema, timeperiod=8, timeshifting=2)
    ema20= TechnicalParameter(IND.ema, timeperiod=20)
    used_paramteres = [ema8, ema20]
    term1 = Term(ema8, RELATIONS.greater, ema8_minus1)  # ema8 is uptrending (positive slope)
    term2 = Term(ema8_minus1, RELATIONS.greater, ema8_minus2)
    term3 = Term(ema8, RELATIONS.greater, ema20)  # ema20 > ema8
    term4 = Term(ema8, RELATIONS.less, ema20)
    open_rule = Rule(Clause(*[term3]))
    close_rule = Rule(Clause(*[term4]))
    trade_system = TradeSystem('EMAS', open_rule, close_rule, TRADE_DIRECTIONS.long)
    return trade_system



def evaluate_trades(stock):
    """
    :param stock: DataFrame contains stock's data
    :return:
    """
    price_values = [stock.Open.values, stock.High.values, stock.Low.values, stock.Close.values, stock.Volume.values]
    prices = OrderedDict(zip([title.lower() for title in stock.columns[1:-1]], columns))  # for talib standards

    # Technical indicators
    ema = talib.abstract.Function(IND.ema)
    ema8 = ema(prices, timeperiod=8)


