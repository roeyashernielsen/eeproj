from utils.general_utils import *
from . import rule
from utils import enums
"""
This Module defines trade-system.
"""


class TradeSystem:
    """
    This class define the trade system rules, directions and stop loss
    """
    def __init__(self, name, open_rule, close_rule, direction, stop_loss=None, moving_stop_loss=None):
        """
        :param name: trade system name as given by the user
        :param open_rule: Rule class instance defines the trade opening criteria
        :param close_rule: Rule class instance defines the trade closure criteria
        :param direction: the type of the trade (long/short) as define in TRADE_DIRECTIONS
        :param stop_loss: percentages value stop loss, default is None
        :param moving_stop_loss: percentages value moving stop loss, default is None
        """
        # type checking
        type_checking(rule.Rule, open_rule, close_rule)
        if direction not in enums.TRADE_DIRECTIONS:
            raise AttributeError

        self.name = name
        self.open_rule = open_rule
        self.close_rule = close_rule
        self.direction = direction
        self.stop_loss = stop_loss
        self.moving_stop_loss = moving_stop_loss

    def get_name(self):
        return self.name

    def get_open_rule(self):
        return self.open_rule

    def get_close_rule(self):
        return self.close_rule

    def get_direction(self):
        return self.direction

    def get_stop_loss(self):
        return self.stop_loss

    def get_moving_stop_loss(self):
        return self.moving_stop_loss


