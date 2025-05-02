from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cart, Cart_Item
from Inventory.models import Instrument
from datetime import date

#@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user, defaults={'created_at': date.today()})
    items = cart.cart_item_set.all()
    # Agregar subtotales a cada ítem
    for item in items:
        item.subtotal = item.instrument.price * item.quantity

    total_price = sum(item.subtotal for item in items)

    return render(request, 'cart.html', {'cart': cart, 'items': items, 'total_price': total_price})

# Agregar un producto al carrito
#@login_required
def add_to_cart(request, instrument_id):
    instrument = get_object_or_404(Instrument, id=instrument_id)
    cart, created = Cart.objects.get_or_create(user=request.user, defaults={'created_at': date.today()})

    cart_item, item_created = Cart_Item.objects.get_or_create(
        cart=cart, 
        instrument=instrument,
        defaults={'added_at': date.today(), 'quantity': 1}
        )
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('catalog')

# Incrementar la cantidad de un producto en el carrito
#@login_required
def increase_quantity(request, item_id):
    item = get_object_or_404(Cart_Item, id=item_id)
    if item.cart.user == request.user:
        item.quantity += 1
        item.save()

    return redirect('cart_view')

# Disminuir la cantidad de un producto en el carrito
#@login_required
def decrease_quantity(request, item_id):
    item = get_object_or_404(Cart_Item, id=item_id)
    if item.cart.user == request.user:
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
        else:
            item.delete()  # Elimina el item si la cantidad es 0

    return redirect('cart_view')

# Eliminar un producto del carrito
#@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(Cart_Item, id=item_id)
    if item.cart.user == request.user:
        item.delete()

    return redirect('cart_view')
