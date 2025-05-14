import pytest
from django.urls import reverse
from Inventory.models import Instrument, Type, Mark
from django.core.files.uploadedfile import SimpleUploadedFile

@pytest.fixture
def cliente_admin(client, django_user_model):
    # Crear un usuario administrador para las pruebas
    admin_user = django_user_model.objects.create_user(
        username="admin",
        password="admin123",
        is_staff=True,
        is_superuser=True
    )
    client.login(username="admin", password="admin123")
    return client

@pytest.fixture
def cliente_usuario(client, django_user_model):
    # Crear un usuario normal para las pruebas
    normal_user = django_user_model.objects.create_user(
        username="usuario",
        password="usuario123",
        is_staff=False,
        is_superuser=False
    )
    client.login(username="usuario", password="usuario123")
    return client

@pytest.mark.django_db
def test_vista_instrumento(cliente_admin):
    # Crear datos de prueba
    tipo = Type.objects.create(type="Cuerda")
    marca = Mark.objects.create(mark="Yamaha")
    Instrument.objects.create(instrument="Guitarra", type=tipo, mark=marca, price=500000, stock=10)

    url = reverse('products:instrumento')
    respuesta = cliente_admin.get(url)

    assert respuesta.status_code == 200
    assert "Guitarra" in respuesta.content.decode()

@pytest.mark.django_db
def test_vista_crear_instrumento(cliente_admin):
    tipo = Type.objects.create(type="Cuerda")
    marca = Mark.objects.create(mark="Yamaha")
    url = reverse('products:crear_instrumento')

    datos = {
        "instrument": "Piano",
        "type": tipo.id,
        "mark": marca.id,
        "price": 1000000,
        "stock": 5,
        "image": SimpleUploadedFile("piano.jpg", b"file_content", content_type="image/jpeg")
    }

    respuesta = cliente_admin.post(url, datos)

    assert respuesta.status_code == 302  # Redirección después de crear
    assert Instrument.objects.filter(instrument="Piano").exists()

@pytest.mark.django_db
def test_vista_editar_instrumento(cliente_admin):
    tipo = Type.objects.create(type="Cuerda")
    marca = Mark.objects.create(mark="Yamaha")
    instrumento = Instrument.objects.create(instrument="Guitarra", type=tipo, mark=marca, price=500000, stock=10)

    url = reverse('products:editar_instrumento', kwargs={'instrument_id': instrumento.id})
    datos = {
        "instrument": "Guitarra Eléctrica",
        "type": tipo.id,
        "mark": marca.id,
        "price": 600000,
        "stock": 8
    }

    respuesta = cliente_admin.post(url, datos)

    assert respuesta.status_code == 302  # Redirección después de editar
    instrumento.refresh_from_db()
    assert instrumento.instrument == "Guitarra Eléctrica"
    assert instrumento.price == 600000
    assert instrumento.stock == 8

@pytest.mark.django_db
def test_vista_eliminar_instrumento(cliente_admin):
    tipo = Type.objects.create(type="Cuerda")
    marca = Mark.objects.create(mark="Yamaha")
    instrumento = Instrument.objects.create(instrument="Guitarra", type=tipo, mark=marca, price=500000, stock=10)

    url = reverse('products:eliminar_instrumento', kwargs={'instrument_id': instrumento.id})
    respuesta = cliente_admin.post(url)

    assert respuesta.status_code == 302  # Redirección después de eliminar
    assert not Instrument.objects.filter(id=instrumento.id).exists()

@pytest.mark.django_db
def test_vista_catalogo(cliente_usuario):
    tipo = Type.objects.create(type="Cuerda")
    marca = Mark.objects.create(mark="Yamaha")
    Instrument.objects.create(
        instrument="Guitarra",
        type=tipo,
        mark=marca,
        price=500000,
        stock=10,
        image=SimpleUploadedFile("guitarra.jpg", b"file_content", content_type="image/jpeg")
    )

    url = reverse('products:catalog')
    respuesta = cliente_usuario.get(url)

    assert respuesta.status_code == 200
    assert "Guitarra" in respuesta.content.decode()