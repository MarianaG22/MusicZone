from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cart, Cart_Item, Sale, Sale_Detail, Order
from Inventory.models import Instrument
from Users.models import User
from django.utils.timezone import now
from django.http import JsonResponse
from django.contrib import messages
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

# Realizar pedido
@login_required
def register_sale(request):
    if request.method == "POST":
        cart = Cart.objects.filter(user=request.user).first()  
        if not cart or not Cart_Item.objects.filter(cart=cart).exists():
            return JsonResponse({"success": False, "message": "El carrito está vacío."})

        user = request.user  
        items = Cart_Item.objects.filter(cart=cart)
        total_price = sum(item.instrument.price * item.quantity for item in items)

        # Registrar la venta
        sale = Sale.objects.create(user=user, total_price=total_price, date=now())

        # Crear la orden relacionada
        Order.objects.create(sale=sale, order_date=date.today())

        for item in items:
            instrument = item.instrument
            # Mensaje de stock bajo 
            if instrument.stock < item.quantity:
                if user.is_staff:
                    mensaje = f"No hay suficiente stock de {instrument.instrument}."
                else:
                    mensaje = f"Lo sentimos, el instrumento {instrument.instrument} no está disponible en este momento."
                return JsonResponse({"success": False, "message": mensaje})
            # Datos
            Sale_Detail.objects.create(
                sale=sale,
                instrument=instrument,
                quantity=item.quantity,
                price=instrument.price
            )
            # Reducir el stock
            instrument.stock -= item.quantity
            instrument.save()

        # Vaciar carrito después de la compra
        items.delete()

        # Notificar al administrador
        admin_user = User.objects.filter(is_superuser=True).first()
        if admin_user:
            messages.success(request, f"Nuevo pedido realizado por {user.username}. Total: ${total_price}")

        return JsonResponse({"success": True, "message": "¡Pedido realizado exitosamente!"})
    
    return JsonResponse({"success": False, "message": "Método no permitido."})

@login_required
def order_list(request):
    if request.user.is_staff:
        orders = Order.objects.select_related('sale', 'sale__user').all()
    else:
        orders = Order.objects.filter(sale__user=request.user)

    return render(request, 'order_list.html', {'orders': orders})

def toggle_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.user.is_staff and request.method == "POST":
        new_status = request.POST.get('new_status')
        if new_status in dict(Order.Status.choices).keys():
            order.status = new_status
            order.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'new_status': order.get_status_display()})
            return redirect('order_list')
    return JsonResponse({'success': False, 'error': 'No autorizado'}, status=403)