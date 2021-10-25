from django.shortcuts import render

# Create your views here.
from django.http import HttpResponseRedirect

from .forms import ConversionForm


def index(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ConversionForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            start_row = form.cleaned_data['start_row']
            # redirect to a new URL:
            return HttpResponseRedirect('result/')
        # if a GET (or any other method) we'll create a blank form
    else:
        form = ConversionForm
    return render(request, 'index.html', {'form': form})


def result(request):
    return render(request, 'result.html')