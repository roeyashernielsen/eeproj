from django.shortcuts import render, render_to_response
from .models import Stock


def index(request):
    i = 0
    if (request.GET.get('get.data')):
        s = Stock(file=open('/Users/roeya/Desktop/yahoo_stocks.csv', 'w+'))
        s.save()
    if (request.GET.get('del.data')):
        i = (2 * int(request.GET.get('mytextbox')))

    return render(request, 'Markit/index.html', {
        'name': i,
    })
