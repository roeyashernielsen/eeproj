import copy

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
        if name in self:
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


# ###################
# ## Enum classes ###
# ###################

"""
The next Enum class contains the names of all the supported technical indicators
SMA- simple moving average
EMA- exponential moving average
RSI- relative strength index
AR- Aroon indicator
ARO- Aroon oscillator
ATR- average true range
"""
SUPPORTED_INDICATORS = EnumDict(sma='SMA', ema='EMA', rsi='RSI', ar='AR', aro='ARO', atr='ATR')

# The parameters that received from the puller
RAW_PARAMETERS = EnumDict(open='Open', high='High', low='Low', close='Close', volume='Volume', adj_close='Adj Close')
# parameters that are added to the raw stock data table
_STOCK_DATA_ADDED_COLUMNS = EnumDict(open_trigger='OPEN_TRIGGER', close_trigger='CLOSE_TRIGGER')
STOCK_DATA_COLUMNS = EnumDict(date='Date') + RAW_PARAMETERS + _STOCK_DATA_ADDED_COLUMNS + SUPPORTED_INDICATORS
TECHNICAL_PARAMETER = RAW_PARAMETERS + SUPPORTED_INDICATORS
NUMERIC_VALUE = EnumDict(numeric_value='NUMERIC_VALUE')  # for technical param that is pure value (float)


"""
The next Enum class contains all the order relations between indicators.
"""
RELATIONS = EnumDict(greater='GREATER', less='LESS', crossover='CROSSOVER', crossover_below='CROSSOVER_BELOW',
                     crossover_above='CROSSOVER_ABOVE')


