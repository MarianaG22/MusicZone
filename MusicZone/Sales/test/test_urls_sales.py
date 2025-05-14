import pytest
from django.urls import reverse, resolve
from Sales import views

@pytest.mark.django_db
def test_url_cart_view():
    ruta = reverse('sales:cart_view')
    assert resolve(ruta).func == views.cart_view

@pytest.mark.django_db
def test_url_add_to_cart():
    ruta = reverse('sales:add_to_cart', kwargs={'instrument_id': 1})
    assert resolve(ruta).func == views.add_to_cart

@pytest.mark.django_db
def test_url_remove_from_cart():
    ruta = reverse('sales:remove_from_cart', kwargs={'item_id': 1})
    assert resolve(ruta).func == views.remove_from_cart

@pytest.mark.django_db
def test_url_increase_quantity():
    ruta = reverse('sales:increase_quantity', kwargs={'item_id': 1})
    assert resolve(ruta).func == views.increase_quantity

@pytest.mark.django_db
def test_url_decrease_quantity():
    ruta = reverse('sales:decrease_quantity', kwargs={'item_id': 1})
    assert resolve(ruta).func == views.decrease_quantity

@pytest.mark.django_db
def test_url_register_sale():
    ruta = reverse('sales:register_sale')
    assert resolve(ruta).func == views.register_sale

@pytest.mark.django_db
def test_url_order_list():
    ruta = reverse('sales:order_list')
    assert resolve(ruta).func == views.order_list

@pytest.mark.django_db
def test_url_toggle_order_status():
    ruta = reverse('sales:toggle_order_status', kwargs={'order_id': 1})
    assert resolve(ruta).func == views.toggle_order_status