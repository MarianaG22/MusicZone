import pytest
from django.urls import reverse
from Users.models import User, Role

@pytest.fixture
def cliente_admin(client):
    # Crear un usuario administrador para las pruebas
    usuario_admin = User.objects.create_user(
        username="admin",
        password="admin123",
        is_staff=True,
        is_superuser=True,
        email="admin@ejemplo.com",
        name="Admin",
        last_name="Usuario"
    )
    client.login(username="admin", password="admin123")
    return client

@pytest.mark.django_db
def test_vista_lista_usuarios(cliente_admin):
    # Crear datos de prueba
    rol = Role.objects.create(role="Admin")
    User.objects.create(username="usuario1", email="usuario1@ejemplo.com", role=rol)
    User.objects.create(username="usuario2", email="usuario2@ejemplo.com", role=rol)

    # Acceder a la vista
    url = reverse('users:user')
    respuesta = cliente_admin.get(url)

    # Aserciones
    assert respuesta.status_code == 200
    assert "usuario1" in respuesta.content.decode()
    assert "usuario2" in respuesta.content.decode()

@pytest.mark.django_db
def test_vista_crear_usuario(cliente_admin):
    rol = Role.objects.create(role="Admin")
    url = reverse('users:add_user')
    datos = {
        "username": "nuevousuario",
        "email": "nuevousuario@ejemplo.com",
        "name": "Nuevo",
        "last_name": "Usuario",
        "role": rol.id,
        "password": "contraseña123"
    }

    respuesta = cliente_admin.post(url, datos)

    # Aserciones
    assert respuesta.status_code == 302  # Redirección después de la creación
    assert User.objects.filter(username="nuevousuario").exists()

@pytest.mark.django_db
def test_vista_eliminar_usuario(cliente_admin):
    rol = Role.objects.create(role="Admin")
    usuario = User.objects.create(username="usuario_prueba", email="prueba@ejemplo.com", role=rol)

    url = reverse('users:remove_user', args=[usuario.id])
    respuesta = cliente_admin.post(url)

    # Aserciones
    assert respuesta.status_code == 302  # Redirección después de la eliminación
    assert not User.objects.filter(username="usuario_prueba").exists()

@pytest.mark.django_db
def test_vista_editar_usuario(cliente_admin):
    rol = Role.objects.create(role="Admin")
    usuario = User.objects.create(username="usuario_prueba", email="prueba@ejemplo.com", role=rol)

    url = reverse('users:edit_user', args=[usuario.id])
    datos = {
        "username": "usuario_actualizado",
        "email": "actualizado@ejemplo.com",
        "name": "Actualizado",
        "last_name": "Usuario",
        "role": rol.id,
        "password": "contraseña123"
    }

    respuesta = cliente_admin.post(url, datos)

    # Aserciones
    assert respuesta.status_code == 302  # Redirección después de la actualización
    usuario.refresh_from_db()
    assert usuario.username == "usuario_actualizado"
    assert usuario.email == "actualizado@ejemplo.com"