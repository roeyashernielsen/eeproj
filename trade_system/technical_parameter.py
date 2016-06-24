from utils import enums


class TechnicalParameter:
    """
    Class of that represented technical parameter instance. It could be raw stock data (e.g. open price, close...), or
    technical indicators or oscillators. The second type is pure numeric value- floating point number.
    """
    def __init__(self, name, timeperiod=None, shifting=0, value=None, **kwargs):
        """
        :param name: name of the parameter, should be one of the TECHNICAL_PARAMETERS or NUMERIC_VALUE.
        :param timeperiod: time period (in days) that the calculation relays on. Default is None.
        :param shifting: the relevant day for the analysis. Default is 0 (current day)
        :param value: for numeric values input (constant number). Has meaning only when name==NUMERIC_VALUE. Default is None.
        :param kwargs: other args, that relevant for specific technical indicators.
        """
        if name not in enums.TECHNICAL_PARAMETER + enums.NUMERIC_VALUE:
            raise AttributeError
        self.name = name
        self.value = float(value) if name in enums.NUMERIC_VALUE else value
        self.raw = True if name in enums.RAW_PARAMETERS else False
        self.timeperiod = timeperiod
        self.shifting = shifting

        for key, value in kwargs.items():
            setattr(self, key, value)

    def get_name(self):
        return self.name

    def get_timeperiod(self):
        return self.timeperiod

    def get_shifting(self):
        return self.shifting

    def is_raw(self):
        """it's raw if it's Open/High/Low/Close/Volume or adj close"""
        return self.raw

    def is_numeric_value(self):
        return bool(self.value)

    def get_numeric_value(self):
        if self.is_numeric_value():
            return self.value

    def is_technical_indicator(self):
        return not (self.is_raw() or self.is_numeric_value())
