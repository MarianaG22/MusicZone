import pytest
from django.urls import reverse, resolve
from Users import views

@pytest.mark.django_db
def test_url_lista_usuarios():
    ruta = reverse('users:user')
    assert resolve(ruta).func == views.user

@pytest.mark.django_db
def test_url_crear_usuario():
    ruta = reverse('users:add_user')
    assert resolve(ruta).func == views.add_user

@pytest.mark.django_db
def test_url_editar_usuario():
    ruta = reverse('users:edit_user', kwargs={'usuario_id': 1})
    assert resolve(ruta).func == views.edit_user

@pytest.mark.django_db
def test_url_eliminar_usuario():
    ruta = reverse('users:remove_user', kwargs={'usuario_id': 1})
    assert resolve(ruta).func == views.remove_user