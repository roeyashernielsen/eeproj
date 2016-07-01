from utils.enums import TRADE_DIRECTIONS
from ipdb import set_trace


class Trade:
    """
    This class represents trade after its closure. It contains info of the opening day and the closing day.
    """
    def __init__(self, opening_day, closing_day, direction):
        """
        :param opening_day: tuple of: (pandas Series object contains the raw stock data parameters, the index of this
        Series in the previous DataFrame
        :param closing_day: tuple of: (pandas Series object contains the raw stock data parameters, the index of this
        Series in the previous DataFrame
        :param direction: long/short
        """
        self.opening_day = opening_day[0]
        self.closing_day = closing_day[0]

        # at default, the opening and the closing price determine by the open price of the day
        self.open_price = opening_day[0].Open  # TODO fix- no hard coded
        self.close_price = closing_day[0].Open
        self.profit_points = self.close_price - self.open_price  # in points ($)
        self.profit_percentages = (self.profit_points / self.open_price) * 100.0  # in percentages
        if direction is TRADE_DIRECTIONS.short:
            self.profit_points = -self.profit_points
            self.profit_percentages = -self.profit_percentages
        self.duration = closing_day[1] - opening_day[1]  # trade length in days

    def get_opening_day(self):
        return self.opening_day

    def get_closing_day(self):
        return self.closing_day

    def get_open_price(self):
        return self.open_price

    def get_close_price(self):
        return self.close_price

    def get_profit_points(self):
        return self.profit_points

    def get_profit_percentage(self):
        return self.profit_percentages

    def get_duration(self):
        return self.duration
