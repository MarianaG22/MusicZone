import pytest
from Sales.models import Sale, Sale_Detail, Order, Cart, Cart_Item
from Users.models import User
from Inventory.models import Instrument, Type, Mark
from datetime import date

@pytest.mark.django_db
def test_crear_venta():
    user = User.objects.create_user(username="testuser", password="password123")
    sale = Sale.objects.create(user=user, total_price=100000, date=date.today())
    assert sale.user == user
    assert sale.total_price == 100000
    assert sale.date == date.today()
    assert str(sale) == f"Sale #{sale.id} - {user.username}"

@pytest.mark.django_db
def test_crear_detalle_venta():
    user = User.objects.create_user(username="testuser", password="password123")
    tipo = Type.objects.create(type="Cuerda")
    marca = Mark.objects.create(mark="Yamaha")
    instrumento = Instrument.objects.create(
        instrument="Guitarra",
        type=tipo,
        mark=marca,
        price=500000,
        stock=10
    )
    sale = Sale.objects.create(user=user, total_price=500000, date=date.today())
    detalle = Sale_Detail.objects.create(sale=sale, instrument=instrumento, quantity=2, price=1000000)
    assert detalle.sale == sale
    assert detalle.instrument == instrumento
    assert detalle.quantity == 2
    assert detalle.price == 1000000
    assert str(detalle) == f"SaleDetail #{detalle.id} - Sale #{sale.id} - {instrumento.instrument}"

@pytest.mark.django_db
def test_crear_orden():
    user = User.objects.create_user(username="testuser", password="password123")
    sale = Sale.objects.create(user=user, total_price=100000, date=date.today())
    order = Order.objects.create(sale=sale, status=Order.Status.PENDIENTE, order_date=date.today())
    assert order.sale == sale
    assert order.status == Order.Status.PENDIENTE
    assert order.order_date == date.today()
    assert str(order) == f"Order #{order.id} - Sale #{sale.id} - Pendiente"

@pytest.mark.django_db
def test_crear_carrito():
    user = User.objects.create_user(username="testuser", password="password123")
    cart = Cart.objects.create(user=user, created_at=date.today())
    assert cart.user == user
    assert cart.created_at == date.today()
    assert str(cart) == f"Cart #{cart.id} - {user.username}"

@pytest.mark.django_db
def test_crear_item_carrito():
    user = User.objects.create_user(username="testuser", password="password123")
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
    cart_item = Cart_Item.objects.create(cart=cart, instrument=instrumento, quantity=3, added_at=date.today())
    assert cart_item.cart == cart
    assert cart_item.instrument == instrumento
    assert cart_item.quantity == 3
    assert cart_item.added_at == date.today()
    assert str(cart_item) == f"CartItem #{cart_item.id} - Cart #{cart.id} - {instrumento.instrument}"