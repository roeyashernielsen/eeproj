from utils import enums
from utils.general_utils import type_checking
from .technical_parameter import TechnicalParameter


class Term:
    """
    This class define term - the smallest building block of trade-system.
    """

    def __init__(self, technical_parameter_1, relation, technical_parameter_2):

        # type checking
        # type_checking(TechnicalParameter, technical_parameter_1)
        # type_checking(TechnicalParameter, technical_parameter_2)
        # type_checking(enums.RELATIONS, relation)

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

    def set_index(self, index):
        self.index = index

    def get_index(self):
        return self.index


