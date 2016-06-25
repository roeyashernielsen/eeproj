from django.shortcuts import render
from utils import enums


def index(request):
	i = 0
	if request.GET.get('get.data'):
		i = (3 * int(request.GET.get('mytextbox')))
	if request.GET.get('del.data'):
		i = (2 * int(request.GET.get('mytextbox')))

	return render(request, 'Markit/index.html', {
		'name': i,
	})


def form(request):

	if request.GET.get('send.form'):
		bla = str(request.GET.get('element_1_1'))
		print(bla)

	return render(request, 'Markit/form.html', {
		'indicators': list(enums.SUPPORTED_INDICATORS.values()),
		'directions': list(enums.TRADE_DIRECTIONS.values()),
		'markets':     list(enums.TECHNICAL_PARAMETER.values())
	})
