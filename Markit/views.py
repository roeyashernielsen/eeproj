from django.shortcuts import render, render_to_response
from .models import Stock
from django import forms


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

def form(request):
    return render(request, 'Markit/form.html', {
    })


class MyForm(forms.Form):
    original_field = forms.CharField()
    extra_field_count = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        extra_fields = kwargs.pop('extra', 0)

        super(MyForm, self).__init__(*args, **kwargs)
        self.fields['extra_field_count'].initial = extra_fields

        for index in range(int(extra_fields)):
            # generate extra fields in the number specified via extra_fields
            self.fields['extra_field_{index}'.format(index=index)] = forms.CharField()


def myform(request):
    if request.method == 'POST':
        form = MyForm(request.POST, extra=request.POST.get('extra_field_count'))
        if form.is_valid:
            print("valid!")
    else:
        form = MyForm()
    return render(request, 'Markit/myform.html', { 'form': form })