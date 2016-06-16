from utils.general_general import *
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



