import sys
import os
import pandas as pd
from trade_system.trade_system import *
from trade_system.rule import *
from trade_system.technical_parameter import *
from utils import enums


def main(argv=None):
	path = "/Users/roeya/Desktop/stock/"
	stocks = {}

	for file in os.listdir(path):
		if file.endswith(".csv"):
			stocks[file.rsplit('.', 1)[0]] = pd.read_csv(path + file)

	print(enums.SUPPORTED_INDICATORS.ema)


# tp1 = TechnicalParameter()
# open_rule = Rule()
# close_rule = Rule()
# sys = TradeSystem()

def parse_indicators(trade_system):
	indicators = []
	terms = trade_system.get_open_rule().get_clauses().get_terms() + trade_system.get_close_rule().get_clauses().get_terms()
	for term in terms:
		tp1 = term.get_technical_parameter_1
		tp2 = term.get_technical_parameter_1
		if(tp1.is_technical_indicator()):
			indicators.append(term.get_technical_parameter_1)
		if (tp2.is_technical_indicator()):
			indicators.append(term.get_technical_parameter_1)
	return indicators

def indicator_equality(indicator1, indicator2):
	if(indicator1.get_name == indicator2.get_name):
		if(indicator1.get_period == indicator2.get_period):
			return True
	return False

def


if __name__ == "__main__":
	sys.exit(main())
