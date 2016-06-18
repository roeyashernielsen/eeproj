from utils import enums
from utils.general_utils import type_checking

class Term:
    """
    This class define term - the smallest building block of trade-system.
    """

    def __init(self, technical_parameter_1, relation, technical_parameter_2):

        # type checking
        type_checking(TechnicalParameter, technical_parameter_1)
        type_checking(TechnicalParameter, technical_parameter_2)
        type_checking(enums.RELATIONS, relation)

        # assignments
        self.technical_parameter_1 = technical_parameter_1
        self.relation = relation
        self.technical_parameter_2 = technical_parameter_2
        if type(technical_parameter_2) in [int, float]:
            self.numeric_value = True
        else:
            self.numeric_value = False

    def get_technical_parameter_1(self):
        return self.technical_parameter_1

    def get_technical_parameter_2(self):
        return self.technical_parameter_2

    def get_relation(self):
        return self.relation

    def is_numeric_value(self):
        return self.numeric_value



class TechnicalParameter:
    """
    Class of that represented technical parameter instance. It could be raw stock data (e.g. open price, close...), or
    technical indicators or oscillators. The second type is pure numeric value- floating point number.
    """
    def __init__(self, name, period=0, shifting=0, value=None, **kwargs):
        """
        :param name: name of the parameter, should be one of the TECHNICAL_PARAMETERS or NUMERIC_VALUE.
        :param period: time period (in days) that the calculation relays on. Default is 0 (based on current time/raw data).
        :param shifting: the relevant day for the analysis. Default is 0 (current day)
        :param value: for numeric values input (constant number). Has meaning only when name==NUMERIC_VALUE. Default is None.
        :param kwargs: other args, that relevant for specific technical indicators.
        """
        if name not in enums.TECHNICAL_PARAMETER + enums.NUMERIC_VALUE:
            raise AttributeError
        self.name = name
        if name == enums.NUMERIC_VALUE.numeric_value:
            self.is_numeric_value = True
            self.value = float(value)
        else:
            if name in enums.RAW_PARAMETERS:
                self.is_raw = True
            else:
                self.is_raw = False
            self.period = period
            self.shifting = shifting
            self.is_numeric_value = False

        for key, value in kwargs.iteritems():
            setattr(self, key, value)

    def get_name(self):
        return self.name

    def get_period(self):
        return self.period

    def get_shifting(self):
        return self.shifting

    def is_raw(self):
        return self.is_raw

    def is_numeric_value(self):
        return self.is_numeric_value
