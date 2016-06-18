from utils import enums


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
