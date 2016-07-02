from django.shortcuts import render, render_to_response
from trade_system.rule import *
from trade_system.term import *
from trade_system.trade_system import *
from management.main import *
from management.ploter import *
from utils import enums
import pandas as pd
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from django.http import HttpResponse, HttpResponseRedirect
import re
s = ""
f = ""
stocks_stat_df = ""


def index(request):
	i = 0
	if request.GET.get('get.data'):
		i = (3 * int(request.GET.get('mytextbox')))
	if request.GET.get('del.data'):
		i = (2 * int(request.GET.get('mytextbox')))

	return render(request, 'Markit/index.html', {
		'name': i,
	})


def graph(request):
	# from pylab import *
	import matplotlib.pyplot as plt
	from datetime import datetime
	import time
	from matplotlib.dates import DateFormatter, WeekdayLocator, HourLocator, \
		DayLocator, MONDAY
	from matplotlib.finance import _candlestick
	import pandas as pd

	global s,f,stocks_stat_df
	if request.GET.get('show.graph'):
		mondays = WeekdayLocator(MONDAY)  # major ticks on the mondays
		alldays = DayLocator()  # minor ticks on the days
		yearFormatter = DateFormatter('%Y-%m')  # e.g., Jan 12
		funcy = lambda x: date2num(datetime.strptime(x, "%Y-%m-%d"))

		df = s.get(str(request.GET.get('stock_name')))
		df = df[['Date', 'Open', 'Close', 'High', 'Low']]
		df.columns = ['date', 'open', 'close', 'high', 'low']
		df[['date']] = df['date'].map(funcy)

		df2 = f.get(str(request.GET.get('stock_name')))
		print(df2)
		df2 = df2[['Date', 'Open', 'Close', 'High', 'Low']].head(2 * (len(df2) / 2))
		print(df2)
		df2.columns = ['date', 'open', 'close', 'high', 'low']
		df2[['date']] = df2['date'].map(funcy)

		fig, ax1 = plt.subplots()
		fig.set_size_inches(18.5, 10.5)
		fig.subplots_adjust(bottom=0.2)
		ax1.xaxis.set_major_locator(mondays)
		ax1.xaxis.set_minor_locator(alldays)
		ax1.xaxis.set_major_formatter(yearFormatter)
		_candlestick(ax1, [tuple(x) for x in df.values], width=0.6)
		ax1.xaxis_date()
		ax1.autoscale_view()
		plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')

		# ax[1].xaxis.set_major_locator(mondays)
		# ax[1].xaxis.set_minor_locator(alldays)
		ax2 = ax1.twinx()
		# ax2.xaxis.set_major_formatter(yearFormatter)
		_candlestick(ax2, [tuple(x) for x in df2.values], width=0.6, colorup='g', colordown='b')
		# ax[1].xaxis_date()
		# ax[1].autoscale_view()
		# plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')

		canvas = FigureCanvas(fig)
		response = HttpResponse(content_type='image/png')
		canvas.print_png(response)
		return response

	if request.GET.get('show.table'):
		df1 = stocks_stat_df.get(str(request.GET.get('stock_name')))[0]
		df2 = stocks_stat_df.get(str(request.GET.get('stock_name')))[1]
		df3 = stocks_stat_df.get(str(request.GET.get('stock_name')))[2]
		return render(request, 'Markit/table.html', {
			'name': str(request.GET.get('stock_name')),
			'data1': df1.to_html,
			'data2': df2.to_html,
			'data3': df3.to_html,
		})


def form(request):
	global s,f,stocks_stat_df
	if request.GET.get('send.form'):
		name = str(request.GET.get('element_1_1'))
		direction = enums.get_enum_value(enums.TRADE_DIRECTIONS, str(request.GET.get('element_1_2')))
		market = enums.get_enum_value(enums.MARKETS, str(request.GET.get('element_2_1')))

		ts_dic = dict(zip(request.GET.keys(), request.GET.values()))
		open_dict = separate_dict_to_clauses(dict((k, v) for k, v in ts_dic.items() if k.startswith('o')))
		close_dict = separate_dict_to_clauses(dict((k, v) for k, v in ts_dic.items() if k.startswith('c')))
		open_rule = build_rule(open_dict)
		close_rule = build_rule(close_dict)
		trade_system = TradeSystem(name, open_rule, close_rule, direction)
		s, f, stock_list, stocks_stat_df, sts_stat_df = main(trade_system)
		return render(request, 'Markit/results.html', {
			'df': sts_stat_df.to_html,
			'stock_list': stock_list
		})

	return render(request, 'Markit/form.html', {
		'indicators': list(enums.TECHNICAL_PARAMETER.values() + enums.NUMERIC_VALUE.values()),
		'directions': list(enums.TRADE_DIRECTIONS.values()),
		'markets': list(enums.MARKETS.values()),
		'relations': list(enums.RELATIONS.values())
	})


def separate_dict_to_clauses(dic):
	res = []
	for i in range(int(len(dic)/8)):
		j = i+1
		regexp = re.compile(r'element_[347]_[0-9]_' + str(j) + '_[0-9]')
		res.append(dict((k, v) for k, v in dic.items() if regexp.search(k) is not None))

	return res


def separate_dict_to_terms(dic):
	res = []
	for i in range(int(len(dic)/8)):
		j = i + 1
		regexp = re.compile(r'element_[347]_[0-9]_[0-9]_' + str(j))
		res.append(dict((k, v) for k, v in dic.items() if regexp.search(k) is not None))

	return res


def build_term(dic):
	sdic = sorted(dic)
	if dic.get(sdic[2]) == "":
		tp1 = TechnicalParameter(name=enums.get_enum_value(enums.TECHNICAL_PARAMETER, dic.get(sdic[0])), timeperiod=int(dic.get(sdic[1])))
	else:
		tp1 = TechnicalParameter(name=enums.get_enum_value(enums.TECHNICAL_PARAMETER, dic.get(sdic[0])), timeperiod=int(dic.get(sdic[1])), shifting=int(dic.get(sdic[2])))

	if dic.get(sdic[3]) not in enums.NUMERIC_VALUE:
		if dic.get(sdic[5]) == "":
			tp2 = TechnicalParameter(name=enums.get_enum_value(enums.TECHNICAL_PARAMETER, dic.get(sdic[3])), timeperiod=int(dic.get(sdic[4])))
		else:
			tp2 = TechnicalParameter(name=enums.get_enum_value(enums.TECHNICAL_PARAMETER, dic.get(sdic[3])), timeperiod=int(dic.get(sdic[4])), shifting=int(dic.get(sdic[5])))
	else:
		tp2 = TechnicalParameter(name=enums.get_enum_value(enums.NUMERIC_VALUE, dic.get(sdic[3])), value=int(dic.get(sdic[6])))

	return Term(tp1, enums.get_enum_value(enums.RELATIONS, dic.get(sdic[7])), tp2)


def return_valid_terms(terms):
	res = []
	for term in terms:
		if term.get('name') is not None:
			if term.get('period') is None:
				res.append(term)
	return res

def build_rule(dic):
	clauses = []
	for clause in dic:
		terms_dict = separate_dict_to_terms(clause)
		terms = []
		for term in terms_dict:
			terms.append(build_term(term))
		clauses.append(Clause(*terms))

	return Rule(*clauses)
