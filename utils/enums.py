import copy
import talib

"""
This class contains Enum class definition and enums classes to be use within the different modules
"""

class EnumSet(set):
    """
    Enum class based on set.
    init: enum_name = EnumSet(['NAME1', NAME2'])
    get: enum_name.NAME1
    """
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError

    def __setattr__(self, name, value):
        raise RuntimeError("Cannot override values")

    def __delattr__(self, name):
        raise RuntimeError("Cannot delete values")

    def __add__(self, other):
        return self.union(other)


class EnumDict(dict):
    """
    Enum class, based on dictionary
    init: like dictionary- enum_name = EnumDict(key1=value1, key2=value2,...) or
                           enum_name = EnumDict({'key1':value1, 'key2':value2})
    get: enum_name.key1 --> value1
    """
    def __getattr__(self, name):
        if name in self.keys():
            return self.get(name)
        raise AttributeError

    def __setattr__(self, name, value):
        if name in self:
            raise RuntimeError("Cannot override values")

    def __delattr__(self, name):
        raise RuntimeError("Cannot delete values")

    def __add__(self, other):
        if set(self.keys()).intersection(set(other.keys())):
            raise KeyError("The enums shared duplicated keys. Cannot perform addition")
        new_enum = copy.copy(self)
        new_enum.update(other)
        return new_enum

    def __contains__(self, value):
        return value in self.values()




# ###################
# ## Enum classes ###
# ###################

MARKETS = EnumDict(nyse='NYSE', nasdaq='NASDAQ')
# Enum class of the supported indicators at the moment
SUPPORTED_INDICATORS = EnumDict(adx='ADX', aroonosc='AROONOSC', atr='ATR', ema='EMA', ma='MA', rsi='RSI', sar='SAR',
                                sma='SMA', wma='WMA')

# The parameters that received from the puller
RAW_PARAMETERS = EnumDict(open='Open', high='High', low='Low', close='Close', volume='Volume', adj_close='Adj Close')
# parameters that are added to the raw stock data table
_STOCK_DATA_ADDED_COLUMNS = EnumDict(open_trigger='OPEN_TRIGGER', close_trigger='CLOSE_TRIGGER')
STOCK_DATA_COLUMNS = EnumDict(date='Date') + RAW_PARAMETERS + _STOCK_DATA_ADDED_COLUMNS + SUPPORTED_INDICATORS
TECHNICAL_PARAMETER = RAW_PARAMETERS + SUPPORTED_INDICATORS
NUMERIC_VALUE = EnumDict(numeric_value='NUMERIC_VALUE')  # for technical param that is pure value (float)

TRADE_DIRECTIONS = EnumDict(long='LONG', short='SHORT')

"""
The next Enum class contains all the order relations between indicators.
"""
RELATIONS = EnumDict(greater='GREATER', less='LESS', crossover='CROSSOVER', crossover_below='CROSSOVER_BELOW',
                     crossover_above='CROSSOVER_ABOVE')


# TA-Lib technical indicators by groups
INDICATORS_GROUPS = EnumDict(zip([k.lower().replace(' ', '_') for k in talib.get_function_groups().keys()],
                                 [k for k in talib.get_function_groups().keys()]))
CYCLE_INDICATORS = EnumDict(zip([ind.lower() for ind in talib.get_function_groups().get(INDICATORS_GROUPS.cycle_indicators)],
                                [ind for ind in talib.get_function_groups().get(INDICATORS_GROUPS.cycle_indicators)]))
MOMENTUM_INDICATORS = EnumDict(zip([ind.lower() for ind in talib.get_function_groups().get(INDICATORS_GROUPS.momentum_indicators)],
                                [ind for ind in talib.get_function_groups().get(INDICATORS_GROUPS.momentum_indicators)]))
OVERLAP_STUDIES_INDICATORS = EnumDict(zip([ind.lower() for ind in talib.get_function_groups().get(INDICATORS_GROUPS.overlap_studies)],
                                [ind for ind in talib.get_function_groups().get(INDICATORS_GROUPS.overlap_studies)]))
VOLATILITY_INDICATORS = EnumDict(zip([ind.lower() for ind in talib.get_function_groups().get(INDICATORS_GROUPS.volatility_indicators)],
                                [ind for ind in talib.get_function_groups().get(INDICATORS_GROUPS.volatility_indicators)]))
VOLUME_INDICATORS = EnumDict(zip([ind.lower() for ind in talib.get_function_groups().get(INDICATORS_GROUPS.volume_indicators)],
                                [ind for ind in talib.get_function_groups().get(INDICATORS_GROUPS.volume_indicators)]))

# PRICE_TRANSFORM = EnumDict(zip([ind.lower() for ind in talib.get_function_groups().get(INDICATORS_GROUPS.price_transform)],
 #                               [ind for ind in talib.get_function_groups().get(INDICATORS_GROUPS.price_transform)]))


"""
The next Enum class contains the names of all the supported technical indicators, derived from the TA-Lib's indicators
"""
ALL_INDICATORS = CYCLE_INDICATORS + MOMENTUM_INDICATORS + OVERLAP_STUDIES_INDICATORS + VOLATILITY_INDICATORS + VOLUME_INDICATORS

# remove all the indicators with more than 1 vector output - the architecture not supported at the moment # TODO add support
indicators_to_remove = [ind for ind in ALL_INDICATORS if len(talib.abstract.Function(ind).output_names) > 1]
[ALL_INDICATORS.pop(ind) for ind in indicators_to_remove]
