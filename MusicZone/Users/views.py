# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import User, Role

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

@staff_member_required(login_url='/')
@login_required
def role(request):
    roles = Role.objects.all()
    return render(request, 'roles/role.html', {'roles': roles})

@staff_member_required(login_url='/')
@login_required
def add_role(request):
    if request.method == 'POST':
        nombre_rol = request.POST.get('role')
        if not Role.objects.filter(role=nombre_rol).exists():
            Role.objects.create(role=nombre_rol)
            messages.success(request, 'Rol creado correctamente.')
        else:
            messages.error(request, 'Este rol ya existe.')
            return redirect('users:user')
    return redirect('users:role')

@staff_member_required(login_url='/')
@login_required
def edit_role(request, role_id):
    rol = get_object_or_404(Role, pk=role_id)
    roles = Role.objects.all()
    if request.method == 'POST':
        new_name = request.POST.get('role_name')
        
        if Role.objects.filter(role=new_name).exclude(pk=role_id).exists():
            messages.error(request, 'Este nombre de rol ya está en uso.')
        else:
            rol.role = new_name
            rol.save()
            messages.success(request, 'Rol actualizado correctamente.')
            return redirect('users:role')
    return render(request, 'roles/role.html', {'roles': roles})

@staff_member_required(login_url='/')
@login_required
def delete_role(request, role_id):
    rol = get_object_or_404(Role, pk=role_id)
    if request.method == 'POST':
        rol.delete()
        messages.success(request, 'Rol eliminado correctamente.')
        return redirect('users:role')
    return redirect('users:role')