import pytest
from django.urls import reverse, resolve
from Inventory import views

@pytest.mark.django_db
def test_url_instrumento():
    ruta = reverse('products:instrumento')
    assert resolve(ruta).func == views.instrumento

@pytest.mark.django_db
def test_url_crear_instrumento():
    ruta = reverse('products:crear_instrumento')
    assert resolve(ruta).func == views.crear_instrumento

@pytest.mark.django_db
def test_url_editar_instrumento():
    ruta = reverse('products:editar_instrumento', kwargs={'instrument_id': 1})
    assert resolve(ruta).func == views.editar_instrumento

@pytest.mark.django_db
def test_url_eliminar_instrumento():
    ruta = reverse('products:eliminar_instrumento', kwargs={'instrument_id': 1})
    assert resolve(ruta).func == views.eliminar_instrumento

@pytest.mark.django_db
def test_url_catalogo():
    ruta = reverse('products:catalog')
    assert resolve(ruta).func == views.catalog