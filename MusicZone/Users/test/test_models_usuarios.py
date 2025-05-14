import pytest
from Users.models import Role, User

@pytest.mark.django_db
def test_crear_rol():
    rol = Role.objects.create(role="Admin")
    assert rol.role == "Admin"
    assert str(rol) == "Admin"

@pytest.mark.django_db
def test_crear_usuario():
    rol = Role.objects.create(role="Admin")
    usuario = User.objects.create_user(
        username="usuarioprueba",
        password="contraseñaprueba",
        email="usuarioprueba@ejemplo.com",
        name="Prueba",
        last_name="Usuario",
        role=rol
    )
    assert usuario.username == "usuarioprueba"
    assert usuario.check_password("contraseñaprueba")
    assert usuario.email == "usuarioprueba@ejemplo.com"
    assert usuario.name == "Prueba"
    assert usuario.last_name == "Usuario"
    assert usuario.role == rol
    assert str(usuario) == "usuarioprueba"

@pytest.mark.django_db
def test_usuario_sin_rol():
    usuario = User.objects.create_user(
        username="usuariosinrol",
        password="contraseñaprueba",
        email="usuariosinrol@ejemplo.com",
        name="Sin",
        last_name="Rol"
    )
    assert usuario.username == "usuariosinrol"
    assert usuario.role is None