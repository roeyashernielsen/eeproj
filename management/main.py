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


if __name__ == "__main__":
	sys.exit(main())
