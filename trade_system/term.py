from utils.enum import Enum
from utils.general_general import type_checking
"""
This Enum class contains the names of all the supported technical indicators
SMA- simple moving average
EMA- exponential moving average
RSI- relative strength index
AR- Aroon indicator
ARO- Aroon oscillator
ATR- average true range
"""
Indicators = Enum(['SMA', 'EMA', 'RSI', 'AR', 'ARO', 'ATR'])


"""
This Enum class contains all the order relations between indicators.
"""
Relations = Enum(['GREATER', 'LESS', 'CROSSOVER', 'CROSSOVER_BELOW', 'CROSSOVER_ABOVE'])


class Term:
    """
    This class define term - the smallest building block of trade-system.
    """

    def __init(self, indicator_1, relation, indicator_2):

        # type checking
        type_checking(Indicators, indicator_1)
        type_checking([Indicators, int, float], indicator_2)
        type_checking(Relations, relation)

        # assignments
        self.indicator_1 = indicator_1
        self.relation = relation
        self.indicator_2 = indicator_2

