from django.shortcuts import render
from trade_system.rule import *
from trade_system.term import *
from trade_system.trade_system import *
from utils import enums
import pandas as pd
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from django.http import HttpResponse
import re



def index(request):
	i = 0
	if request.GET.get('get.data'):
		i = (3 * int(request.GET.get('mytextbox')))
	if request.GET.get('del.data'):
		i = (2 * int(request.GET.get('mytextbox')))

	return render(request, 'Markit/index.html', {
		'name': i,
	})


def results(request):
	fig = Figure()
	ax = fig.add_subplot(111)
	data_df = pd.read_csv("/Users/roeya/Desktop/stock/BDE.csv")
	data_df = pd.DataFrame(data_df)
	data_df.plot(ax=ax)
	canvas = FigureCanvas(fig)
	response = HttpResponse(content_type='image/png')
	canvas.print_png(response)
	return response


def form(request):
	if request.GET.get('send.form'):
		name = str(request.GET.get('element_1_1'))
		direction = str(request.GET.get('element_1_2'))
		market = str(request.GET.get('element_2_1'))

		ts_dic = dict(zip(request.GET.keys(), request.GET.values()))
		open_dict = separate_dict_to_clauses(dict((k, v) for k, v in ts_dic.items() if k.startswith('o')))
		close_dict = separate_dict_to_clauses(dict((k, v) for k, v in ts_dic.items() if k.startswith('c')))
		open_rule = build_rule(open_dict)
		close_rule = build_rule(close_dict)
		trade_system = TradeSystem(open_rule, close_rule, direction)

		print(name + direction + market)
		print(request.GET)
	# open_rule = Rule(Clause(get_mock_term()))
	# 	close_rule = Rule(Clause(get_mock_term()))
	# 	return TradeSystem(open_rule, close_rule, enums.TRADE_DIRECTIONS.long)
	#
	# def get_mock_term():
	# 	tp1 = get_mock_technical_parameter()
	# 	tp2 = get_mock_technical_parameter()
	# 	rel = random.choice(list(enums.RELATIONS.values()))
	# 	return Term(tp1, rel, tp2)
	#
	# def get_mock_technical_parameter():
	# 	indicator = random.choice(list(enums.SUPPORTED_INDICATORS.values()))
	# 	period = random.randint(10, 50)
	# 	return TechnicalParameter(indicator, period, 0)

	return render(request, 'Markit/form.html', {
		'indicators': list(enums.SUPPORTED_INDICATORS.values()),
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
	tp1 = TechnicalParameter(dic.get(sdic[0]), int(dic.get(sdic[1])))
	tp2 = TechnicalParameter(dic.get(sdic[3]), int(dic.get(sdic[4])))

	return Term(tp1, dic.get(sdic[7]), tp2)


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
