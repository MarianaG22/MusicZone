import pytest
from Inventory.models import Type, Mark, Instrument

@pytest.mark.django_db
def test_crear_tipo():
    tipo = Type.objects.create(type="Cuerda")
    assert tipo.type == "Cuerda"
    assert str(tipo) == "Cuerda"

@pytest.mark.django_db
def test_crear_marca():
    marca = Mark.objects.create(mark="Yamaha")
    assert marca.mark == "Yamaha"
    assert str(marca) == "Yamaha"

@pytest.mark.django_db
def test_crear_instrumento():
    tipo = Type.objects.create(type="Cuerda")
    marca = Mark.objects.create(mark="Yamaha")
    instrumento = Instrument.objects.create(
        instrument="Guitarra Acústica",
        type=tipo,
        mark=marca,
        price=500000,
        stock=10,
        image="galery/guitarra.jpg"
    )
    assert instrumento.instrument == "Guitarra Acústica"
    assert instrumento.type == tipo
    assert instrumento.mark == marca
    assert instrumento.price == 500000
    assert instrumento.stock == 10
    assert instrumento.image == "galery/guitarra.jpg"
    assert str(instrumento) == "Guitarra Acústica"

@pytest.mark.django_db
def test_instrumento_sin_imagen():
    tipo = Type.objects.create(type="Percusión")
    marca = Mark.objects.create(mark="Roland")
    instrumento = Instrument.objects.create(
        instrument="Batería Electrónica",
        type=tipo,
        mark=marca,
        price=1500000,
        stock=5,
        image="galery/default.jpg"  # Imagen por defecto
    )
    assert instrumento.image == "galery/default.jpg"