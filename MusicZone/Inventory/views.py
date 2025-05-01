from django.shortcuts import render
from .models import Instrument, Type, Mark

def catalog(request):
    instrument_list = Instrument.objects.all()
    types = Type.objects.all()
    marks = Mark.objects.all()

    return render(request, 'catalog/catalog.html', {
        'instrument_list': instrument_list,
        'types': types,
        'marks': marks
    })