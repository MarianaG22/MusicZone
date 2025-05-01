from django.shortcuts import render
from .models import Instrument, Type, Mark
from django.core.paginator import Paginator

def catalog(request):
    instrument_list = Instrument.objects.all()
    types = Type.objects.all()
    marks = Mark.objects.all()

    # Configurar paginación (mostrar 12 instrumentos por página)
    paginator = Paginator(instrument_list, 12)  
    page_number = request.GET.get('page')
    instruments = paginator.get_page(page_number)

    return render(request, 'catalog/catalog.html', {
        'instrument_list': instruments,
        'types': types,
        'marks': marks
    })