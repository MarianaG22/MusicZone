from django.db import models
from Users.models import User
from Inventory.models import Instrument

# Create your models here.
class Sale(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario")
    total_price = models.IntegerField(verbose_name="Precio Total")
    date = models.DateField(verbose_name="Fecha")

    def __str__(self):
        return f"Sale #{self.id} - {self.user.username}"

class Sale_Detail(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, verbose_name="Venta")
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE, verbose_name="Instrumento")
    quantity = models.IntegerField(verbose_name="Cantidad")
    price = models.IntegerField(verbose_name="Precio")

    def __str__(self):
        return f"SaleDetail #{self.id} - Sale #{self.sale.id} - {self.instrument.name}"

class Order(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, verbose_name="Venta")
    status = models.BooleanField(default=False, verbose_name="Estado")
    order_date = models.DateField(verbose_name="Fecha de Pedido")

    def __str__(self):
        return f"Order #{self.id} - Sale #{self.sale.id} - {'Completed' if self.status else 'Pending'}"

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario")
    created_at = models.DateField(verbose_name="Fecha de Creación")

    def __str__(self):
        return f"Cart #{self.id} - {self.user.username}"
    
class Cart_Item(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name="Carrito")
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE, verbose_name="Instrumento")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Quantity")
    added_at = models.DateField(verbose_name="Fecha de Adición")

    def __str__(self):
        return f"CartItem #{self.id} - Cart #{self.cart.id} - {self.instrument.instrument}"