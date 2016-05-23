from django.shortcuts import render

def index(request):
    return render(request, 'Markit/index.html', {
        'name': 'Roey',
    })