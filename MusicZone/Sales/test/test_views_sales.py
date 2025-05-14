import pytest
from django.urls import reverse
from Sales.models import Cart, Cart_Item, Order, Sale, Sale_Detail
from Inventory.models import Instrument, Type, Mark
from Users.models import User
from datetime import date
from django.core.files.uploadedfile import SimpleUploadedFile

@pytest.fixture
def cliente_usuario(client, django_user_model):
    user = django_user_model.objects.create_user(
        username="testuser",
        password="password123",
        email="testuser@example.com"
    )
    client.login(username="testuser", password="password123")
    return client, user

@pytest.fixture
def cliente_admin(client, django_user_model):
    admin = django_user_model.objects.create_user(
        username="admin",
        password="admin123",
        email="admin@example.com",
        is_staff=True
    )
    client.login(username="admin", password="admin123")
    return client, admin

@pytest.mark.django_db
def test_cart_view(cliente_usuario):
    client, user = cliente_usuario
    url = reverse('sales:cart_view')
    respuesta = client.get(url)
    assert respuesta.status_code == 200

@pytest.mark.django_db
def test_add_to_cart(cliente_usuario):
    client, user = cliente_usuario
    tipo = Type.objects.create(type="Cuerda")
    marca = Mark.objects.create(mark="Yamaha")
    instrumento = Instrument.objects.create(
        instrument="Guitarra",
        type=tipo,
        mark=marca,
        price=500000,
        stock=10
    )
    url = reverse('sales:add_to_cart', kwargs={'instrument_id': instrumento.id})
    respuesta = client.post(url)
    assert respuesta.status_code == 302  # Redirección
    assert Cart_Item.objects.filter(instrument=instrumento).exists()

@pytest.mark.django_db
def test_remove_from_cart(cliente_usuario):
    client, user = cliente_usuario
    tipo = Type.objects.create(type="Cuerda")
    marca = Mark.objects.create(mark="Yamaha")
    instrumento = Instrument.objects.create(
        instrument="Guitarra",
        type=tipo,
        mark=marca,
        price=500000,
        stock=10
    )
    cart = Cart.objects.create(user=user, created_at=date.today())
    cart_item = Cart_Item.objects.create(cart=cart, instrument=instrumento, quantity=1, added_at=date.today())
    url = reverse('sales:remove_from_cart', kwargs={'item_id': cart_item.id})
    respuesta = client.post(url)
    assert respuesta.status_code == 302  # Redirección
    assert not Cart_Item.objects.filter(id=cart_item.id).exists()

@pytest.mark.django_db
def test_register_sale(cliente_usuario):
    client, user = cliente_usuario
    tipo = Type.objects.create(type="Cuerda")
    marca = Mark.objects.create(mark="Yamaha")
    instrumento = Instrument.objects.create(
        instrument="Guitarra",
        type=tipo,
        mark=marca,
        price=500000,
        stock=10
    )
    cart = Cart.objects.create(user=user, created_at=date.today())
    Cart_Item.objects.create(cart=cart, instrument=instrumento, quantity=1, added_at=date.today())
    url = reverse('sales:register_sale')
    respuesta = client.post(url)
    assert respuesta.status_code == 200
    assert Sale.objects.filter(user=user).exists()
    assert Order.objects.filter(sale__user=user).exists()
