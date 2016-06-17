from utils import enums
from utils.general_utils import type_checking

class Term:
    """
    This class define term - the smallest building block of trade-system.
    """

    def __init(self, technical_parameter_1, relation, technical_parameter_2):

        # type checking
        type_checking(TechnicalParameter, technical_parameter_1)
        type_checking([TechnicalParameter, int, float], technical_parameter_2)
        type_checking(enums.RELATIONS, relation)

        # assignments
        self.technical_parameter_1 = technical_parameter_1
        self.relation = relation
        self.technical_parameter_2 = technical_parameter_2

    def get_technical_parameter_1(self):
        return self.technical_parameter_1

    def get_technical_parameter_2(self):
        return self.technical_parameter_2

    def get_relation(self):
        return self.relation



class TechnicalParameter:
    """
    Class of that represented technical parameter instance
    """
    def __init__(self, name, period=0, shifting=0, **kwargs):
        """

        :param name:
        :param period:
        :param shifting:
        :param kwargs:
        """
        if name not in enums.TECHNICAL_PARAMETER:
            raise AttributeError
        self.name = name
        if name in enums.RAW_PARAMETERS:
            self.is_basic = True
        else:
            self.is_basic = False
        self.period = period
        self.shifting = shifting

        for key, value in kwargs.iteritems():
            setattr(self, key, value)


    def get_name(self):
        return self.name
