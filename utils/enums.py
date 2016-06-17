"""
This class contains Enum class definition and enums classes to be use within the different modules
"""

class Enum(set):
    """
    Enum class.
    init: enum_instance = Enum(['NAME1', NAME2'])
    get: enum_instance.NAME1
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

# not working
class Enum2():
    def __init__(self, *args, **kwargs):
        for arg in args:
            setattr(self, arg, arg)
        for key, value in kwargs.iteritems():
            setattr(self, key, value)

    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError

    def __setattr__(self, name, value):
        if name in self:
            raise RuntimeError("Cannot override values")

    def __delattr__(self, name):
        raise RuntimeError("Cannot delete values")

    def __add__(self, other):
        return self.union(other)


def venum(**venums):
    """
    values enums- each item has name and values
    :param venums: kwargs style - (NAME1=value1, NAME2=value2, ...)
    """
    return type('VEnum', (), venums)



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
SUPPORTED_INDICATORS = Enum(['SMA', 'EMA', 'RSI', 'AR', 'ARO', 'ATR'])


RAW_PARAMETERS = Enum(['OPEN_PRICE', 'HIGH_PRICE', 'LOW_PRICE', 'CLOSE_PRICE', 'VOLUME', 'ADJ_CLOSE_PRICE'])
_STOCK_DATA_ADDED_COLUMNS = Enum(['OPEN_TRIGGER', 'CLOSE_TRIGGER'])
STOCK_DATA_COLUMNS = Enum('DATE') + RAW_PARAMETERS + _STOCK_DATA_ADDED_COLUMNS + SUPPORTED_INDICATORS
TECHNICAL_PARAMETER = RAW_PARAMETERS + SUPPORTED_INDICATORS


"""
The next Enum class contains all the order relations between indicators.
"""
RELATIONS = Enum(['GREATER', 'LESS', 'CROSSOVER', 'CROSSOVER_BELOW', 'CROSSOVER_ABOVE'])


