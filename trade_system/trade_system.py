from utils.general_utils import *
import rule
"""
This Module defines trade-system.
"""


class TradeSystem:
    def __init__(self, open_rule, close_rule):
        # type checking
        type_checking(rule.Rule, open_rule, close_rule)
        self.open_rule = open_rule
        self.close_rule = close_rule

    def get_open_rule(self):
        return self.open_rule

    def get_close_rule(self):
        return self.close_rule


