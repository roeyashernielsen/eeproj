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

	# print(enums.SUPPORTED_INDICATORS.ema)
	# tp1 = TechnicalParameter()
	# open_rule = Rule()
	# close_rule = Rule()
	# sys = TradeSystem()

# def parse_indicators(trade_system):
# 	indicators = []
# 	for trem in trade_system.get_open_rule().get_clauses().get_terms():
# 		indicators.append(term.get_technical_parameter_1())
# 	close_rule = trade_system.get_close_rule()
#


if __name__ == "__main__":
	sys.exit(main())
