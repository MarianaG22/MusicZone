from django.shortcuts import render, redirect, get_object_or_404
from .models import Instrument, Type, Mark
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

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

##############################CRUD PRODUCTOS###############################################
@staff_member_required(login_url='/')
@login_required
def instrumento(request):
    # Obtener todos los instrumentos
    instruments_list = Instrument.objects.all()
    types = Type.objects.all()
    marks = Mark.objects.all()

    # Configurar paginación
    paginator = Paginator(instruments_list, 10)  # 10 instrumentos por página
    page_number = request.GET.get('page')
    instruments = paginator.get_page(page_number)

    return render(request, 'CRUD Product/instrument.html', {
        'instruments': instruments,
        'types': types,
        'marks': marks,
    })

@staff_member_required(login_url='/')
@login_required
def crear_instrumento(request):
    types = Type.objects.all()
    marks = Mark.objects.all()
    
    if request.method == 'POST':
        instrument_name = request.POST.get('instrument', '').strip()
        type_id = request.POST.get('type')
        mark_id = request.POST.get('mark')
        price = request.POST.get('price', '0').strip()
        stock = request.POST.get('stock', '0').strip()
        image = request.FILES.get('image')

        # Validaciones
        if not instrument_name:
            messages.error(request, 'El nombre del instrumento es obligatorio.')
            return render(request, 'CRUD Product/create_instrument.html', {'types': types, 'marks': marks})
        
        if not type_id:
            messages.error(request, 'Debe seleccionar un tipo.')
            return render(request, 'CRUD Product/create_instrument.html', {'types': types, 'marks': marks})

        if not mark_id:
            messages.error(request, 'Debe seleccionar una marca.')
            return render(request, 'CRUD Product/create_instrument.html', {'types': types, 'marks': marks})

        # Obtiene instancias de Type y Mark
        type_instance = get_object_or_404(Type, pk=type_id)
        mark_instance = get_object_or_404(Mark, pk=mark_id)

        # Crear instrumento
        instrument = Instrument(
            instrument=instrument_name,
            type=type_instance,
            mark=mark_instance,
            price=price,
            stock=stock,
            image=image
        )
        instrument.save()

        messages.success(request, f'El instrumento "{instrument.instrument}" ha sido creado exitosamente.')
        return redirect('/')

    return render(request, 'CRUD Product/create_instrument.html', {'types': types, 'marks': marks})

@staff_member_required(login_url='/')
@login_required
def editar_instrumento(request, instrument_id):
    instrument = get_object_or_404(Instrument, id=instrument_id)
    types = Type.objects.all()
    marks = Mark.objects.all()

    if request.method == 'POST':
        # Actualizar campos del instrumento
        instrument.instrument = request.POST.get('instrument')
        instrument.price = request.POST.get('price')
        instrument.stock = request.POST.get('stock')

        # Actualizar tipo
        type_id = request.POST.get('type')
        if type_id:
            instrument.type = get_object_or_404(Type, id=type_id)

        # Actualizar marca
        mark_id = request.POST.get('mark')
        if mark_id:
            instrument.mark = get_object_or_404(Mark, id=mark_id)

        # Actualizar imagen (si se sube una nueva)
        if 'image' in request.FILES:
            instrument.image = request.FILES['image']

        # Guardar cambios
        instrument.save()
        messages.success(request, f'El instrumento "{instrument.instrument}" ha sido actualizado exitosamente.')
        return redirect('products:instrumento')

    context = {
        'instrument': instrument,
        'types': types,
        'marks': marks,
    }

    return render(request, 'CRUD Product/edit_instrument.html', context)

@staff_member_required(login_url='/')
@login_required
def eliminar_instrumento(request, instrument_id):
    instrument = get_object_or_404(Instrument, id=instrument_id)
    
    if request.method == 'POST':
        instrument.delete()
        messages.success(request, f'El instrumento "{instrument.instrument}" ha sido eliminado exitosamente.')
        return redirect('products:instrumento')

    return render(request, 'CRUD Product/delete_instrument.html', {'instrument': instrument})