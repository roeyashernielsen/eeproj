from django.shortcuts import render, render_to_response

def index(request):
    i = 0
    if(request.GET.get('get.data')):
        i = (int(request.GET.get('mytextbox')))
    if (request.GET.get('del.data')):
        i = (2 * int(request.GET.get('mytextbox')))

    return render(request, 'Markit/index.html', {
        'name': i,
    })