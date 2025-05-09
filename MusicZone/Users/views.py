# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import User, Role
from Sales.models import Order

@staff_member_required(login_url='/')
@login_required
def user(request):
    usuarios = User.objects.all()
    return render(request, 'users/user.html', {'usuarios': usuarios})

@staff_member_required(login_url='/')
@login_required
def add_user(request):
    roles = Role.objects.all()
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        name = request.POST.get('name')
        last_name = request.POST.get('last_name')
        role_id = request.POST.get('role')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya existe.')
        else:
            role = get_object_or_404(Role, pk=role_id)
            usuario = User.objects.create_user(
                username=username, email=email, name=name,
                last_name=last_name, role=role
            )
            messages.success(request, 'Usuario creado exitosamente.')
            return redirect('users:user')

    return render(request, 'users/add_user.html', {'roles': roles})

@staff_member_required(login_url='/')
@login_required
def edit_user(request, usuario_id):
    usuario = get_object_or_404(User, pk=usuario_id)
    roles = Role.objects.all()
    
    if request.method == 'POST':
        usuario.username = request.POST.get('username')
        usuario.email = request.POST.get('email')
        usuario.name = request.POST.get('name')
        usuario.last_name = request.POST.get('last_name')
        role_id = request.POST.get('role')
        usuario.role = get_object_or_404(Role, pk=role_id)

        if request.POST.get('password'):
            usuario.set_password(request.POST.get('password'))

        usuario.save()
        messages.success(request, 'Usuario actualizado correctamente.')
        return redirect('users:user')

    return render(request, 'users/edit_user.html', {'usuario': usuario, 'roles': roles})

@staff_member_required(login_url='/')
@login_required
def remove_user(request, usuario_id):
    usuario = get_object_or_404(User, pk=usuario_id)
    
    if request.method == 'POST':  # Asegúrate de que la eliminación se haga con un POST
        usuario.delete()
        messages.success(request, 'Usuario eliminado correctamente.')
        return redirect('users:user')
    
    # Si no es POST, muestra un mensaje o redirige de alguna manera
    return redirect('users:user')  # O puedes mostrar un mensaje de advertencia

@login_required
def user_profile(request):
    orders = Order.objects.filter(sale__user=request.user).select_related('sale').prefetch_related('sale__sale_detail_set')
    print(orders)
    return render(request, 'user_profile.html', {'orders': orders})

@login_required
def mark_as_received(request, order_id):
    order = get_object_or_404(Order, id=order_id, sale__user=request.user)
    if order.status != Order.Status.RECIBIDO:
        order.status = Order.Status.RECIBIDO
        order.save()
        messages.success(request, 'El pedido ha sido marcado como recibido.')
    else:
        messages.info(request, 'El pedido ya estaba marcado como recibido.')
    return redirect('users:user_profile')