from django.shortcuts import render
from .models import Instrument, Type, Mark
from django.core.paginator import Paginator

def catalog(request):

    # Capturar filtros del formulario
    type_param = request.GET.get('type')
    selected_type = int(type_param) if type_param and type_param.isdigit() else None

    mark_param = request.GET.get('mark')
    selected_mark = int(mark_param) if mark_param and mark_param.isdigit() else None

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    # Consultar la tabla Instrument
    instrument_list = Instrument.objects.all()

    # Aplicar filtros si existen
    if selected_type:
        instrument_list = instrument_list.filter(type__id=selected_type)

    if selected_mark:
        instrument_list = instrument_list.filter(mark__id=selected_mark)

    if min_price:
        instrument_list = instrument_list.filter(price__gte=min_price)

    if max_price:
        instrument_list = instrument_list.filter(price__lte=max_price)
    
    # Consultar tablas
    types = Type.objects.all()
    marks = Mark.objects.all()

    # Paginación (mostrar 12 instrumentos por página)
    paginator = Paginator(instrument_list, 12)
    page_number = request.GET.get('page')
    instruments = paginator.get_page(page_number)

    return render(request, 'catalog/catalog.html', {
        'instrument_list': instruments,
        'types': types,
        'marks': marks,
        'selected_type': selected_type,
        'selected_mark': selected_mark,
        'price_min': min_price,
        'price_max': max_price,
    })
